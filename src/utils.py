# src/utils.py
import requests
import time
import re
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict, Optional
from pathlib import Path

global df_researchers

BASE_URL = "https://sensitivityresearch.com"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

DATA_DIR = Path("data")

def get_soup(url, delay=2):
    """Realiza una petición HTTP con un delay ético y devuelve un objeto BeautifulSoup."""
    # print(f"-> Solicitando URL: {url}")
    time.sleep(delay)  # pausa entre requests para no sobrecargar el servidor

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Lanza un error para códigos de estado HTTP malos
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error al solicitar {url}: {e}")
        return None

def write_directory(directory: List[dict]):
    """Guarda una lista de diccionarios en un archivo CSV."""
    return pd.DataFrame(directory)

def get_researcher_url_by_index(index_nb: int, df: pd.DataFrame) -> str:
    """Guarda una lista de diccionarios en un archivo CSV."""
    #global df_researchers
    researcher_url = df.loc[index_nb, "Profile URL"]
    return researcher_url


def parse_sociodemographics(text):
    """
    Aplica expresiones regulares para extraer edad, género y posibles diagnósticos.

    Args:
        text (str): La cadena de texto de la columna de características sociodemográficas.

    Returns:
        tuple: (edad_str, genero_str, diagnosticos_str)
    """
    text = str(text).upper() if text else ""

    # 1. Edades: Busca patrones como XX-YY YEARS, >XX, o XX to YY
    age_pattern = re.compile(r'(\d+[-\s]?\d+\s?YEARS?|\>\s?\d+|\d+\s?TO\s?\d+)', re.IGNORECASE)
    ages = "; ".join(age_pattern.findall(text))

    # 2. Género: Busca MALE, FEMALE, WOMEN, MEN
    gender_pattern = re.compile(r'(MALE|FEMALE|WOMEN|MEN|NON-BINARY)', re.IGNORECASE)
    genders = "; ".join(gender_pattern.findall(text))

    # 3. Diagnósticos comunes (Ejemplo): Busca HSP, ADHD, ASD, PTSD, etc.
    diag_pattern = re.compile(r'(HSP|SPS|ADHD|ASD|AUTISM|ANXIETY|DEPRESSION|PTSD|NEURODIVERS(E|ITY))', re.IGNORECASE)
    diagnoses = "; ".join(set(diag_pattern.findall(text)))  # Usar set para únicos

    return ages, genders, diagnoses


def save_data(data: List[Dict], filename):
    """Guarda una lista de diccionarios en un archivo CSV."""
    df = pd.DataFrame(data)
    df.to_csv(f"data/{filename}", index=False, encoding='utf-8')
    print(f"\nDatos guardados exitosamente en data/{filename}")
    return df