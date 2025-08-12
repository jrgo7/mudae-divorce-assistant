from textual import on, work
from textual.app import App, ComposeResult
from textual.widgets import Header, Button, SelectionList, Label, Footer
from textual_fspicker import FileOpen
from textual.containers import Horizontal, Vertical


class MainApp(App):
    CSS_PATH = "style.tcss"
    
    def __init__(self):
        super().__init__()
        self.title = "Mudae Divorce Assistant"
        self.divorce_list: set[str] = set()
        self.divorce_value: int = 0

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Vertical(
            Horizontal(
                Label("File chosen:"),
                Button("Select file...", id="select-file"),
                classes="vertically-align-middle",
            ),
            Label("$divorce ", id="divorce-list"),
            Label("Divorcing these characters will yield 0 ka.", id="divorce-value"),
            SelectionList(name="Select characters to keep", id="characters-list"),
        )

    @work
    @on(Button.Pressed, "#select-file")
    async def select_file(self) -> None:
        file_chosen = await self.push_screen_wait(FileOpen())
        button = self.query_one("#select-file")
        assert isinstance(button, Button)
        # button.label = str(file_chosen)

        selection_list = self.query_one("#characters-list")
        assert isinstance(selection_list, SelectionList)
        with open(str(file_chosen), "r") as file_pointer:
            lines = file_pointer.readlines()[4:]
        selection_list.add_options([self.parse_line(line) for line in lines])

    def parse_line(self, line: str) -> tuple[str, tuple[str, int]]:
        name, kakera, _ = line.rsplit(maxsplit=2)
        kakera = int(kakera.replace(",", ""))
        return f"{name} - {kakera} ka", (name, kakera)

    @on(SelectionList.SelectionToggled, "#characters-list")
    def toggle_character(self, event: SelectionList.SelectionToggled) -> None:
        name, kakera = event.selection.value
        if name not in self.divorce_list:
            self.divorce_list.add(name)
            self.divorce_value += kakera
        else:
            self.divorce_list.remove(name)
            self.divorce_value -= kakera

        divorce_value_display = self.query_one("#divorce-value")
        assert isinstance(divorce_value_display, Label)
        divorce_value_display.update(
            f"Divorcing these characters will yield {self.divorce_value} ka."
        )

        divorce_list_display = self.query_one("#divorce-list")
        assert isinstance(divorce_list_display, Label)
        divorce_list_display.update("$divorce " + " $ ".join(self.divorce_list))


app = MainApp()
if __name__ == "__main__":
    app.run()
