# src/measures.py

from src.utils import *

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
        header = thead.find_all("th")
        # print(header)
        for th in header:
            if th:
                headers.append(th.text.strip())
                print(headers)
    else:
        print("Atencion: Alguna etiqueta de la cabecra \
        no ha podido ser recuperarda")
        # Tabla tiene 5 columnas
        headers = [f'Column {i+1}' for i in range(5)]
        # print(headers)

    # Extraemos las fiilas de datos
    table_data = []
    if table.find("tbody"):
        rows = table.find("tbody").find_all("tr")
        for row in rows:
            row_data = []
            cells = row.find_all("td")
            for cell in cells:
                # Pulimos el contenido de las celdas
                # y eliminamos saltos de linea y multiples
                # espacios
                cell = cell.text.strip()
                cell = cell.replace('\n', ' ')
                cell = cell.replace('  ', ' ')
                row_data.append(cell)
            table_data.append(row_data)

    # Formateamos los datos en DataFrame
    df = pd.DataFrame(table_data, columns=headers)
    return df


