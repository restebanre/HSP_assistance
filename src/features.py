# features.py
import pandas as pd
import numpy as np
import re


class FeatureMarker:
    """
    Clase para encapsular y aplicar toda la lógica de extracción y refinamiento
    de características sobre el DataFrame de medidas de sensibilidad.
    """

    def __init__(self, df: pd.DataFrame):
        """Inicializa la clase con el DataFrame original."""
        self.df = df.copy()  # Trabaja sobre una copia para no modificar el original

    def extract_target_environment(self) -> pd.DataFrame:
        """Extrae la característica 'Target Environment' (Entorno Objetivo)."""

        def classify_environment(row):
            name = row['Name of the Measure']
            desc = row['Description']

            if 'Observational Measure' in row['Type of Measure']:
                return 'Preescolar/Laboratorio'
            if 'School' in name or 'school context' in desc:
                return 'Entorno Escolar'
            if 'Parent Version' in name:
                return 'Hogar/Familia'
            if 'Person Scale' in name and 'adults' in desc:
                return 'Vida Adulta General'
            if 'Child Scale' in name or 'adolescents' in desc:
                return 'Hogar/Escuela (General Infantil)'

            return 'Indefinido'

        self.df['Target Environment'] = self.df.apply(classify_environment, axis=1)
        return self.df

    def extract_number_of_items(self) -> pd.DataFrame:
        """Extrae y refina la característica 'Number of Items'."""

        # 1. Extracción inicial de ítems principales
        item_extraction_pattern = r'is an? (\d+)-?items?'
        self.df['Number of Items'] = self.df['Description'].str.extract(item_extraction_pattern, expand=False)
        self.df['Number of Items'] = self.df['Number of Items'].fillna('').astype(str)

        # 2. Corrección: Versión de Padres es 12
        self.df.loc[self.df['Name of the Measure'].str.contains('Parent Version'), 'Number of Items'] = '12'

        # 3. Formato final (incluyendo ítems adicionales)
        def format_number_of_items(row):
            desc = row['Description']

            if 'additional items' in desc:
                match_add = re.search(r'(\d+) additional items', desc)
                main_items = row['Number of Items']
                if match_add and main_items.isdigit():
                    return f"{main_items} (+{match_add.group(1)})"

            if 'Observational Measure' in row['Type of Measure']:
                return 'N/A'

            if row['Number of Items'].isdigit():
                return row['Number of Items']

            return 'N/A'

        self.df['Number of Items'] = self.df.apply(format_number_of_items, axis=1)
        return self.df

    def extract_brief_description(self) -> pd.DataFrame:
        """Crea la descripción breve."""
        # Tomar la primera frase de la descripción
        self.df['Brief description'] = self.df['Description'].str.split('.').str[0]
        return self.df

    def extract_target_population(self) -> pd.DataFrame:
        """Clasifica la población objetivo (Adulto, Niño/Adolescente, etc.)."""

        def classify_population(row):
            env = row['Target Environment']
            if 'Adult' in env:
                return 'Adulto'
            elif 'Hogar/Familia' in env:
                return 'Padres (Evaluación de Niño)'
            elif 'Escolar' in env:
                return 'Profesor (Evaluación de Niño)'
            elif 'Preescolar' in env:
                return 'Observador (Evaluación de Niño)'
            else:
                return 'Niño/Adolescente (Autoreporte)'

        self.df['Target population'] = self.df.apply(classify_population, axis=1)
        return self.df

    def extract_age_range(self) -> pd.DataFrame:
        """Extrae el rango de edades."""

        def extract_age_range_logic(description):
            # Pattern 1: edades X-Y
            match_range = re.search(r'ages of (\d+) and (\d+) years', description)
            if match_range:
                return f"{match_range.group(1)}-{match_range.group(2)} años"

            # Pattern 2: edad única (e.g., three-year-old)
            match_single = re.search(r'(\w+)-year-old children', description)
            if match_single:
                return f"Aprox. {match_single.group(1)} años"

            # Pattern 3: Adults (general)
            if 'in adults' in description:
                return 'Adultos (18+)'

            return 'No especificado'

        self.df['Age Range'] = self.df['Description'].apply(extract_age_range_logic)
        return self.df

    def select_and_rename_final_columns(self) -> pd.DataFrame:
        """Selecciona las columnas finales y renombra 'Language'."""

        final_columns = [
            'Name of the Measure',
            'Brief description',
            'Number of Items',
            'Target population',
            'Age Range',
            'Target Environment',
            'Language'
        ]

        df_final = self.df[final_columns].rename(columns={'Language': 'Disponibilidad idioma'})
        return df_final