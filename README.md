# AutoTest

Attempt to make AI do something useful. This project parses code into abstract syntax trees (ASTs), converts them into strings, and sends them to OpenAI's API to generate documentation in markdown format.

### How to run tool

'''bash
poetry run Scribe --code "def sum2int(a,b): return a + b"
'''

### To-Do
- Add file writing
- Add code to process entire folders
- Add formatting for documenting 
- Add templates