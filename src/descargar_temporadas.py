import requests
from pathlib import Path
import time

BASE_URL = "https://datahub.io/football/spanish-la-liga/_r/-/{}.csv"
OUTPUT_DIR = Path("data/raw/results")


def generar_codigos_temporada(anio_inicio=1993, anio_fin=2025):
    codigos = []
    for anio in range(anio_inicio, anio_fin + 1):
        actual = anio % 100
        siguiente = (anio + 1) % 100
        codigos.append(f"season-{actual:02d}{siguiente:02d}")
    return codigos


def descargar_temporadas():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for codigo in generar_codigos_temporada():
        destino = OUTPUT_DIR / f"{codigo}.csv"

        if destino.exists():
            print(f"{codigo}: ya existe, se omite")
            continue

        url = BASE_URL.format(codigo)
        respuesta = requests.get(url, timeout=15)

        if respuesta.status_code == 200:
            destino.write_bytes(respuesta.content)
            print(f"{codigo}: descargada ({len(respuesta.content)} bytes)")
        else:
            print(f"{codigo}: falló con status {respuesta.status_code}")

        time.sleep(0.5)  # pausa corta entre requests, buena práctica con el servidor de otros


if __name__ == "__main__":
    descargar_temporadas()
