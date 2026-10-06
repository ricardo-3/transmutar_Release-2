"""Consulta el HTML público de Compara Pix y genera un sitio estático. Sin API."""
import argparse
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re
import shutil
from urllib.request import Request, urlopen

SOURCE = "https://comparapix.ar/"
ROOT = Path(__file__).resolve().parents[1]


class QuotesParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.cells = None
        self.cell = None
        self.name = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "tr":
            self.cells, self.name = [], None
        elif tag == "td" and self.cells is not None:
            self.cell = []
        elif self.cell is not None and not self.cells and attrs.get("title"):
            self.name = attrs["title"]

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag == "td" and self.cell is not None:
            self.cells.append(" ".join(self.cell))
            self.cell = None
        elif tag == "tr" and self.cells is not None:
            if self.name and len(self.cells) >= 2:
                match = re.search(r"\$\s*([\d.]+,\d{2})", self.cells[1])
                if match:
                    try:
                        rate = Decimal(match[1].replace(".", "").replace(",", "."))
                    except InvalidOperation:
                        rate = Decimal(0)
                    if rate.is_finite() and rate > 0:
                        self.rows.append((self.name.strip(), rate))
            self.cells, self.cell = None, None


def extract_quotes(html):
    parser = QuotesParser()
    parser.feed(html)
    rows, seen = [], set()
    for name, rate in parser.rows:
        if name not in seen:
            rows.append((name, rate))
            seen.add(name)
        if len(rows) == 5:
            return rows
    raise ValueError("No se encontraron cinco cotizaciones válidas. No se publican datos incompletos.")


def replace_block(html, label, content):
    start, end = f"<!-- {label}:START -->", f"<!-- {label}:END -->"
    if html.count(start) != 1 or html.count(end) != 1:
        raise ValueError(f"Faltan los marcadores de {label}.")
    return html.split(start)[0] + start + "\n" + content + "\n" + end + html.split(end)[1]


def render_snapshot(html, rows, consulted_at):
    buttons = []
    for name, rate in rows:
        label = format(rate, ",.2f").replace(",", "_").replace(".", ",").replace("_", ".")
        buttons.append(
            '<li><button type="button" class="arb-quote" data-pix-rate="'
            + str(rate) + '" aria-label="Usar la cotización de ' + escape(name, quote=True)
            + '"><span>' + escape(name) + '</span><strong>$ ' + label + '</strong></button></li>'
        )
    html = replace_block(html, "PIX-ROWS", "\n".join(buttons))
    stamp = consulted_at.isoformat(timespec="seconds").replace("+00:00", "Z")
    # Siempre se informa cuándo se consultó la página, no cuándo actualizó la fuente.
    text = consulted_at.strftime("%d/%m/%Y %H:%M UTC")
    return replace_block(html, "PIX-TIME", '<time id="arb-pix-time" datetime="' + stamp + '">Consultado: ' + text + '</time>')


def main():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("--output", type=Path, default=ROOT / "_site")
    args_parser.add_argument("--input", type=Path, help="HTML local para pruebas, sin consulta de red")
    args = args_parser.parse_args()
    if args.input:
        source = args.input.read_text(encoding="utf-8")
    else:
        request = Request(SOURCE, headers={"User-Agent": "Arbolito-BR/1.0 (+https://ricardo-3.github.io/Arbolito-BR/)"})
        with urlopen(request, timeout=30) as response:
            source = response.read(2_000_001)
            if len(source) > 2_000_000:
                raise ValueError("Respuesta demasiado grande.")
            source = source.decode("utf-8")
    rows = extract_quotes(source)
    html = render_snapshot((ROOT / "index.html").read_text(encoding="utf-8"), rows, datetime.now(timezone.utc))
    output = args.output.resolve()
    if output == ROOT:
        raise ValueError("El destino debe ser una carpeta distinta de la fuente.")
    output.mkdir(parents=True, exist_ok=True)
    (output / "index.html").write_text(html, encoding="utf-8")
    (output / ".nojekyll").touch()
    if (ROOT / "imagenes").exists():
        shutil.copytree(ROOT / "imagenes", output / "imagenes", dirs_exist_ok=True)
    if (ROOT / "CNAME").exists():
        shutil.copy2(ROOT / "CNAME", output / "CNAME")
    print("Sitio generado con cinco cotizaciones. Consulta:", datetime.now(timezone.utc).isoformat())


if __name__ == "__main__":
    main()
