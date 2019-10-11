import re
import os
from textwrap import wrap, indent

home = os.environ['HOME']

# Group 0 is the full match, which will contain the docstring.
# Group 1 is always blank for some reason, gets the space before the end of the
# block comment
# Group 2 is the function name
c_com = re.compile(r"\/\*(\*(?!\/)|[^*])*\*\/\nnvmlReturn_t DECLDIR (\w+)")
py_func = re.compile(r"def (\w+)\(.*\):")
name_regex = re.compile(r"(\w+)\s+(.*)")

with open(os.path.join(home, 'repos/NVIDIA/nvidia-settings/src/nvml.h')) as f:
    src = f.read()

with open(os.path.join(home, 'repos/fbcotter/py3nvml/py3nvml/py3nvml.py')) as f:
    py_scr = f.read()

def format_str(s):
    s = s.replace('/*', '')
    s = s.replace('*/', '')
    s = s.replace('*', '')
    lines = s.split('\n')

    # Drop the last and first lines as they are blank contains the function def
    lines = lines[1:-1]

    # Strip whitespace
    for i in range(len(lines)):
        lines[i] = lines[i].lstrip()

    # Get paragraphs
    docstring = []
    p = ''
    params = False
    for i in range(len(lines)):
        if lines[i].isspace() or lines[i] == '':
            docstring.append('\n'.join(wrap(p, 76)))
            docstring.append('')
            p = ''
        elif lines[i].startswith(r'\note'):
            if p != '':
                docstring.append('\n'.join(wrap(p, 76)))
                docstring.append('')
            docstring.append('Note:')
            p = lines[i][6:]
        elif lines[i].startswith('@param'):
            if p != '':
                docstring.append('\n'.join(wrap(p, 76)))
                docstring.append('')
            if not params:
                docstring.append('Inputs:')
            p = lines[i][6:].lstrip()
        elif lines[i].startswith('@return'):
            if p != '':
                docstring.append('\n'.join(wrap(p, 76)))
            docstring.append('Raises:')
            p = ''
        elif lines[i].startswith(r'- \ref'):
            p += lines[i][7:]
        else:
            p = p + lines[i]

    return '\n'.join(docstring)

func_docstrings = {}
matches = c_com.finditer(src)
for i, match in enumerate(matches):
    func_docstrings[match.group(2)] = match.group(0)  # format_str(match.group(0))
    #  func_docstrings[match.group(2)] = format_str(match.group(0))

matches = py_func.finditer(py_scr)
out_src = py_scr[:]
for match in matches:
    print(match.group(1))
    if match.group(1) in func_docstrings.keys():
        out_src = out_src.replace(
            match.group(0), match.group(0) +
            indent('\nr"""\n' + func_docstrings[match.group(1)] + '\n"""', '    '))
with open('out.py', 'w') as f:
    f.write(out_src)

