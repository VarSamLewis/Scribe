from rich import console
from Scribe.parse_nb import _get_code_cell, _parse_ast
from typing import List, Dict
from openai import OpenAI
from rich.console import Console
from rich.text import Text
from pathlib import Path
import ast
import os
console = Console()
System_Prompt = """\
Role: Code Documenter
Guidelines  
- You will take in asts in order to generate code documentation
- Produce the documenmtation in an md format
"""

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def LLM_Call(string : str):
    try:
        # Parse the code string into an AST first
        tree = ast.parse(string)
        AI_Input = ast.dump(tree, indent=2)
    except SyntaxError:
        # If it's not valid Python code (like SQL), just use the string directly
        AI_Input = f"Code to document:\n{string}"
    try:      
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": System_Prompt},
                {"role": "user", "content": AI_Input}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        console.print(response.choices[0].message.content)
    except Exception as e:
        console.print(f"[bold red]Error calling OpenAI API: {e}[/bold red]")

def document_code_str(string : str):
    if string == "":
        console.print(Text("No code to document.", style="bold red"))
        return " "
    # Fixed: Just pass the string directly to LLM_Call - don't try to iterate over it
    LLM_Call(string)

def process_notebook(notebook_path: str):
    """Process a specific notebook file"""
    code_cells = _get_code_cell(notebook_path, display=False)  
    ast_tree = _parse_ast(code_cells, display=False)
    
    AI_Input = "\n".join([ast.dump(node, indent=2) for node in ast_tree])
    
    LLM_Call(AI_Input)

if __name__ == "__main__":  
    pass