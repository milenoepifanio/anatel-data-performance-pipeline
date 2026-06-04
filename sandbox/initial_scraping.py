"""
Initial Scraping

Script para fazer scraping inicial de dados do Anatel usando Selenium.
"""

# ============================================================================
# Cell 1: Install Selenium
# ============================================================================

# pip install selenium

# ============================================================================
# Cell 2: Import Required Libraries
# ============================================================================

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver.chrome.service import Service
import time
import os

# ============================================================================
# Cell 3: Define Chrome Options Function
# ============================================================================

def get_default_chrome_options(caminho_pasta):
    # Garante que a pasta existe
    os.makedirs(caminho_pasta, exist_ok=True)

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    # Define configurações de download
    prefs = {
        "download.default_directory": os.path.abspath(caminho_pasta),
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    }

    options.add_experimental_option("prefs", prefs)

    return options

# ============================================================================
# Cell 4: Set Download Directory
# ============================================================================

pasta_destino = "C:/Users/mileno_epifanio/Downloads/PDI/data/raw"

# ============================================================================
# Cell 5: Scrape Anatel Data
# ============================================================================

# Abre o site
driver = webdriver.Chrome(options=get_default_chrome_options(pasta_destino))

driver.get("https://dados.gov.br/dados/conjuntos-dados/indice-desempenho-atendimento")

# Espera os botões estarem visíveis e clica
wait = WebDriverWait(driver, 10)
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-controls='collapse-organizacao']"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-controls='collapse-recursos']"))).click()

# Espera os elementos carregarem
time.sleep(2)  # ou use WebDriverWait com o seletor certo

# Corrige o seletor (TAG 'col-10' não existe — isso é uma classe!)
elementos = driver.find_elements(By.CLASS_NAME, "col-10")
print(elementos)

# Altere "sua-id-aqui" pelo valor real do ID do container onde estão os links
container = driver.find_elements(By.ID, "btnDownloadUrl")

print(container)

palavras_chave = ["SCM", "SMP", "STFC", "TV"]

for i in elementos:
    if any(palavra in i.text for palavra in palavras_chave):
        driver.execute_script("arguments[0].scrollIntoView(true);", i)
        print("🔍 Encontrado:", i.text)
        container_pai = i.find_element(By.ID, "btnDownloadUrl")
        container_pai.click()
        time.sleep(2)  # Aguarda carregamento se necessário
