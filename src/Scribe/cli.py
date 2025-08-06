import typer
from typing import Optional
from pathlib import Path
from Scribe.Scribe import document_code_str, process_file, write_documentation, write_ast

app = typer.Typer(
    name='scribe',
    help="CLI AI tool to auto document code",
    rich_markup_mode="rich"
)

@app.command("doc")
def doc_command(
    code: Optional[str] = typer.Option(None, "--code", "-c", help="Code to document"),
    file: Optional[str] = typer.Option(None, "--file", "-f", help="Path to file to document"),
    document_write: Optional[str] = typer.Option(None, "--doc-write", "-w", help="Path to write documentation"),
    ast_write: Optional[str] = typer.Option(None, "--ast-write", "-a", help="Path to write AST output"),
):
    """Generate documentation for code or files."""
    
    if not code and not file:
        typer.echo("Error: You must provide either --code or --file", err=True)
        typer.echo("Examples:")
        typer.echo('  scribe doc --code "def hello(): pass"')
        typer.echo('  scribe doc --file myfile.py')
        raise typer.Exit(1)
    
    content = None

    if file:
        if Path(file).exists():
            typer.echo(f"Processing file: {file}")
            content = process_file(file)
        else:
            typer.echo(f"Error: File {file} not found", err=True)
            raise typer.Exit(1)
    elif code:
        typer.echo("Processing code input...")
        content = document_code_str(code)

    if document_write and content:
        write_documentation(content, document_write)
    if ast_write and content:
        write_ast(content, ast_write)


if __name__ == "__main__": 
    app()