# src/measures.py
import pandas as pd
from src.utils import get_soup, BASE_URL, save_data

URL_MEASURES = f"{BASE_URL}/research/sensitivity-measures/"


def scrape_sensitivity_measures() -> pd.DataFrame:
    """
    Extrae la tabla de medidas de sensibilidad y aplica expresiones regulares.

    Returns:
        df: Dataframe con los datos de las medidas.
    """
    soup = get_soup(URL_MEASURES)
    if not soup:
        return pd.DataFrame([])

    # measures_data = []


    # La tabla principal es la unica exitente en la página y porta
    # un id especifico en su estructura que nos ayuda a identificarla
    # Nota: Encabezado y cuerpo de la tabla no estan embedidos conjuntamente
    # en la estructura de la tabla.

    table = soup.find('table', {"id": "tablepress-1"})
    if not table:
        raise ValueError("No se encontro tabla de medidas")

    # Extraemos primeramente los encabezados
    headers = []
    thead = soup.find("thead")
    if thead:
        header = thead.find("tr")
        for th in header.find_all("th"):
            span = th.select_one("span.dt-column-title")
            if span:
                labels = span.get_text(strip=True)
            else:
                labels = th.get_text(strip=True)
            print(type(labels))
            print(labels)
            headers.append(labels)

    # Extraemos las fiilas de datos
    rows = []
    tbody = table.find("tbody")
    if tbody:
        for tr in tbody.find_all("tr"):
            row = []
            for td in tr.find_all("td"):
                # Pulimos el contenido de las celdas
                # y eliminamos saltos de linea
                cell = td.get_text(strip=True)
                cell = " ".join(cell.split())
                row.append(cell)
            rows.append(row)

    # Formateamos los datos en DataFrame
    df = pd.DataFrame(rows, columns=headers)
    return df


