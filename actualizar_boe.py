import urllib.request
from bs4 import BeautifulSoup
import datetime

url = "https://boe.es"

cabeceras = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.9'
}

req = urllib.request.Request(url, headers=cabeceras)
with urllib.request.urlopen(req) as response:
    html = response.read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, 'html.parser')
contenido = soup.find('div', id='textoxslt')

lineas = [
    "# Estatuto de los Trabajadores (Texto Consolidado BOE)",
    f"*Última comprobación automática: {datetime.date.today().isoformat()}*\n"
]

if contenido:
    for elem in contenido.find_all(['h4', 'h5', 'p']):
        texto = elem.get_text(" ", strip=True)
        if not texto:
            continue
        if elem.name in ['h4', 'h5']:
            lineas.append(f"\n## {texto}\n")
        else:
            lineas.append(texto + "\n")
else:
    raise ValueError("No se encontró el bloque de texto en la página del BOE.")

with open("ESTATUTO_TRABAJADORES.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lineas))
