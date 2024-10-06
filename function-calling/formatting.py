# Code from here: https://github.com/PrefectHQ/marvin/blob/main/src/marvin/beta/assistants/formatting.py

from typing import Any

from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

class Message:
    def __init__(self, role, content=None, function_call=None):
        self.role = role
        self.content = content
        self.function_call = function_call

def create_panel(content: Any, title: str, color: str):
    return Panel(
        content,
        title=f"[bold]{title}[/]",
        title_align="left",
        subtitle_align="right",
        border_style=color,
        box=box.ROUNDED,
        width=100,
        expand=True,
        padding=(1, 2),
    )

def format_message(message: Message) -> Panel:
    role_colors = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "function": "magenta",
    }
    content = []

    for item in message.content:
        if item.type == "text":
            content.append(item.text.value)

    # Create the panel for the message
    panel = create_panel(
        Markdown("\n\n".join(content)),
        title=message.role.capitalize(),
        color=role_colors.get(message.role, "red"),
    )
    return panel


def pprint_message(message: Message):
    """
    Pretty-prints a single message using the rich library, highlighting the
    speaker's role, the message text, any available images, and the message
    timestamp in a panel format.

    Args:
        message (Message): A message object
    """
    console = Console()
    panel = format_message(message)
    console.print(panel)


def pprint_messages(messages: list[Message]):
    """
    Iterates over a list of messages and pretty-prints each one.

    Messages are pretty-printed using the rich library, highlighting the
    speaker's role, the message text, any available images, and the message
    timestamp in a panel format.

    Args:
        messages (list[Message]): A list of Message objects to be
            printed.
    """
    for message in sorted(messages, key=lambda m: m.created_at):
        pprint_message(message)
