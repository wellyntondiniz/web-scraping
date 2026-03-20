from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service
import re

#orm
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, insert, text, Double

username = "root" 
password = "******DIGITE SUA SENHA*****"  
host = "localhost"  
port = 3306  
database = "imobiliaria"  

connection_string = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(connection_string)

metadata = MetaData()

imovel = Table(
    "imoveis", metadata,
    Column("id", Integer, primary_key=True),
    Column("titulo", String(255)),
    Column("valor", Double)
)

def persistir_dados(titulo, preco):
    with engine.connect() as conexao:
        
        valor = re.sub(r'R\$\s*', '', preco)
        valor = re.sub(r'\.', '', valor)
        valor = re.sub(r'\,', '.', valor)
        
        novo_imovel = {
            "titulo": titulo,
            "valor": valor
        }

        comando = insert(imovel).values(novo_imovel)
        conexao.execute(comando)
        conexao.commit() 


def coletar(driver):
    results = driver.find_elements(By.TAG_NAME, "article")
    for result in results: 
        titulo = result.find_element(By.TAG_NAME, "h2").text
        tipo = result.find_element(By.TAG_NAME, "address").text
        preco = result.find_element(By.TAG_NAME, "h3").text
        itens = result.find_elements(By.TAG_NAME, "li")
        
        persistir_dados(titulo, preco)

        #for item in itens:
        #    print(item.text)
        #print('----------------------')

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)
try:
    driver.get("https://glaciosaimobiliaria.com.br/imoveis/mt/sinop/")

    
    for i in range(10):
        coletar(driver)
        
        botao = driver.find_element(By.CLASS_NAME, "next")
        
        #if not botao.is_enabled():
        #    break
        
        botao.click()
        
        time.sleep(5)



        
        
finally:
    driver.quit()
