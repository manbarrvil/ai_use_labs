import pymupdf4llm
import sys
from pathlib import Path


def pdf_to_markdown(pdf_path: str, output_path: str = None):
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        print(f"Error: no se encontró el archivo '{pdf_path}'")
        sys.exit(1)

    if output_path is None:
        output_path = pdf_path.with_suffix(".md")
    else:
        output_path = Path(output_path)

    fig_dir = (output_path.parent / f"{pdf_path.stem}_fig").resolve()
    fig_dir.mkdir(exist_ok=True)

    md_text = pymupdf4llm.to_markdown(str(pdf_path.resolve()), write_images=True, image_path=str(fig_dir))

    output_path.write_text(md_text, encoding="utf-8")
    print(f"Convertido: {pdf_path} -> {output_path}")
    print(f"Figuras:    {fig_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python pdf_to_markdown.py <archivo.pdf> [salida.md]")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_md = sys.argv[2] if len(sys.argv) > 2 else None
    pdf_to_markdown(input_pdf, output_md)
