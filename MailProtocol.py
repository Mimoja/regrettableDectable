import asyncio
import time
from typing import Dict, List, Tuple
from util import hexdump, is_mod8_less
from APIParser import parseMail
from Api.Api import BaseCommand
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MailProtocol")


class MailProtocol(asyncio.Protocol):
    """
    AI BULLSHIT WARNING!
    The below comment was hallucinated by a brainless machine, do NOT trust it.
    Please remove this Warning upon review / verification of correctness.
    
    Implementation of the DECT Mail Protocol over serial communication.
    Handles frame-based communication with sequence numbers and acknowledgments.

    This protocol implements:
    - Information frames for data transfer
    - Supervisory frames for flow control
    - SABM (Set Asynchronous Balanced Mode) for connection establishment
    - Automatic retransmission of unacknowledged frames
    """

    def __init__(self, onMessage):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Initialize the Mail Protocol.

        Args:
            onMessage: Callback function to handle received messages
        """
        self.transport = None
        self.tx_seq = 0  # Transmit sequence number
        self.rx_seq = 0  # Receive sequence number
        self.outstanding_frames: Dict[int, bytes] = {}  # Track unacknowledged frames
        self.max_outstanding = 7
        self.poll_timers: Dict[int, float] = {}  # Track PollFinal timers
        self.timer_duration = 1.0  # PollFinal timer duration in seconds
        self.temp_buffer = b""
        self.onMessage = onMessage
        self.wait_for_sabm = False
        self.message_queue: List[Tuple[bytes, bool]] = []

    def connection_made(self, transport):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Called when a connection is established.

        Args:
            transport: The transport instance for the connection
        """
        self.transport = transport
        logger.info("Connection established.")

    def data_received(self, data):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Called when data is received from the transport.

        Args:
            data (bytes): Received data
        """
        logger.debug(f"Data received: {hexdump(data)}")
        self.handle_frame(data)

    def connection_lost(self, exc):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Called when the connection is lost or closed.

        Args:
            exc: The exception causing the connection loss, if any
        """
        logger.info("Connection lost.")
        asyncio.get_event_loop().stop()

    def send_sabm(self, pf=True):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Send a SABM (Set Asynchronous Balanced Mode) frame.
        Used for connection establishment and reset.

        Args:
            pf (bool): Poll/Final bit value

        Returns:
            asyncio.Event: Event that will be set when SABM acknowledgment is received
        """
        self.wait_for_sabm = asyncio.Event()
        header = 0xC8 if pf else 0xC0
        frame = bytes([0x10, 0x00, 0x01, header, header])
        self.transport.write(frame)
        logger.debug(f"SABM frame sent: {hexdump(frame, False)}")
        self.outstanding_frames = {}
        self.rx_seq = 0
        self.tx_seq = 0
        return self.wait_for_sabm

    def flush_message_queue(self):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Process queued messages that are waiting to be sent.
        Messages are sent if there's room in the outstanding frames window.
        """
        if not self.message_queue:
            return
        now = time.time()
        sendable = []
        remaining = []

        for payload, pf in self.message_queue:
            block_until = self.mark_expiry.get(0)
            if (
                now >= block_until
                and len(self.outstanding_frames) < self.max_outstanding
            ):
                sendable.append((payload, pf))
            else:
                remaining.append((payload, pf))

        self.message_queue = remaining

        for payload, pf in sendable:
            self._actually_send_information_frame(payload, pf)

    def send_information_frame(self, payload: bytes, pf=True):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Queue an information frame for transmission.

        Args:
            payload (bytes): Data to be sent
            pf (bool): Poll/Final bit value
        """
        if len(self.outstanding_frames) >= self.max_outstanding:
            logger.info(
                f"Queueing message"
                f"because we have {len(self.outstanding_frames)} frames in flight "
                f"(max {self.max_outstanding}). Payload={hexdump(payload, False)}"
            )
            self.message_queue.append((payload, pf))
            return
        else:
            self._actually_send_information_frame(payload, pf)

    def _actually_send_information_frame(self, payload: bytes, pf=True):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Internal method to send an information frame immediately.

        Args:
            payload (bytes): Data to be sent
            pf (bool): Poll/Final bit value
        """
        header = self.tx_seq << 4 | self.rx_seq
        if pf:
            header |= 0x08
        frame = bytes([0x10, 0x00, len(payload) + 1, header]) + payload
        checksum = (header + sum(payload)) & 0xFF
        frame += bytes([checksum])
        tx_seq = self.tx_seq
        self.outstanding_frames[self.tx_seq] = frame
        self.tx_seq = (self.tx_seq + 1) % 8
        self.transport.write(frame)
        logger.debug(
            f"Information frame sent TxSeq={tx_seq}, self.TxSeq={self.tx_seq}:\n{hexdump(frame, True)}"
        )

    def send_supervisory_frame(self, su_id: int, pf=True):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Send a supervisory frame (RR, REJ, RNR).

        Args:
            su_id (int): Supervisory frame type identifier
            pf (bool): Poll/Final bit value
        """
        header = 0x80 | (su_id << 4) | self.rx_seq
        if pf:
            header |= 0x08
        frame = bytes([0x10, 0x00, 0x01, header, header])
        self.transport.write(frame)

    def send(self, command: BaseCommand, program_id=0, task_id=1):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Send a command using the mail protocol.

        Args:
            command (BaseCommand): Command to send
            program_id (int): Program identifier
            task_id (int): Task identifier
        """
        command_bytes = command.to_bytes()
        payload = bytes([program_id, task_id, *command_bytes])
        self.send_information_frame(payload, pf=True)
        logger.debug(
            f"Command sent: Program ID={program_id}, Task ID={task_id}', "
            f"Payload={hexdump(payload, False)}"
        )

    def send_command(
        self,
        program_id: int,
        task_id: int,
        primitive: int,
        params: bytes,
    ):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Send a raw command using the mail protocol.

        Args:
            program_id (int): Program identifier
            task_id (int): Task identifier
            primitive (int): Command primitive identifier
            params (bytes): Command parameters
        """
        primitive_high = (primitive >> 8) & 0xFF
        primitive_low = primitive & 0xFF
        payload = bytes([program_id, task_id, primitive_low, primitive_high, *params])
        self.send_information_frame(payload, pf=True)
        logger.info(
            f"Command sent: Program ID={program_id}, Task ID={task_id}, "
            f"Primitive=0x{primitive:02x}, Params={hexdump(params, False)}, "
        )

    def handle_frame(self, data):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Process received frame data.
        Handles information frames, supervisory frames, and SABM frames.

        Args:
            data (bytes): Received frame data
        """
        self.temp_buffer += data

        if len(self.temp_buffer) == 0:
            return

        if 0x10 not in self.temp_buffer:
            logger.debug("Buffer contains no header; clearing buffer.")
            self.temp_buffer = b""
            return

        while len(self.temp_buffer) >= 5:
            header = self.temp_buffer[3]
            is_control_frame = header & 0x80
            pf = bool(header & 0x08)
            if not is_control_frame:
                tx_seq = (header >> 4) & 0x07
                rx_seq = header & 0x07
                payload_length = self.temp_buffer[2] - 1
                if len(self.temp_buffer) < 5 + payload_length:
                    logger.debug("Incomplete information frame, waiting for more data.")
                    break

                payload = self.temp_buffer[4 : 4 + payload_length]
                checksum = self.temp_buffer[4 + payload_length]
                if (header + sum(payload)) & 0xFF == checksum:
                    if rx_seq == self.tx_seq:
                        self.rx_seq = (self.rx_seq + 1) % 8
                    if len(payload) >= 4:
                        program_id = payload[0]
                        task_id = payload[1]
                        primitive = (payload[3] << 8) | payload[2]
                        mail_params = payload[4:]
                        logger.info(
                            f"Message Recieved: Program ID={program_id}, Task ID={task_id}, "
                            f"Primitive=0x{primitive:02x}, Params=\n{hexdump(mail_params)}"
                        )
                        self.onMessage(primitive, mail_params)
                    else:
                        logger.info(
                            {"header": header, "payload": hexdump(payload, False)}
                        )
                    self.send_supervisory_frame(0, pf)
                else:
                    logger.debug("Invalid checksum, rejecting frame.")
                    self.send_supervisory_frame(1, pf)
                self.temp_buffer = self.temp_buffer[5 + payload_length :]
            else:
                unnumbered = header >> 6 & 0x01
                su_id = (header >> 4) & 0x03
                if unnumbered:
                    logger.debug(f"SABM frame received. SU_ID={su_id} pf={pf}")
                    self.tx_seq = 0
                    self.rx_seq = 0
                    if pf:
                        self.send_sabm(pf=False)
                    elif self.wait_for_sabm and not self.wait_for_sabm.is_set():
                        self.wait_for_sabm.set()
                else:
                    rx_seq = header & 0x07
                    if len(self.temp_buffer) < 5:
                        logger.debug("Incomplete control frame, waiting for more data.")
                        break
                    if su_id == 0:
                        logger.debug(
                            f"Receive Ready (RR) frame received. RXSeq={rx_seq} self.TxSeq={self.tx_seq}"
                        )
                        if (
                            is_mod8_less(self.tx_seq, rx_seq)
                            and len(self.outstanding_frames) == 1
                            and self.tx_seq != rx_seq
                        ):
                            self.tx_seq = rx_seq
                            logger.debug("Fast forwarding TxSeq to RXSeq.")

                        seqs_to_delete = []
                        for seq in self.outstanding_frames.keys():
                            if is_mod8_less(seq, rx_seq):
                                seqs_to_delete.append(seq)

                        for seq in seqs_to_delete:
                            del self.outstanding_frames[seq]

                        # TODO do we actually need to resend here? feels wrong tbqh.
                        self.resend_outstanding_frames()
                        self.flush_message_queue()

                    elif su_id == 1:
                        logger.info(
                            f"Reject (REJ) frame received. RXSeq={rx_seq} self.TxSeq={self.tx_seq}"
                        )
                        if (
                            is_mod8_less(self.tx_seq, rx_seq)
                            and len(self.outstanding_frames) == 1
                            and self.tx_seq != rx_seq
                        ):
                            self.tx_seq = rx_seq
                            logger.debug("Fast forwarding TxSeq to RXSeq.")

                        seqs_to_delete = []
                        for seq in self.outstanding_frames.keys():
                            if is_mod8_less(seq, rx_seq):
                                seqs_to_delete.append(seq)

                        for seq in seqs_to_delete:
                            del self.outstanding_frames[seq]
                        self.resend_outstanding_frames()
                    elif su_id == 2:
                        logger.debug(
                            f"Receiver Not Ready (RNR) frame received. RXSeq={rx_seq} self.TxSeq={self.tx_seq}"
                        )
                    elif su_id == 3:
                        logger.warning("Unnumbered control frame received.")
                self.temp_buffer = self.temp_buffer[5:]

        if self.temp_buffer:
            logger.debug(f"Leftover bytes in buffer: {hexdump(self.temp_buffer)}")
            if 0x10 not in self.temp_buffer:
                logger.debug("Buffer contains garbage bytes, clearing buffer.")
                self.temp_buffer = b""

    def resend_outstanding_frames(self):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Retransmit all unacknowledged frames in the outstanding frames queue.
        """
        if not self.outstanding_frames:
            return
        logger.debug("Resending outstanding frames.")
        for seq, frame in self.outstanding_frames.items():
            logger.debug(f"Resending frame: TxSeq={seq}")
            self.transport.write(frame)

    async def poll_timer(self):
        """
        AI BULLSHIT WARNING!
        The below comment was hallucinated by a brainless machine, do NOT trust it.
        Please remove this Warning upon review / verification of correctness.
    
        Timer coroutine to handle frame acknowledgment timeouts.
        Triggers retransmission of unacknowledged frames.
        """
        while True:
            now = time.time()
            expired_timers = [
                seq
                for seq, start_time in self.poll_timers.items()
                if now - start_time >= self.timer_duration
            ]
            for seq in expired_timers:
                logger.debug(f"Poll timer expired for TxSeq={seq}, resending frame.")
                frame = self.outstanding_frames.get(seq)
                if frame:
                    self.transport.write(frame)
                    self.poll_timers[seq] = time.time()

            # flush messages that are no longer blocked
            self.flush_message_queue()
            await asyncio.sleep(0.1)
