from textual.app import App, ComposeResult
from textual.widgets import Input, Label
from textual.widget import Widget

class InputWithLabel(Widget):
    """An input with a label."""

    def __init__(self, input_label: str, password=False) -> None:
        self.input_label = input_label
        self.is_password = password
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label(self.input_label, style="input-with-label Label")
        if self.is_password:
            yield Input(password=True, style="input-with-label Input")
        else:
            yield Input(style="input-with-label Input")

class UserRegistrationForm(Widget):
    def compose(self) -> ComposeResult:
        yield InputWithLabel("Nombre", style="input-with-label")
        yield InputWithLabel("Correo Electrónico", style="input-with-label")
        yield InputWithLabel("Contraseña", password=True, style="input-with-label")

class UserRegistrationApp(App):
    async def on_load(self, event):
        await self.load_styles("styles.css")
        self.view.dock(UserRegistrationForm(style="user-registration-form"))

if __name__ == "__main__":
    app = UserRegistrationApp()
    app.run()
