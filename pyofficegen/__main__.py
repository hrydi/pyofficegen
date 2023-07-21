import typer
from pyofficegen.commands import excel

app = typer.Typer()
app.add_typer(
  typer_instance=excel.app,
  name="excel"
)

if __name__ == "__main__":
  app()