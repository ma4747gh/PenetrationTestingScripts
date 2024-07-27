import json
from rich.panel import Panel
from rich import box


def cprint(self, string, state):
    if state == 'success':
        self.console.print('\n', end='')
        self.console.print('[bold green][+] {}[/bold green]'.format(string))
    elif state == 'failure':
        self.console.print('\n', end='')
        self.console.print('[bold red][-] {}[/bold red]'.format(string))
    elif state == 'info':
        self.console.print('\n', end='')
        self.console.print('[bold blue][*] {}[/bold blue]'.format(string))
    elif state == 'ack':
        self.console.print('\n', end='')
        self.console.print('[bold yellow][*] {}[/bold yellow]'.format(string))
    else:
        self.console.print('\n', end='')
        self.console.print('[bold {}][*] {}[/bold {}]'.format(state, string, state))


def highlight_json(self, data):
    if isinstance(data, dict):
        return {k: self.highlight_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [self.highlight_json(v) for v in data]
    else:
        return '[#FFF5E1 on #C80036]{}[/#FFF5E1 on #C80036]'.format(data)


def cprint_json(self, data, highlighted=True):
    if highlighted:
        highlighted_data = self.highlight_json(data)
        json_str = json.dumps(highlighted_data, indent=4)
        self.console.print('\n', end='')
        self.console.print(json_str)
    else:
        self.console.print('\n', end='')
        self.console.print(data)


def cprint_panel(self, mode, data):
    if mode == 0:
        panel = Panel(data.decode(), style='#EEEEEE on #373A40', box=box.MINIMAL)
        self.console.print('\n', end='')
        self.console.print(panel)
    else:
        self.console.print('\n', end='')
        self.console.print('[#EEEEEE on #373A40]' + data.decode() + '[/#EEEEEE on #373A40]')
