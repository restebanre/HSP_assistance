# src/researchers.py
from src.utils import get_soup, BASE_URL, save_data
import re

URL_DIRECTORY = f"{BASE_URL}/research/researchers-directory/"
URL_RESEARCHER = f"{BASE_URL}/researcher/"


def scrape_researchers_from_directory():
    """
    Extrae el directorio principal y luego hace drill-down a cada perfil.

    Returns:
        list: Una lista de diccionarios con los datos completos de los investigadores.
    """
    soup = get_soup(URL_DIRECTORY)
    if not soup:
        return []

    researchers_data = []
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

            # Estatus y Universidad (asumiendo que están en párrafos o spans)
            # status_uni_raw = card.find('p').get_text(strip=True).split(' at ')  # Ejemplo de división
            # status = status_uni_raw[0].strip()
            # university = status_uni_raw[1].strip() if len(status_uni_raw) > 1 else 'N/A'
            status_tag = card.select_one("p:nth-of-type(1)")
            status = status_tag.get_text(strip=True) if status_tag else "N/A"

            university_tag = card.select_one("p:nth-of-type(2)")
            university = university_tag.get_text(strip=True) if university_tag else "N/A"

            # Obtener detalles del perfil (el drill-down)
            details = {}
            if profile_url:
                details = scrape_researcher_details(profile_url)

            researcher_entry = {
                'Name': name,
                'Status': status,
                'University': university,
                'Profile URL': profile_url,
                'Expertise': details.get('Expertise', 'N/A'),
                'Email': details.get('Email', 'N/A'),
                'Discipline': details.get('Discipline', 'N/A'),
                'Location': details.get('Location', 'N/A'),
            }
            researchers_data.append(researcher_entry)

        except Exception as e:
            print(f"Error procesando investigador: {e}")
            continue

    return researchers_data


def scrape_researcher_details(profile_url):
    """Extrae datos detallados (Expertise, Contacto) de la página individual."""
    soup = get_soup(profile_url)
    details = {
        'Full Name': '',
        'Title': '',
        'Expertise': '',
        'Discipline': '',
        'Location': '',
        'Email': ''
    }

    if soup:
        # Ejemplo de localización de datos en la página de un investigador
        # Asumiendo que los datos están en divs o p con identificadores claros

        # 1. Expertise
        expertise_section = soup.select_one('.fl-module-content:nth-of-type(1)')
        if expertise_section:
            details['Full Name'] = expertise_section.find('h1')
            details['Title'] = expertise_section.find('h2')
            details['Expertise'] = expertise_section.find('h3')

        # 2. Contacto (Buscamos un patrón de email)
        # Aplicamos RegEx para extraer emails (patrón general: user@domain.tld)
        card_section = soup.select_one('.fl-module-content:nth-of-type(2)')
        if card_section:
            details['Discipline'] = card_section.select_one("p:nth-of-type(1)").select_one('br')
            details['Location'] = card_section.select_one("p:nth-of-type(2)").select_one('br')
            details['Email'] = card_section.find('a', href=True).replace('mailto:', '').strip()


        # 3. Disciplina y Ubicación (asumiendo que están etiquetados de alguna manera)
        # Esto requiere inspección manual, pero se simula la extracción de etiquetas

    return details


def scrape_researcher_details_bck(profile_url):
    """Extrae datos detallados (Expertise, Contacto) de la página individual."""
    soup = get_soup(profile_url)
    details = {
        'Full Expertise': '',
        'Email': '',
        'Discipline': '',
        'Location': ''
    }

    if soup:
        # Ejemplo de localización de datos en la página de un investigador
        # Asumiendo que los datos están en divs o p con identificadores claros

        # 1. Expertise
        expertise_section = soup.find('div', class_=re.compile(r'expertise|areas-of-research', re.I))
        if expertise_section:
            details['Full Expertise'] = expertise_section.get_text(strip=True).replace('\n', ', ')

        # 2. Contacto (Buscamos un patrón de email)
        # Aplicamos RegEx para extraer emails (patrón general: user@domain.tld)
        email_text = soup.get_text()
        email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', re.I)
        emails = "; ".join(set(email_pattern.findall(email_text)))
        details['Email'] = emails

        # 3. Disciplina y Ubicación (asumiendo que están etiquetados de alguna manera)
        # Esto requiere inspección manual, pero se simula la extracción de etiquetas
        contact_info = soup.find('div', class_=re.compile(r'contact-info', re.I))
        if contact_info:
            # Lógica placeholder: simula extracción de texto de etiquetas como 'Discipline:' o 'Location:'
            text = contact_info.get_text()
            discipline_match = re.search(r'Discipline:\s*(.*?)(?:\n|$)', text, re.I)
            location_match = re.search(r'Location:\s*(.*?)(?:\n|$)', text, re.I)

            details['Discipline'] = discipline_match.group(1).strip() if discipline_match else 'N/A'
            details['Location'] = location_match.group(1).strip() if location_match else 'N/A'

    return details


def scrape_researchers_directory():
    """
    Extrae el directorio principal y luego hace drill-down a cada perfil.

    Returns:
        list: Una lista de diccionarios con los datos completos de los investigadores.
    """
    soup = get_soup(URL_DIRECTORY)
    if not soup:
        return []

    researchers_data = []
    # Localizar la estructura de la lista de investigadores (asumimos una lista de divs/articles)
    researcher_list_items = soup.find_all('article', class_=re.compile(r'researcher-card', re.I))

    for item in researcher_list_items:
        try:
            name_tag = item.find('h3')
            name = name_tag.get_text(strip=True) if name_tag else 'N/A'

            # El enlace al perfil individual
            profile_link_tag = item.find('a', href=True)
            profile_url = f"{BASE_URL}{profile_link_tag['href']}" if profile_link_tag else None

            # Estatus y Universidad (asumiendo que están en párrafos o spans)
            status_uni_raw = item.find('p').get_text(strip=True).split(' at ')  # Ejemplo de división
            status = status_uni_raw[0].strip()
            university = status_uni_raw[1].strip() if len(status_uni_raw) > 1 else 'N/A'

            # Obtener detalles del perfil (el drill-down)
            details = {}
            if profile_url:
                details = scrape_researcher_details(profile_url)

            researcher_entry = {
                'Name': name,
                'Status': status,
                'University': university,
                'Profile URL': profile_url,
                'Expertise (Summary)': item.find('span', class_='expertise').get_text(strip=True) if item.find('span',
                                                                                                               class_='expertise') else 'N/A',
                'Expertise (Detailed)': details.get('Full Expertise', 'N/A'),
                'Email': details.get('Email', 'N/A'),
                'Discipline': details.get('Discipline', 'N/A'),
                'Location': details.get('Location', 'N/A'),
            }
            researchers_data.append(researcher_entry)

        except Exception as e:
            print(f"Error procesando investigador: {e}")
            continue

    return researchers_data


