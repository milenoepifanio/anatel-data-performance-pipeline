"""
Refactor Scraping Class

Versão refatorada da classe de scraping do Anatel com melhor estrutura e error handling.
"""

# ============================================================================
# Cell 1: Import Required Libraries
# ============================================================================

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from typing import List

# ============================================================================
# Cell 2: AnatelPerformanceScraper Class
# ============================================================================

class AnatelPerformanceScraper:
    def __init__(self, download_directory: str, timeout_seconds: int = 10):
        self.download_directory = os.path.abspath(download_directory)
        os.makedirs(self.download_directory, exist_ok=True)
        self.timeout_seconds = timeout_seconds
        self.driver = None
        self.keywords = ["SCM", "SMP", "STFC", "TV"]

    @staticmethod
    def get_default_chrome_options(download_directory: str) -> webdriver.ChromeOptions:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

        prefs = {
            "download.default_directory": os.path.abspath(download_directory),
            "download.prompt_for_download": False,
            "directory_upgrade": True,
            "safebrowsing.enabled": True,
        }

        options.add_experimental_option("prefs", prefs)
        return options

    def open_browser(self) -> None:
        options = self.get_default_chrome_options(self.download_directory)
        self.driver = webdriver.Chrome(options=options)

    def close_browser(self) -> None:
        if self.driver is not None:
            self.driver.quit()
            self.driver = None

    def navigate_to_source(self, url: str) -> None:
        assert self.driver is not None, "Browser must be opened before navigation."
        self.driver.get(url)

    def expand_sections(self) -> None:
        assert self.driver is not None, "Browser must be opened before expanding sections."
        wait = WebDriverWait(self.driver, self.timeout_seconds)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-controls='collapse-organizacao']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-controls='collapse-recursos']"))).click()

    def list_download_targets(self) -> List[webdriver.remote.webelement.WebElement]:
        assert self.driver is not None, "Browser must be opened before listing targets."
        time.sleep(2)
        return self.driver.find_elements(By.CLASS_NAME, "col-10")

    def filter_targets(self, targets: List[webdriver.remote.webelement.WebElement]) -> List[webdriver.remote.webelement.WebElement]:
        return [target for target in targets if any(keyword in target.text for keyword in self.keywords)]

    def download_matching_files(self, targets: List[webdriver.remote.webelement.WebElement]) -> List[str]:
        assert self.driver is not None, "Browser must be opened before downloading files."

        downloaded = []
        for target in targets:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", target)
            download_button = target.find_element(By.ID, "btnDownloadUrl")
            download_button.click()
            downloaded.append(target.text)
            time.sleep(2)

        return downloaded

    def run(self, source_url: str) -> List[str]:
        try:
            self.open_browser()
            self.navigate_to_source(source_url)
            self.expand_sections()
            targets = self.list_download_targets()
            matching_targets = self.filter_targets(targets)
            return self.download_matching_files(matching_targets)
        finally:
            self.close_browser()

# ============================================================================
# Cell 3: Execute Scraping
# ============================================================================

download_directory = "C:/Users/Mileno/Downloads/PDI/data/raw"

source_url = "https://dados.gov.br/dados/conjuntos-dados/indice-desempenho-atendimento"

scraper = AnatelPerformanceScraper(download_directory)
matched_items = scraper.run(source_url)
print("Downloaded items:", len(matched_items))
