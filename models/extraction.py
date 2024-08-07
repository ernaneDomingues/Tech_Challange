import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

START_YEAR = 1970
END_YEAR = datetime.now().year

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

def parse_table_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find('table', class_='tb_base tb_dados')
    headers = [header.text.strip() for header in table.find_all('th')]
    rows = [
        [cell.text.strip() for cell in row.find_all('td')]
        for row in table.find_all('tr')[1:]
    ]
    return headers, rows

def extract_table_data(url, year):
    try:
        content = fetch_page_content(url)
        headers, rows = parse_table_content(content)
        df = pd.DataFrame(rows, columns=headers)
        df['Ano'] = year
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

def pivot_dataframe(df, columns):
    if not all(col in df.columns for col in columns):
        raise ValueError("Uma ou mais colunas especificadas não estão presentes no DataFrame")
    for col in columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df_pivot = df.pivot_table(index='Ano', columns=columns[0], values=columns[1:], aggfunc='sum')
    df_pivot.columns = ['_'.join(col).strip() for col in df_pivot.columns.values]
    df_pivot.reset_index(inplace=True)
    return df_pivot

def get_table_headers(url, end_year):
    content = fetch_page_content(url.format(year=end_year))
    headers, _ = parse_table_content(content)
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


if __name__=='__main__':
    
    # Função principal para extrair dados de todos os URLs
    def extract_and_save_all_data(url_templates, start_year, end_year):
        for url_template in url_templates:
            all_data = extract_table_all_data(url_template, start_year, end_year)
            if not all_data.empty:
                headers = get_table_headers(url_template, end_year)
                filename = get_filename_from_page(end_year, url_template)
                if filename:
                    save_to_csv(all_data, filename)
                    print(f"Dados salvos em {filename}")
    # Executa a extração de dados
    extract_and_save_all_data(URL_TEMPLATES, START_YEAR, END_YEAR)