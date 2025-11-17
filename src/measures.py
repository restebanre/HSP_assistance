# src/measures.py
import pandas as pd
from src.utils import get_soup, parse_sociodemographics, BASE_URL, save_data

URL_MEASURES = f"{BASE_URL}/research/sensitivity-measures/"


def scrape_sensitivity_measures():
    """
    Extrae la tabla de medidas de sensibilidad y aplica expresiones regulares.

    Returns:
        list: Una lista de diccionarios con los datos de las medidas.
    """
    soup = get_soup(URL_MEASURES)
    if not soup:
        return []

    measures_data = []
    # La tabla principal en la página está contenida en una estructura específica
    # Se asume que es la única tabla o la más relevante
    table = soup.find('table')

    if table:
        # Saltar la cabecera (thead)
        rows = table.find('tbody').find_all('tr')

        for row in rows:
            cols = row.find_all(['td', 'th'])
            if len(cols) >= 5:  # Asumiendo que hay 5 columnas (o más) para extraer

                measure_name = cols[0].get_text(strip=True)
                items_count = cols[1].get_text(strip=True)
                # La columna 4 (índice 3) contiene las características sociodemográficas.
                characteristics_text = cols[3].get_text(strip=False)

                # Aplicar RegEx desde utils.py
                ages, genders, diagnoses = parse_sociodemographics(characteristics_text)

                measures_data.append({
                    'Measure Name': measure_name,
                    'Items Count': items_count,
                    'Sociodemographics (Raw)': characteristics_text.replace('\n', ' ').strip(),
                    'Age Groups (RegEx)': ages,
                    'Gender (RegEx)': genders,
                    'Diagnosis (RegEx)': diagnoses,
                })

    return measures_data


