from rich import console
from parse_nb import _get_code_cell, _parse_ast, _extract_modules, _write_tree_to_file
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

"""

def LLM_Call(string : str):
    if string == "":
        console.print(Text("No code to document.", style="bold red"))
        return " "

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    AI_Input = "\n".join([ast.dump(node, indent=2) for node in string])

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
    
    

if __name__ == "__main__":
    notebook_path = r"C:\Users\samle\OneDrive\Documents\sample_de_nb.ipynb"
    code_cells = _get_code_cell(notebook_path, display=False)  
    ast_tree = _parse_ast(code_cells, display=False)
    modules = _extract_modules(ast_tree, display=False)
    _write_tree_to_file(ast_tree, "ast_tree.txt")
    LLM_Call(ast_tree)

