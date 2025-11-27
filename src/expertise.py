# expertise.py

import pandas as pd
import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
import nltk
import matplotlib.pyplot as plt
from matplotlib import use
from wordcloud import WordCloud
from typing import List, Dict, Set
### from lib2to3.btm_utils import tokens
###

use('Agg')
# descargamos recursos de NLTK
nltk.download('stopwords')
# nltk.download('punk')
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

class ExpertiseAnalyzer:
    def __init__(self, df: pd.DataFrame, text_column: str):
        """
        Inicializa el analizador con un DataFrame y el nombre de la columna de texto
        :param df: DataFrame que contiene los datos de los investigadores
        :param text_column: Nombre de la columna objetivo del analisis
        """
        self.df = df
        self.text_column = text_column
        # self.language = 'English'

    @staticmethod
    def clean_and_tokenize(text: str, language: str = 'english') -> list:
        """
        Limpia y tokeniza el texto.

        :param language: language
        :param text: TExto a procesar
        :return: Lista de tokens limpios
        """
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        tokens = word_tokenize(text, language=language, preserve_line=True)
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words and len(word) > 2]
        return tokens

    @staticmethod
    def extract_ngrams(tokens: list, n: int =2) -> list:
        """
        Extrae n-grams de una lista de tokens

        :param tokens: Lista de tokens
        :param n: Tamaño de lon n-grams (por defecto, 2 para bigramas)
        :return: lists de n-gramas
        """
        return [' '.join(gram) for gram in ngrams(tokens, n)]

    def get_word_frequency(self) -> Counter:
        """
        Obtiene la frecuencia de palabras en la columna texto

        :return: Diccionario con las palabras y su frecuencia
        """
        all_tokens = []
        for text in self.df[self.text_column]:
            tokens = self.clean_and_tokenize(text)
            all_tokens.extend(tokens)
        return Counter(all_tokens)

    def get_ngram_frequency(
            self, n: int = 2, language: str = 'english'
                            ) -> Counter:
        """
        Obtiene la frecuancia de n-gramas en la columna de texto

        :param language: language
        :param n: Tamaño de los n-gramas (por defect 2)
        :return: Diccionario con los n-gramas y su frecuancia
        """
        all_ngrams = []
        print('FEATURE')
        print(self.df[self.text_column].head())
        for text in self.df[self.text_column]:
            tokens = self.clean_and_tokenize(text, language=language)
            ngrams_list = self.extract_ngrams(tokens, n)
            all_ngrams.extend(ngrams_list)
        return Counter(all_ngrams)

    def generate_wordcloud(self, save_path: str = None):
        """
        Genera una nube de palabras y la guarda opconalente.

        :param save_path: save_path (str, optional): Ruta para guardar
                la imagen de la nube de palabras
        :return:
        """
        all_tokens = []
        for text in self.df[self.text_column]:
            tokens = self.clean_and_tokenize(text)
            all_tokens.extend(tokens)

        wordcloud = \
            (WordCloud(width=800, height=400, background_color='white')
             .generate(' '.join(all_tokens)))

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Nube de Palabras - Expertise')

        if save_path:
            plt.savefig(save_path)
        plt.show()

    def get_top_keywords(self, top_n: int = 20) -> List[str]:
        word_freq = self.get_word_frequency()
        return [word for word, count in word_freq.most_common(top_n)]

    def get_top_ngrams(self, n: int = 3, top_n: int = 20) -> List[str]:
        ngram_freq = self.get_ngram_frequency(n)
        return [ngram for ngram, count in ngram_freq.most_common(top_n)]

    def add_ngrams_column(
            self, keywords: List[str], new_column_name: str = 'Keywords'
                            ) -> None:
        """
        Añade una nueva columna al DataFrame con las palabras clave que coinciden
        con el expertise del investigador

        :param keywords: Lista de palabras clave de interés
        :param new_column_name: Nombre de la nueva columna
        :return: None
        """
        self.df[new_column_name] = self.df[self.text_column].apply(
            lambda text: ', '.join([word for word in keywords if word in
        self.clean_and_tokenize(text)])
        )


