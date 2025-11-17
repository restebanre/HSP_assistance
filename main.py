# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from src.utils import save_data
from src.measures import scrape_sensitivity_measures
from src.researchers import scrape_researchers_from_directory

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

if __name__ == '__main__':
    measures = scrape_sensitivity_measures()
    print(measures)
    if measures:
        save_data(measures, 'measures.csv')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# if __name__ == '__main.ipynb__':
    researchers = scrape_researchers_from_directory()
    print(researchers)
    if researchers:
        save_data(researchers, 'researchers.csv')