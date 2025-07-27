import json
import ast
import logging
import types
from typing import List, Dict

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def _get_code_cell(folder_path: str, display : bool = False) -> List[str]:

    try:
        with open(folder_path, "r") as f:
            notebook = json.load(f)
    except Exception as e:
        logging.error(f"Error loading notebook: {e}")
        raise
            
    try:    
        code_cells = [cell['source'] for cell in notebook['cells'] if cell['cell_type'] == 'code']
        if display:
            for i, code in enumerate(code_cells):
                print(f"Code Cell {i + 1}:\n{''.join(code)}\n")

        return code_cells
    except Exception as e:
        logging.error(f"Error extracting code cells: {e}")
        raise

def _extract_modules(trees: List[ast.AST], display: bool = False) -> Dict[int, List[str]]:
    extracted = {}

    for i, tree in enumerate(trees):
        modules = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    modules.add(alias.name)
                    logging.debug(f"Found import: {alias.name}")

            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module)
                logging.debug(f"Found import-from: {node.module}")
                if display:
                    print(f"Found ImportFrom in Cell {i + 1}: {node.module}")

        if display:
            print(f"Extracted modules from Cell {i + 1}: {modules}")

        extracted[i] = sorted(modules)

    return extracted

def _parse_ast(cells : List[str], display : bool= False  ) -> Dict:
    trees = []
    for i, code in enumerate(cells):
        try:
            tree = ast.parse("\n".join(code))
            trees.append(tree)
            logging.info(f"Successfully parsed code cell {i + 1} into AST.")
            if display:
                print(ast.dump(tree, indent=4)) 
        except SyntaxError as e:
            logging.error(f"Syntax error in code cell {i + 1}: {e}")
        except Exception as e:
            logging.error(f"Error parsing code cell {i + 1}: {e}")
            raise

    return trees

def _write_tree_to_file(trees: List[ast.AST], file_path: str = "tree.txt") -> None:
    try:
        with open(file_path, "w") as f:
            for i, tree in enumerate(trees):
                f.write(ast.dump(tree, indent=4))
        logging.info(f"All AST trees written to {file_path}.")
    except Exception as e:
        logging.error(f"Error writing AST trees to file: {e}")
        raise


if __name__ == "__main__":
    pass
