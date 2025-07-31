import typer
from typing import Optional
from pathlib import Path
from Scribe.Scribe import document_code_str, process_notebook  # Import both functions

app = typer.Typer(
    name='scribe',
    help="CLI AI tool to auto document code",
    rich_markup_mode="rich"
)

@app.command()
def doc(
    input_data: str = typer.Argument(..., help="Code to document or path to .ipynb file"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file for documentation")
):
    """Generate documentation for code or Jupyter notebooks."""
    
    # Check if it's a notebook file
    if input_data.endswith('.ipynb') and Path(input_data).exists():
        typer.echo(f"Processing notebook: {input_data}")
        process_notebook(input_data)
    else:
        # Treat as raw code
        typer.echo("Processing code input...")
        document_code_str(input_data)

@app.command()
def notebook(
    path: str = typer.Argument(..., help="Path to Jupyter notebook"),
):
    """Process a specific Jupyter notebook file."""
    if not Path(path).exists():
        typer.echo(f"Error: File {path} not found", err=True)
        raise typer.Exit(1)
    
    if not path.endswith('.ipynb'):
        typer.echo("Error: File must be a .ipynb file", err=True)
        raise typer.Exit(1)
    
    process_notebook(path)

if __name__ == "__main__": 
    app()