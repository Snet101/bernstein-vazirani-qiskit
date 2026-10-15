"""Execute from a fresh kernel in the repository, save only on success."""
import argparse
import asyncio
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def main():
    if sys.platform == "win32":
        # ZeroMQ needs add_reader; avoid Proactor's extra selector thread on Windows.
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("bernstein_vazirani.ipynb"))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    notebook = nbformat.read(root / "bernstein_vazirani.ipynb", as_version=4)
    client = NotebookClient(notebook, timeout=180, kernel_name="python3",
                            resources={"metadata": {"path": str(root)}})
    client.execute()
    errors = [output for cell in notebook.cells if cell.cell_type == "code"
              for output in cell.outputs if output.output_type == "error"]
    if errors:
        raise RuntimeError("Notebook has error outputs")
    images = sum("image/png" in output.get("data", {})
                 for cell in notebook.cells if cell.cell_type == "code"
                 for output in cell.outputs)
    if images < 8:
        raise RuntimeError(f"Expected five circuit diagrams and three histograms; got {images} PNGs")
    destination = args.output.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(notebook, destination)
    print(f"PASS: fresh-kernel notebook executed with {images} PNGs; saved to {destination}")


if __name__ == "__main__":
    main()
