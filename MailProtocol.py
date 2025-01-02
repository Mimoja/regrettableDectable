import asyncio
import time
from typing import Dict
from util import hexdump
from APIParser import parseMail
from Api.Api import BaseCommand


class MailProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None
        self.tx_seq = 0  # Transmit sequence number
        self.rx_seq = 0  # Receive sequence number
        self.outstanding_frames: Dict[int, bytes] = {}  # Track unacknowledged frames
        self.poll_timers: Dict[int, float] = {}  # Track PollFinal timers
        self.timer_duration = 1.0  # PollFinal timer duration in seconds
        self.synced = False
        self.temp_buffer = b""

    def connection_made(self, transport):
        self.transport = transport
        self.send_sabm()
        print("Connection established.")

    def data_received(self, data):
        # print("Data received (hexdump):")
        # print(hexdump(data))
        self.handle_frame(data)

    def connection_lost(self, exc):
        print("Connection lost.")
        self.synced = False
        asyncio.get_event_loop().stop()

    def send_sabm(self, pf=True):
        header = 0xC8 if pf else 0xC0
        frame = bytes([0x10, 0x00, 0x01, header, header])
        self.transport.write(frame)
        print(f"SABM frame sent: {hexdump(frame, False)}")
        self.outstanding_frames = {}
        self.rx_seq = 0
        self.tx_seq = 0

    def send_information_frame(self, payload: bytes, pf=True):
        header = self.tx_seq << 4 | self.rx_seq
        # Set PollFinal bit
        if pf:
            header |= 0x08
        frame = bytes([0x10, 0x00, len(payload) + 1, header]) + payload
        checksum = (header + sum(payload)) & 0xFF
        frame += bytes([checksum])
        tx_seq = self.tx_seq
        self.outstanding_frames[self.tx_seq] = frame
        self.tx_seq = (self.tx_seq + 1) % 8  # Wrap TxSeq
        self.transport.write(frame)
        print(
            f"Information frame sent TxSeq={tx_seq}, self.TxSeq={self.tx_seq}:\n{hexdump(frame, True)}"
        )

    def send_supervisory_frame(self, su_id: int, pf=True):
        header = 0x80 | (su_id << 4) | self.rx_seq
        # Set PollFinal bit
        if pf:
            header |= 0x08
        frame = bytes([0x10, 0x00, 0x01, header, header])
        self.transport.write(frame)
        # print(f"Supervisory frame sent: {hexdump(frame, False)}")

    def send(self, command: BaseCommand, program_id=0, task_id=1):
        """
        Send a command as an information frame.
        :param params: Additional parameters (bytes)
        :param program_id: Program ID byte
        :param task_id: Task ID byte
        """
        command_bytes = command.to_bytes()
        payload = bytes([program_id, task_id, *command_bytes])

        self.send_information_frame(payload)
        print(
            f"Command sent: Program ID={program_id}, Task ID={task_id}, Payload={hexdump(bytes([*payload]), False)}"
        )

    def send_command(
        self, program_id: int, task_id: int, primitive: int, params: bytes
    ):
        """
        Send a command as an information frame.
        :param program_id: Program ID byte
        :param task_id: Task ID byte
        :param primitive: Primitive (2 bytes, big-endian)
        :param params: Additional parameters (bytes)
        """

        primitive_high = (primitive >> 8) & 0xFF
        primitive_low = primitive & 0xFF
        payload = bytes([program_id, task_id, primitive_low, primitive_high, *params])

        self.send_information_frame(payload)
        print(
            f"Command sent: Program ID={program_id}, Task ID={task_id}, Primitive=0x{primitive:2x}, Params={hexdump(bytes([*params]), False)}"
        )

    def handle_frame(self, data):
        """
        Handle incoming data, process complete frames, and deal with leftover bytes.
        """
        # Append new data to the buffer
        self.temp_buffer += data

        while len(self.temp_buffer) >= 5:
            # Extract the frame header
            header = self.temp_buffer[3]
            is_control_frame = header & 0x80
            pf = bool(header & 0x08)
            # Information frame
            if not is_control_frame:
                tx_seq = (header >> 4) & 0x07
                rx_seq = header & 0x07
                payload_length = self.temp_buffer[2] - 1
                if len(self.temp_buffer) < 5 + payload_length:
                    # Incomplete frame
                    print("Incomplete information frame, waiting for more data.")
                    break

                payload = self.temp_buffer[4 : 4 + payload_length]
                checksum = self.temp_buffer[4 + payload_length]

                if (header + sum(payload)) & 0xFF == checksum:
                    acked = False
                    if rx_seq == self.tx_seq:
                        self.rx_seq = (self.rx_seq + 1) % 8
                        acked = True
                    # # print(
                    # #     f"Valid information frame received: TxSeq={tx_seq}, self.TxSeq={self.tx_seq} RxSeq={rx_seq} Acked={acked} self.RxSeq={self.rx_seq} "
                    # # )

                    #    As per spec, at least 4 bytes are needed for Program Id + Task Id + Primitive
                    if len(payload) >= 4:
                        program_id = payload[0]
                        task_id = payload[1]
                        primitive = (payload[3] << 8) | payload[2]
                        mail_params = payload[4:]

                        print(
                            f"Message Recieved: Program ID={program_id}, Task ID={task_id}, Primitive=0x{primitive:2x}, Params=\n{hexdump(mail_params)}"
                        )
                        parseMail(primitive, mail_params)

                    else:

                        print(
                            {
                                "header": header,
                                "payload": hexdump(payload, False),
                            }
                        )

                    self.send_supervisory_frame(0, pf)  # Send RR frame
                else:
                    print("Invalid checksum, rejecting frame.")
                    self.send_supervisory_frame(1, pf)  # Send REJ frame

                # Remove processed frame from the buffer
                self.temp_buffer = self.temp_buffer[5 + payload_length :]
            # Control frame
            else:
                unnumbered = header >> 6 & 0x01
                su_id = (header >> 4) & 0x03

                if unnumbered:
                    print(f"SABM frame received. SU_ID={su_id} pf={pf}")
                    if not self.synced and su_id == 0x00 and pf:
                        self.send_sabm(pf=False)
                else:
                    rx_seq = header & 0x07

                    if len(self.temp_buffer) < 5:
                        print("Incomplete control frame, waiting for more data.")
                        break

                    if su_id == 0:
                        print(
                            f"Receive Ready (RR) frame received. RXSeq={rx_seq} self.TxSeq={self.tx_seq}"
                        )

                        if (rx_seq - 1) % 8 in self.outstanding_frames:
                            del self.outstanding_frames[(rx_seq - 1) % 8]
                        self.resend_outstanding_frames()
                    elif su_id == 1:
                        print(
                            f"Reject (REJ) frame received. RXSeq={rx_seq} self.TxSeq={self.tx_seq}"
                        )
                        self.resend_outstanding_frames()
                    elif su_id == 2:
                        print(
                            f"Receiver Not Ready (RNR) frame received. RXSeq={rx_seq} self.TxSeq={self.tx_seq}"
                        )
                    elif su_id == 3:
                        print("Unnumbered control frame received.")

                # Remove processed control frame from the buffer
                self.temp_buffer = self.temp_buffer[5:]

        # If data remains, it is incomplete or garbage
        if self.temp_buffer:
            print(f"Leftover bytes in buffer: {hexdump(self.temp_buffer)}")
            if 0x10 not in self.temp_buffer:
                print("Buffer contains garbage bytes, clearing buffer.")
                self.temp_buffer = b""

    def resend_outstanding_frames(self):
        if len(self.outstanding_frames.keys()) == 0:
            return
        print("Resending outstanding frames.")
        for seq, frame in self.outstanding_frames.items():
            print(f"Resending frame: TxSeq={seq}")
            self.transport.write(frame)

    async def poll_timer(self):
        while True:
            now = time.time()
            expired_timers = [
                seq
                for seq, start_time in self.poll_timers.items()
                if now - start_time >= self.timer_duration
            ]
            for seq in expired_timers:
                print(f"Poll timer expired for TxSeq={seq}, resending frame.")
                frame = self.outstanding_frames.get(seq)
                if frame:
                    self.transport.write(frame)
                    self.poll_timers[seq] = time.time()
            await asyncio.sleep(0.1)
