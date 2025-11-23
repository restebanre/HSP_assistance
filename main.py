# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from src.utils import save_data
from src.measures import scrape_sensitivity_measures
from src.researchers import *

from src.utils import *
global df_researchers
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

if __name__ == '__main__':
    df_measures = scrape_sensitivity_measures()
    print(df_measures)
    if not df_measures.empty:
        df_measures.to_csv(f"data/measures.csv", sep='\t', index=False, encoding='utf-8')

        # save_data(measures, 'measures.csv')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# if __name__ == '__main.ipynb__':
    # researchers = scrape_researchers_from_directory()
    # print(researchers)
    # if researchers:
        # save_data(researchers, 'researchers.csv')

# if __name__ == '__main.ipynb__':
    lst = scrape_researchers_from_directory()
    # print(df_researchers)

    for i in range(1):
        df_researchers = write_directory(lst)
        # print(get_researcher_url_by_index(i, df_researchers))
        url= get_researcher_url_by_index(i, df_researchers)
        scrape_researcher_details(url)

    if not df_researchers.empty:
        df_researchers.to_csv(f"data/researchers.csv", sep='\t', index=False, encoding='utf-8')