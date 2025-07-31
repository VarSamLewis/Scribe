import typer
from typing import Optional
from pathlib import Path
from Scribe.Scribe import document_code_str, process_file  

app = typer.Typer(
    name='scribe',
    help="CLI AI tool to auto document code",
    rich_markup_mode="rich"
)

@app.command("doc")
def doc_command(
    code: Optional[str] = typer.Option(None, "--code", "-c", help="Code to document"),
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Path to file to document"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file for documentation")
):
    """Generate documentation for code or files."""
    
    if not code and not file:
        typer.echo("Error: You must provide either --code or --file", err=True)
        typer.echo("Examples:")
        typer.echo('  scribe doc --code "def hello(): pass"')
        typer.echo('  scribe doc --file myfile.py')
        raise typer.Exit(1)
    
    if file:
        if Path(file).exists():
            typer.echo(f"Processing file: {file}")
            process_file(file)
        else:
            typer.echo(f"Error: File {file} not found", err=True)
            raise typer.Exit(1)
    
    if code:
        typer.echo("Processing code input...")
        document_code_str(code)


if __name__ == "__main__": 
    app()