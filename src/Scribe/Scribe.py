from rich import console
from Scribe.parse_files import _get_nb_code, _parse_ast, _get_code_file
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

def process_file(file_path : str):
    
    if file_path.endswith('.ipynb') and Path(file_path).exists():
        code_cells = _get_nb_code(file_path, display=False)  
        ast_tree = _parse_ast(code_cells, display=False)
    
        AI_Input = "\n".join([ast.dump(node, indent=2) for node in ast_tree])

    elif file_path.endswith('.py') and Path(file_path).exists():
        AI_Input = _get_code_file(file_path)
    
    LLM_Call(AI_Input)

if __name__ == "__main__":  
    pass