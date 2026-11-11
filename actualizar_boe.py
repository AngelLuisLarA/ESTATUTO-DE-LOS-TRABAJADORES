import urllib.request
import xml.etree.ElementTree as ET
import datetime

base = "https://boe.es"
ruta = "legislacion-consolidada/id/BOE-A-2015-11430/texto"
URL_BOE = base + ruta

cabeceras = {
    'Accept': 'application/xml',
    'User-Agent': 'Mozilla/5.0'
}

req = urllib.request.Request(URL_BOE, headers=cabeceras)
with urllib.request.urlopen(req) as response:
    xml_data = response.read()

root = ET.fromstring(xml_data)
lineas = [
    "# Estatuto de los Trabajadores (Texto Consolidado BOE)",
    f"*Última comprobación automática: {datetime.date.today().isoformat()}*\n"
]

for bloque in root.findall(".//bloque"):
    titulo = bloque.attrib.get("titulo", "")
    if titulo:
        lineas.append(f"\n## {titulo}\n")
    
    versiones = bloque.findall("version")
    if versiones:
        ultima_version = versiones[-1]
        for parrafo in ultima_version.findall(".//p"):
            texto = "".join(parrafo.itertext()).strip()
            if texto:
                lineas.append(texto + "\n")

with open("ESTATUTO_TRABAJADORES.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lineas))
