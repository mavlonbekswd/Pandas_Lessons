"""Tiny helper to build valid .ipynb notebooks from a list of (kind, text) cells."""
import nbformat as nbf


def build_notebook(cells, path):
    """cells: list of ('md', text) or ('code', text). Writes a v4 notebook."""
    nb = nbf.v4.new_notebook()
    out = []
    for kind, text in cells:
        if kind == "md":
            out.append(nbf.v4.new_markdown_cell(text))
        elif kind == "code":
            out.append(nbf.v4.new_code_cell(text))
        else:
            raise ValueError(kind)
    nb["cells"] = out
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
    }
    with open(path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    return path
