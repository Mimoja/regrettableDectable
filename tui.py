from rich.console import Console
from rich.prompt import Prompt
from typing import Optional
from MailProtocol import MailProtocol
from ppApi import PpApi, ApiPpUle


async def tui(protocol: Optional[MailProtocol] = None):
    """
    Minimal TUI for controlling LEDs.
    """
    console = Console()
    console.print("[bold green]LED Controller[/bold green]")

    while True:
        try:
            action = Prompt.ask(
                "\nWhat would you like to do?",
                choices=["on", "off", "exit"],
                default="exit",
            )
            if action == "exit":
                console.print("[bold red]Exiting...[/bold red]")
                break

            if protocol:
                protocol.send_command(
                    program_id=0,
                    task_id=1,
                    primitive=PpApi.API_PP_ULE_HAL_SET_PORT_REQ,
                    params=[ApiPpUle.API_PP_ULE_GPIO_LED3, 1],
                )
            else:
                console.print("[bold red]Protocol not initialized.[/bold red]")

        except ValueError:
            console.print("[bold red]Invalid input. Please try again.[/bold red]")
