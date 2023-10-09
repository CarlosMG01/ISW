from textual.app import App, ComposeResult
from textual.widgets import Static, Button
from textual.containers import Container, Horizontal

class WidgetApp(App):
  CSS_PATH = "app.tcss"

  def compose(self) -> ComposeResult:
        yield Container(
                Horizontal(
                    Button("d", classes= "button"),
                    Static("Título", classes= "tittle"),
                    Button("usuario", classes= "button")
                )
                )

  def on_button_pressed(self, event: Button.Pressed) -> None:
        self.exit(event.button)    


if __name__ == "__main__":
    app = WidgetApp()
    app.run()

