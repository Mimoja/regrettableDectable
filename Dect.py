import asyncio
import serial_asyncio
import uuid
from termcolor import colored
from APIParser import parseMail
from MailProtocol import MailProtocol
from Api.Api import BaseCommand
from Api.Commands import Commands


class DECT:
    """
    Main DECT request-response framework.
    """

    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.pending_requests = {}
        self.protocol = None

    async def connect(self):
        """
        Establish the serial connection and initialize the protocol.
        """
        print(f"Connecting to {self.port} at {self.baudrate} baud...")
        loop = asyncio.get_running_loop()
        transport, protocol = await serial_asyncio.create_serial_connection(
            loop, lambda: MailProtocol(self.received), self.port, self.baudrate
        )
        protocol.transport = transport
        self.protocol = protocol

        while True:
            try:
                evnt = self.protocol.send_sabm()
                await asyncio.wait_for(evnt.wait(), timeout=0.1)
                print("SABM synced successfully.")
                break
            except asyncio.TimeoutError:
                print("Timeout, retrying SABM.")
                continue

    async def command(
        self, command: BaseCommand, program_id=0, task_id=1, max_retries=3, timeout=5
    ):
        event = asyncio.Event()
        primitive = command.primitive()
        self.pending_requests[primitive] = {"event": event, "response": None}

        current_try = 0
        while current_try < max_retries:
            current_try += 1
            print(
                f"[DECT] Sending '{command.__class__.__name__}' (Attempt {current_try}/{max_retries})"
            )

            if self.protocol:
                self.protocol.send(command, program_id, task_id)

            try:
                await asyncio.wait_for(event.wait(), timeout=timeout)
                response = self.pending_requests[primitive]["response"]
                del self.pending_requests[primitive]
                return response
            except asyncio.TimeoutError:
                print(f"[DECT] Timeout for '{command}' (Attempt {current_try})")
                if current_try == max_retries:
                    del self.pending_requests[primitive]
                    print(f"Command '{command}' timed out after {max_retries} attempts")
                    return None

    def received(self, primitive, params):

        response = parseMail(primitive, params)
        if not response:
            print(
                colored(
                    f"[DECT] Unparsed DECT response (Type={Commands(primitive).name})",
                    "red",
                )
            )

        if primitive in self.pending_requests or primitive - 1 in self.pending_requests:
            if primitive - 1 in self.pending_requests:
                primitive = primitive - 1

            print(f"[DECT] Matched response: {response} (Primitive={hex(primitive)})")
            self.pending_requests[primitive]["response"] = response
            self.pending_requests[primitive]["event"].set()
        else:
            print(f"[DECT] Unmatched response: {response} (Primitive={hex(primitive)})")

    async def wait_for(self, primitive, timeout=1):

        if type(primitive) is not list:
            primitive = [primitive]

        event = asyncio.Event()
        for prim in primitive:
            self.pending_requests[prim] = {"event": event, "response": None}

        try:
            await asyncio.wait_for(event.wait(), timeout=timeout)
            response = None
            for prim in primitive:
                if prim in self.pending_requests:
                    if response is None:
                        response = self.pending_requests[prim]["response"]
                    del self.pending_requests[prim]
            return response
        except asyncio.TimeoutError:
            for prim in primitive:
                print(f"[DECT] Timeout for collecting  {Commands(prim).name}")
                del self.pending_requests[prim]
            return None

    async def sync(self, timeout=1.0):
        if not self.pending_requests:
            print("[DECT] No in-flight commands, nothing to wait for.")
            return

        tasks = [
            asyncio.wait_for(req["event"].wait(), timeout=timeout)
            for req in self.pending_requests.values()
        ]

        print(f"[DECT] Waiting for {len(tasks)} in-flight command(s) to complete...")
        await asyncio.gather(*tasks, return_exceptions=True)
