# src/researchers.py
from src.utils import *
import pandas as pd
import re

URL_DIRECTORY = f"{BASE_URL}/research/researchers-directory/"
URL_RESEARCHER = f"{BASE_URL}/researcher/"


def scrape_researchers_from_directory() -> List[Dict]:
    """
    Extrae el directorio principal y luego hace drill-down a cada perfil.

    Returns:
        list: Una lista de diccionarios con los datos completos de los investigadores.
    """


    soup = get_soup(URL_DIRECTORY)
    if not soup:
        return []

    entry_directory = []
    # Localizar la estructura de la lista de investigadores (asumimos una lista de divs/articles)
    # researcher_list_items = soup.find_all('article', class_=re.compile(r'researcher-card', re.I))
    researcher_card_list = soup.select('.fl-post-grid-post.researcher')
    print(researcher_card_list)

    for card in researcher_card_list:
        print(card)
        try:
            name_tag = card.find('h2')
            name = name_tag.get_text(strip=True) if name_tag else 'N/A'

            # El enlace al perfil individual
            profile_link_tag = card.find('a', href=True)
            profile_url = f"{profile_link_tag['href']}" if profile_link_tag else None
            print(f'URL investigador:{profile_url}')
            # Estatus y Universidad (asumiendo que están en párrafos o spans)
            # status_uni_raw = card.find('p').get_text(strip=True).split(' at ')  # Ejemplo de división
            # status = status_uni_raw[0].strip()
            # university = status_uni_raw[1].strip() if len(status_uni_raw) > 1 else 'N/A'
            status_tag = card.select_one("p:nth-of-type(1)")
            status = status_tag.get_text(strip=True) if status_tag else "N/A"

            university_tag = card.select_one("p:nth-of-type(2)")
            university = university_tag.get_text(strip=True) if university_tag else "N/A"

            # Obtener detalles del perfil (el drill-down)
            # details = {}
            # if profile_url:
                # details = scrape_researcher_details(profile_url)

            # print(f'detalles investigador{details}')

            researcher_entry = {
                'Name': name,
                'Status': status,
                'University': university,
                'Profile URL': profile_url
            }
            entry_directory.append(researcher_entry)

        except Exception as e:
            print(f"Error procesando investigador: {e}")
            continue

    return entry_directory



def scrape_researcher_details(profile_url: str) -> Dict:
    """Extrae datos detallados (Expertise, Contacto) de la página individual."""
    global info_paragraph
    """Extrae datos detallados (Expertise, Contacto) de la página individual."""

    soup = get_soup(profile_url)

    # details = {
    #     'Full Expertise': '',
    #     'Email': '',
    #     'Discipline': '',
    #     'Location': ''
    # }

    researcher_card = {
        'Name': None,
        'Title': None,
        'Institution': None,
        'Expertise': None,
        'Discipline of research': None,
        'Location': None,
        'Contact':None
    }

    # Contenido principal de la ficha del investigador
    card_details = soup.select_one('.fl-row-fixed-width.fl-row-bg-none')

    if not card_details:
        return []

    #---------------------------------------
    # 1er bloque: Nombre, titulo, Expertise
    #---------------------------------------

    # 1. Expertise
    expertise_section = card_details.select_one('.fl-col:nth-of-type(1) .fl-module-html .fl-html')

    if expertise_section:
        researcher_card['Name'] = expertise_section.find('h1').get_text(strip=True)
        researcher_card['Title'] = expertise_section.find('h2').get_text(strip=True)

        # Expertise (rejuntamos pedazos de texto en un mismo parrafo)
        chunks = []
        tag_h3 = expertise_section.find('h3')

        # texto suelto despues de h3
        if tag_h3 and tag_h3.next_sibling:
            chunks.append(tag_h3.next_sibling.get_text(strip=True))

        # parrafos subsiguientes
        for p in expertise_section.find_all('p'):
            exp_paragraph = p.get_text(strip=True)
            if exp_paragraph:
                chunks.append(exp_paragraph)

        # unimos pedazos y depuramos texto y saltos de linea
        cleaned_paragraph = ' '.join(chunks).strip('"').replace(u'\xa0', u' ')

        researcher_card['Expertise'] = re.sub(r'\s+', ' ', cleaned_paragraph).strip()
            #(expertise_section.find('h3').g.get_text(strip=True))
        print(researcher_card)

    #---------------------------------------
    # 2do bloque: disciplina, ubicacion e e-mail
    #---------------------------------------

    card_section = card_details.select_one('.fl-col:nth-of-type(2) .fl-module-html .fl-html')

    print(card_section)
    # recuperamos una lista por balizas de <p>
    if card_section:
        info_paragraph = card_section.find_all('p')
        print(f'Bloque 2 {info_paragraph}')

    # 1. Disciplina de investigacion
    if len(info_paragraph) > 0:
        # texto se encuentra despues de un <br/>
        tag_discipline = info_paragraph[0].find('br')

        if tag_discipline and tag_discipline.next_sibling:
            # raw_discipline = buffer.split(feature, 1)[1].strip()
            discipline = tag_discipline.next_sibling.strip()
            researcher_card['Discipline of research'] = re.sub(r'\s+', ' ', discipline).strip()
        else:
            researcher_card['Discipline of research'] = 'N/A'
        print(researcher_card['Discipline of research'])

    #2. Ubicacion
    if len(info_paragraph) > 1:
        print(f'info {info_paragraph[1]}')
        # texto se encuentra despues de un <br/>
        tag_location = info_paragraph[1]
        print(f' tag_loc {tag_location}')
        buffer2 = tag_location.text.strip()
        feature2 = 'Location:'
        print(f'buffer {buffer2}')

        if feature2 in buffer2:
            tag_location = buffer2.split(feature2, 1)[1].strip()
            print(f' tag_loc_2 {tag_location}')
            chunks_location = [chunk.strip(",").strip() for chunk in tag_location.split('\n') if chunk.strip()]
            #location = tag_location.next_sibling.strip().strip('"')
            #researcher_card['Location'] = re.sub(r'\s+', ' ', location).strip()
            researcher_card['Location'] = ', '.join(chunks_location)
        else:
            researcher_card['Location'] = 'N/A'
        print(researcher_card['Location'])

    # 3. Contacto
    if len(info_paragraph) > 2:
        # texto se encuentra despues de un <br/>
        tag_contact = info_paragraph[2] #.find('br')
        contacto = tag_contact.find('a')
        if contacto:
            researcher_card['Contact'] = contacto.text.strip()
        else:
            researcher_card['Contact'] = 'N/A'
        print(researcher_card['Contact'])



    # 3. Disciplina y Ubicación (asumiendo que están etiquetados de alguna manera)
    # Esto requiere inspección manual, pero se simula la extracción de etiquetas
    # print(details['Discipline'])

    # 2. Contacto (Buscamos un patrón de email)
    # Aplicamos RegEx para extraer emails (patrón general: user@domain.tld)
    print(researcher_card)
    return researcher_card

def compile_researcher_directory(directory: List[Dict]) -> pd.DataFrame:


    directory_list = []
    df_url_directory = list_to_dataframe(directory)

    for idx in range(len(directory)): # len(directory)
        url= get_researcher_url_by_index(idx, df_url_directory)
        details = scrape_researcher_details(url)
        directory_list.append(details)

    print(f'DIRECTORY LIST: {directory_list}')
    return pd.DataFrame(directory_list)