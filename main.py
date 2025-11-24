# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from src.utils import save_data
from src.measures import scrape_sensitivity_measures
from src.researchers import *
from src.utils import *

global df_researchers

if __name__ == '__main__':

    # 1. Recuperamos en forma de  colleccion de datos (dataframe)
    # la tabla de medidores de indicadores en HSP

    df_measures = scrape_sensitivity_measures()
    print(df_measures)
    if not df_measures.empty:
        df_measures.to_csv(f"data/measures.csv", sep='\t', index=False, encoding='utf-8')

    # 2. Recuperamos en forma de dataframe, el directorio
    # de contactos de especialistas en HSP

    directory = scrape_researchers_from_directory()

    df_researchers = compile_researcher_directory(directory)
    print(df_researchers)
    # for idx in range(len(directory)):
    #     df_directory = write_directory(directory)
    #     url= get_researcher_url_by_index(idx, df_directory)
    #     df_researchers = scrape_researcher_details(url)

    if not df_researchers.empty:
        df_researchers.to_csv(f"data/researchers.csv", sep='\t', index=False, encoding='utf-8')