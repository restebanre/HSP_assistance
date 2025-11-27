# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from src.measures import *
from src.researchers import *
from src.utils import *
from src.expertise import ExpertiseAnalyzer

global df_researchers

if __name__ == '__main__':

    """-------------------------------------------------------------
    # 1. Recuperamos en forma de  colleccion de datos (dataframe)  #
    # la tabla de medidores de indicadores en HSP                  #
    #------------------------------------------------------------"""


    # df_measures = scrape_sensitivity_measures()

    # save_dataframe_to_csv(df_measures, "measures")

    # df_segmentation = feature_extraction_pipeline(df_measures)

    # save_dataframe_to_csv(df_segmentation, "segmentation")

    """-------------------------------------------------------------
    # 2. Recuperamos en forma de dataframe, el directorio          #
    # de contactos de especialistas en HSP                         #
    #------------------------------------------------------------"""

    directory = scrape_researchers_from_directory()

    df_researchers = compile_researcher_directory(directory)

    # save_dataframe_to_csv(df_researchers, "researchers")


    """-------------------------------------------------------------
    # 3. xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx          #
    # de contactos de especialistas en HSP                         #
    #------------------------------------------------------------"""


    expertise_extraction_pipeline(df_researchers, 'Expertise')

    print(df_researchers.head())

    save_dataframe_to_csv(df_researchers, "ngrams_researchers")


#    if not df_researchers.empty:
#        df_researchers.to_csv(f"data/researchers.csv", sep='\t', index=False, encoding='utf-8')