"""
SCRIPT: Conversão do kanbn pra texto e csv
AUTOR: Danilo Mello
CRIAÇÃO: 01/03/2018
DESCRIÇÃO: Este script acessa o site do kanban com o auxílio do Selenium, acessa o quadro do projeto Unifica
            e realiza o scrap, passando os dados coletado para texto numa forma que possa ser lido pelo Oracle DB.
PARÂMETROS:
    EMAIL: email de login ao kanban (variável de sistema)
    EMAILSENHA: senha de acesso ao kaban (variável de sistema)
"""

import bs4, csv, os, re
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

browser = webdriver.Chrome(executable_path=os.path.join(os.getcwd(),"chromedriver.exe"))
wait = ui.WebDriverWait(browser, 10)

email = os.environ["EMAIL"]
senha = os.environ["EMAILSENHA"]

destinoArquivoTxt = os.path.join(os.getcwd(), "kanban.txt")
destinoArquivoCSV = os.path.join(os.getcwd(), "kanban.csv")
destinoArquivoDesktop = os.path.join(os.environ["USERPROFILE"], "Desktop", "kanban.txt")

browser.get("https://kanbanflow.com/login?")
browser.find_element_by_id("email").send_keys(email)
browser.find_element_by_id("password").send_keys(senha)
browser.find_element_by_xpath("//button[@type='submit']").click()

browser.find_element_by_xpath("//div[@class='boardList-currentBoard truncate']").click()
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'UNIFICA')))
browser.find_element_by_partial_link_text("UNIFICA").click()
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='task-name']")))

codigoFonte = browser.page_source

sopa = bs4.BeautifulSoup(codigoFonte, "html.parser")

colunas = sopa.find('tbody').find('tr').find_all('td')

tituloColunaDosCartoes = {}
for i in range(len(colunas)):
    cartoes = bs4.BeautifulSoup(str(colunas[i]), "html.parser").find_all("span")
    for cartao in cartoes:
        if colunas[i].find("h2").text == "JOB":
            pass
        else:
            tituloColunaDosCartoes[cartao.text.strip()] = colunas[i].find("h2").text

#Escreve o dicionário de dados em um arquivo csv
# with open(destinoArquivoCSV, 'wb', newline='') as ofile:
#     dict_writer = csv.writer(ofile)
#     for key, val in cartoes.items():
#         dict_writer.writerow([key, val])

#Escreve o dicionário de dados em um arquivo txt
with open(destinoArquivoTxt, 'w', newline='') as ofile:
    for key, val in tituloColunaDosCartoes.items():
        try:
            ofile.write("'" + re.search(r'\d+', key).group() + "','" + val + "',\r\n")
        except:
            ofile.write("'" + key + "','" + val + "',\r\n")
ofile.close()

browser.quit()