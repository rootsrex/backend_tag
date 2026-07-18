import time
from html.parser import HTMLParser

import requests

PAGE_URL   = "https://www.ecuadorlegalonline.com/consultas/registro-civil/consultar-cedulas/"
API_CEDULA = "https://www.ecuadorlegalonline.com/modulo/consultar-cedula.php"
API_NOMBRE = "https://apps.ecuadorlegalonline.com/modulo/consultar-cedulanombre.php"

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
)

BASE_HEADERS = {
    "User-Agent": UA,
    "Accept-Language": "es-EC,es;q=0.9,en;q=0.8",
}


class TableParser(HTMLParser):
    """Extrae filas de una tabla HTML como listas de texto."""
    def __init__(self):
        super().__init__()
        self.rows = []
        self._in_row = False
        self._cells = []
        self._cell_buf = []

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._in_row = True
            self._cells = []
        elif tag == "td" and self._in_row:
            self._cell_buf = []

    def handle_endtag(self, tag):
        if tag == "td":
            self._cells.append(" ".join(self._cell_buf).strip())
        elif tag == "tr" and self._in_row:
            self.rows.append(self._cells[:])
            self._in_row = False

    def handle_data(self, data):
        if self._in_row:
            t = data.strip()
            if t:
                self._cell_buf.append(t)


def _session() -> requests.Session:
    """Crea sesión con la página principal para obtener cookies."""
    s = requests.Session()
    s.get(PAGE_URL, headers={**BASE_HEADERS, "Referer": "https://www.google.com/"}, timeout=15)
    return s


def buscar_por_cedula(cedula: str) -> list[dict]:
    s = _session()
    r = s.post(
        API_CEDULA,
        data={"name": cedula, "tipo": "I"},
        headers={
            **BASE_HEADERS,
            "Referer": PAGE_URL,
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
        },
        timeout=15,
    )
    r.raise_for_status()
    body = r.text.strip()
    if not body:
        return []

    parser = TableParser()
    parser.feed(body)
    resultados = []
    for row in parser.rows:
        resultados.append({
            "cedula": row[0].strip() if len(row) > 0 else "-",
            "nombre": row[1].strip() if len(row) > 1 else "-",
        })
    return resultados


def buscar_por_nombre(nombre: str) -> list[dict]:
    ts = int(time.time() * 1000)
    r = requests.get(
        API_NOMBRE,
        params={"nombres": nombre.upper(), "_": ts},
        headers={
            **BASE_HEADERS,
            "Referer": PAGE_URL,
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
        },
        timeout=15,
    )
    r.raise_for_status()
    body = r.text.strip()
    if not body or body in ("[]", "null", ""):
        return []

    datos = r.json()
    resultados = []
    for item in datos:
        defun = item.get("fechaDefuncion")
        resultados.append({
            "cedula": item.get("identificacion", "-"),
            "nombre": item.get("nombreCompleto", "-"),
            "estado": f"Fallecido ({defun})" if defun else "Activo",
        })
    return resultados
