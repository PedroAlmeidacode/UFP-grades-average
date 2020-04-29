import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()



def tableDataText(table):
    def rowgetDataText(tr, coltag='td'):
        return [td.get_text(strip=True) for td in tr.find_all(coltag)]
    rows = []
    trs = table.find_all('tr')
    headerow = rowgetDataText(trs[0], 'th')
    if headerow: # if there is a header row include first
        rows.append(headerow)
        trs = trs[1:]
    for tr in trs: # for every table row
        rows.append(rowgetDataText(tr, 'td') ) # data row
    return rows


def calculate_media(rows, creditos):
    total_credits = 0
    total_nota_times_credit = 0
    for line in range(0, len(rows)):
        disciplina = rows[line][0]
        grade = float(rows[line][2][0:2])
        ects = int(creditos[disciplina]) # coloca em var os creditos que a disciplina (rows[line][0]) vale
        total_credits += ects # soma ao total de creditos o credito da nova disciplina
        total_nota_times_credit += float(ects * grade)

    return float(total_nota_times_credit / total_credits)










creditos = {
'Estatística Aplicada':'5',
'Gramática da Comunicação':'3',
'Inglês':'3',
'Introdução à Algoritmia e Programação':'6',
'Matemática I':'7',
'Sistemas de Informação':'6',
'Análise de Sistemas':'6',
'Eletrónica Aplicada':'7',
'Física':'4',
'Matemática II':'7',
'Energias e Meio Ambiente':'6',
'Língua Estrangeira -Alemão-':'6',
'Algoritmos e Estruturas de Dados I':'6',
'Análise Numérica':'5',
'Arquitetura de Computadores':'6',
'Linguagens de Programação I':'7',
'Sistemas Digitais':'6',
'Algoritmos e Estruturas de Dados II':'6',
'Hardware e Sensores':'6',
'Investigação Operacional':'4',
'Linguagens de Programação II':'7',
'Sistemas Operativos':'7',
'Bases de Dados':'6',
'Engenharia de Software':'6',
'Laboratório de Programação':'5',
'Multimédia I':'6',
'Redes de Computadores I':'7',
'Laboratório de Projeto Integrado':'7',
'Multimédia II':'6',
'Conceção de Jogos':'4',
'Redes de Computadores II':'7',
'Sistemas Distribuídos':'6'
}


number = os.getenv('USER_LOGIN')
pswd = os.getenv('USER_PSWD')
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) snap Chromium/81.0.4044.122 Chrome/81.0.4044.122 Safari/537.36'}
login_data = {
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    'ctl00$ContentPlaceHolder1$Accordion1_AccordionExtender_ClientState': '0',
    'ctl00$ContentPlaceHolder1$AccordionPane1_content$txtLogin': number,
    'ctl00$ContentPlaceHolder1$AccordionPane1_content$Button1': 'Validar',
    'ctl00$ContentPlaceHolder1$AccordionPane1_content$txtPassword': pswd,
    'ctl00$ContentPlaceHolder1$AccordionPane1_content$ddlIMG': 'pt'
}




with requests.Session() as s:
    print("Fetching data from SIUFP...")
    url = "https://portal.ufp.pt/authentication.aspx"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    login_data['__VIEWSTATE'] = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
    login_data['__EVENTVALIDATION'] = soup.find('input', attrs={'name': '__EVENTVALIDATION'})['value']
    login_data['__VIEWSTATEGENERATOR'] = soup.find('input', attrs={'name': '__VIEWSTATEGENERATOR'})['value']

    page = s.post(url, data=login_data, headers=headers)
    notas = s.get("https://portal.ufp.pt/Notas/Definitivo.aspx", headers=headers)

contain_notes = BeautifulSoup(notas.content, "html.parser")
table = contain_notes.find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == "ctl00_ContentPlaceHolder1_AccordionPane1_content_GridView1")
rows = tableDataText(table)

rows.pop(0) # retira primeiro valor que indica os tipos dos valores do resto da lista
print("You average is: ", calculate_media(rows, creditos))





