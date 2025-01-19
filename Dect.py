import asyncio
import serial_asyncio
import uuid
from termcolor import colored
from APIParser import parseMail
from MailProtocol import MailProtocol
from Api.Api import BaseCommand
from Api.Commands import Commands

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DECT")


class DECT:
    """ 
    Main DECT request-response framework.
    Handles communication with DECT devices over serial connection.
    """ 


    def __init__(self, port, baudrate):
        """ 

        Initialize a new DECT connection.

        Args:
            port (str): Serial port to connect to
            baudrate (int): Baud rate for serial communication
        """ 

        self.port = port
        self.baudrate = baudrate
        self.pending_requests = {}
        self.protocol = None

    async def connect(self):
        """ 

        Establish the serial connection and initialize the protocol.
        Attempts to synchronize SABM (Set Asynchronous Balanced Mode) with retries.

        Raises:
            asyncio.TimeoutError: If SABM synchronization fails repeatedly
        """ 

        logger.info(f"Connecting to {self.port} at {self.baudrate} baud...")
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
                logger.debug("SABM synced successfully.")
                break
            except asyncio.TimeoutError:
                logger.info("Timeout, retrying SABM.")
                continue

    async def command(
        self, command: BaseCommand, program_id=0, task_id=1, max_retries=3, timeout=5
    ):
        """ 


        Send a command to the DECT device and wait for response.

        Args:
            command (BaseCommand): Command to send
            program_id (int): Program identifier
            task_id (int): Task identifier
            max_retries (int): Maximum number of retry attempts
            timeout (int): Timeout in seconds for each attempt

        Returns:
            The command response if successful, None if timed out
        """ 

        event = asyncio.Event()
        primitive = command.primitive()
        self.pending_requests[primitive] = {"event": event, "response": None}

        current_try = 0
        while current_try < max_retries:
            current_try += 1
            logger.debug(
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
                logger.debug(f"[DECT] Timeout for '{command}' (Attempt {current_try})")
                if current_try == max_retries and timeout > 0:
                    del self.pending_requests[primitive]
                    logger.warning(
                        f"Command '{command}' timed out after {max_retries} attempts"
                    )
                    return None

    def received(self, primitive, params):
        """ 

        Handle received DECT responses.
        Matches responses with pending requests and processes them.

        Args:
            primitive: The primitive type of the response
            params: Parameters received with the response
        """ 

        response = parseMail(primitive, params)
        if not response:
            logger.warning(
                colored(
                    f"[DECT] Unparsed DECT response (Type={Commands(primitive).name})",
                    "red",
                )
            )

        if (
            primitive not in self.pending_requests
            and primitive - 1 in self.pending_requests
        ):
            primitive = primitive - 1

        if primitive in self.pending_requests:

            logger.debug(
                f"[DECT] Matched response: {response} (Primitive={Commands(primitive).name})"
            )
            self.pending_requests[primitive]["response"] = response
            self.pending_requests[primitive]["event"].set()
        else:
            logger.debug(
                f"[DECT] Unmatched response: {response} (Primitive={Commands(primitive).name})"
            )

    async def wait_for(self, primitive, timeout=5):
        """ 

        Wait for a specific primitive or list of primitives to be received.

        Args:
            primitive (Union[int, List[int]]): Primitive(s) to wait for
            timeout (int): Timeout in seconds

        Returns:
            The response if received within timeout, None otherwise
        """ 

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
                logger.warning(f"[DECT] Timeout for collecting  {Commands(prim).name}")
                del self.pending_requests[prim]
            return None

    async def sync(self, timeout=1.0):
        """ 

        Wait for all pending requests to complete.

        Args:
            timeout (float): Timeout in seconds for each pending request

        Note:
            This method will wait for all in-flight commands to either complete or timeout.
        """ 

        if not self.pending_requests:
            logger.info("[DECT] No in-flight commands, nothing to wait for.")
            return

        tasks = [
            asyncio.wait_for(req["event"].wait(), timeout=timeout)
            for req in self.pending_requests.values()
        ]

        logger.debug(
            f"[DECT] Waiting for {len(tasks)} in-flight command(s) to complete..."
        )
        await asyncio.gather(*tasks, return_exceptions=True)
