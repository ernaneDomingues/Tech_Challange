import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

START_YEAR = 1970
END_YEAR = datetime.now().year - 1

# URLs base para cada tipo de tabela
URL_TEMPLATES = [
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_02",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_03&subopcao=subopt_01",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_03&subopcao=subopt_02",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_03&subopcao=subopt_03",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_03&subopcao=subopt_04",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_04",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_05&subopcao=subopt_01",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_05&subopcao=subopt_02",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_05&subopcao=subopt_03",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_05&subopcao=subopt_04",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_05&subopcao=subopt_05",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_06&subopcao=subopt_01",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_06&subopcao=subopt_02",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_06&subopcao=subopt_03",
    "http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao=opt_06&subopcao=subopt_04"
]


def fetch_page_content(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def parse_table_content_with_category(content):
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table', class_='tb_base tb_dados')
    headers = [header.text.strip() for header in table.find_all('th')]
    headers.insert(0, 'Categoria')
    rows = []

    current_category = None

    for row in table.find_all('tr'):
        cells = row.find_all('td')

        if len(cells) == 2:
            product = cells[0].text.strip()
            quantity = cells[1].text.strip().replace('.', '').replace('-', '0')
            quantity = int(quantity) if quantity.isdigit() else 0

            # Verifica se o texto está em maiúsculas e não contém números
            if product.isupper() and not any(c.isdigit() for c in product):
                # Se for uma linha de soma total, assume como a categoria atual
                current_category = product
            else:
                # Adiciona a linha ao DataFrame com a categoria atual
                rows.append([current_category, product, quantity])

    return headers, rows

def get_table_headers(url, end_year):
    content = fetch_page_content(url.format(year=end_year))
    headers, _ = parse_table_content_with_category(content)
    return headers

def get_filename_from_page(end_year, url):
    content = fetch_page_content(url.format(year=end_year))
    soup = BeautifulSoup(content, 'html.parser')
    p_element = soup.find('p', {'class': 'text_center'})
    if p_element:
        filename_base = p_element.text.strip().replace(f' [{end_year}]', '').replace(' ', '_').replace(',', '')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{filename_base}_{timestamp}.csv'
        return filename
    return None

def save_to_csv(df, filename):
    df.to_csv(filename, index=False)

def standardize_column_name(column):
    column = column.strip()  # Remove extra spaces
    column = column.lower()  # Convert to lowercase
    column = column.replace(' ', '_')  # Replace spaces with underscores
    column = column.replace('(', '')  # Remove parentheses
    column = column.replace(')', '')  # Remove parentheses
    column = column.replace('.', '')  # Remove periods
    return column

def extract_table_data(url, year):
    try:
        content = fetch_page_content(url)
        headers, rows = parse_table_content_with_category(content)
        df = pd.DataFrame(rows, columns=headers)
        df['Ano'] = year
        df.columns = [standardize_column_name(col) for col in df.columns]
        return df
    except Exception as e:
        print(f"Erro ao extrair dados do ano {year}: {e}")
        return pd.DataFrame()

def extract_table_all_data(url_template, start_year, end_year):
    all_data = pd.DataFrame()
    for year in range(start_year, end_year + 1):
        url = url_template.format(year=year)
        year_data = extract_table_data(url, year)
        if not year_data.empty:
            all_data = pd.concat([all_data, year_data], ignore_index=True)
            print(f"Dados do ano {year} extraídos com sucesso.")
    return all_data

if __name__=='__main__':    
    # Função principal para extrair dados de todos os URLs
    def extract_and_save_all_data(url_templates, start_year, end_year):
        for url_template in url_templates:
            all_data = extract_table_all_data(url_template, start_year, end_year)
            if not all_data.empty:
                filename = get_filename_from_page(end_year, url_template)
                if filename:
                    save_to_csv(all_data, filename)
                    print(f"Dados salvos em {filename}")
    # Executa a extração de dados
    extract_and_save_all_data(URL_TEMPLATES, START_YEAR, END_YEAR)