# src/utils.py
import requests
import time
import re
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict, Optional
from pathlib import Path
import pandas as pd
from src.features import FeatureMarker
from src.expertise import ExpertiseAnalyzer
from collections import Counter

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

def list_to_dataframe(directory: List[dict]):
    """Guarda una lista de diccionarios en un archivo CSV."""
    return pd.DataFrame(directory)

def get_researcher_url_by_index(index_nb: int, df: pd.DataFrame) -> str:
    """Guarda una lista de diccionarios en un archivo CSV."""
    #global df_researchers
    researcher_url = df.loc[index_nb, "Profile URL"]
    # print(f'ESTE TIPO ES DEL URL {type(researcher_url)}')
    # print(f'URL: {researcher_url}')
    return researcher_url

def feature_extraction_pipeline(df_initial: pd.DataFrame) -> pd.DataFrame:
    """
    Función principal que ejecuta toda la tubería (pipeline) de extracción
    de características a partir del DataFrame inicial.

    Args:
        df_initial: El DataFrame de pandas con las 5 columnas iniciales.

    Returns:
        Un DataFrame de pandas con las 7 características extraídas.
    """

    # 1. Instanciar la clase FeatureExtractor con el DataFrame inicial
    extractor = FeatureMarker(df_initial)

    # 2. Ejecutar los métodos de extracción secuencialmente
    # Nota: Los métodos se encadenan al modificar internamente el DataFrame (self.df)
    # y devolverlo para el siguiente paso (aunque aquí no estamos encadenando directamente).

    extractor.extract_target_environment()
    extractor.extract_number_of_items()
    extractor.extract_brief_description()
    extractor.extract_target_population()
    extractor.extract_age_range()

    # 3. Seleccionar las columnas finales y renombrar
    df_result = extractor.select_and_rename_final_columns()

    return df_result

def expertise_extraction_pipeline(df_initial: pd.DataFrame, text_column: str):
    """
        Función principal que ejecuta toda la tubería (pipeline) de extracción
        de palabras clave sobre el expertise a partir del DataFrame inicial.

        Args:
            df_initial: El DataFrame de pandas con las 7 columnas iniciales.

        Returns:
            :param df_initial: DataFrame de pandas con las 8 características extraídas.
            :param text_column: Nombre de la columna objetivo
        """

    # 1. Instanciar la clase FeatureExtractor con el DataFrame inicial
    tokenizer = ExpertiseAnalyzer(df_initial, text_column)

    # 2. Evaluamos los métodos de extracción secuencialmente
    # Nota: Los métodos se encadenan al modificar internamente el DataFrame (self.df)
    # y devolverlo para el siguiente paso (aunque aquí no estamos encadenando directamente).

    word_freq = tokenizer.get_word_frequency()
    print("Palabras más comunes:")
    print(word_freq.most_common(30))

    tokenizer.generate_wordcloud(save_path="./data/wordcloud.png")

    bigram_freq = tokenizer.get_ngram_frequency(n=2, language='english')
    print("Bigramas más comunes:")
    print(bigram_freq.most_common(30))

    trigram_freq = tokenizer.get_ngram_frequency(n=3, language='english')
    print("Trigramas más comunes:")
    print(trigram_freq.most_common(30))


    # 3. Seleccionar las columnas finales y renombrar
    # df_result = tokenizer.select_and_rename_final_columns()

    top_words = tokenizer.get_top_ngrams(n=1, top_n=30)
    print("Palabras más comunes:")
    print(top_words)

    # Nueva columna de ngrams comunes con cada investigador
    tokenizer.add_ngrams_column(n=1, list_ngrams=top_words, new_column_name='Expertise_By_words')

    top_bigrams = tokenizer.get_top_ngrams(n=2, top_n=30)
    print("Bigrams más comunes:")
    print(top_bigrams)

    # Nueva columna de ngrams comunes con cada investigador
    tokenizer.add_ngrams_column(n=2, list_ngrams=top_bigrams, new_column_name='Expertise_Bigrams')

    top_trigrams = tokenizer.get_top_ngrams(n=3, top_n=10)
    print("Trigrams más comunes:")
    print(top_trigrams)

    # Nueva columna de ngrams comunes con cada investigador
    tokenizer.add_ngrams_column(n=3, list_ngrams=top_trigrams, new_column_name='Expertise_Trigrams')

    return


def save_dataframe_to_csv(df: pd.DataFrame, filename):
    """Guarda una lista de diccionarios en un archivo CSV."""

    df.to_csv(f"data/{filename}.csv", index=False, encoding='utf-8')

    print(f"\nDatos guardados exitosamente en data/{filename}")
    return


def save_data(data: List[Dict], filename):
    """Guarda una lista de diccionarios en un archivo CSV."""
    df = pd.DataFrame(data)
    df.to_csv(f"data/{filename}", index=False, encoding='utf-8')

    print(f"\nDatos guardados exitosamente en data/{filename}")
    return df

