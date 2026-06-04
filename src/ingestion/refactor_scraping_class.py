from pathlib import Path
from typing import List, Optional
from contextlib import contextmanager
import time
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.utils.paths import (
    RAW_DIR,
    SOURCE_URL_IDA_ANATEL,
    create_directories,
)

logger = logging.getLogger(__name__)


class AnatelPerformanceScraper:
    """
    Scraper responsible for downloading Anatel performance files
    from dados.gov.br into the local raw data layer.
    """

    def __init__(
        self,
        download_directory: Path,
        timeout_seconds: int = 10,
    ) -> None:
        self.download_directory = Path(download_directory).resolve()
        self.timeout_seconds = timeout_seconds
        self.driver: Optional[webdriver.Chrome] = None

        self.target_models = ["SCM", "SMP", "STFC", "TV"]

        self.model_mapping = {
            "SCM": "SCM",
            "SMP": "SMP",
            "STFC": "STFC",
            "TV": "SEAC",
        }

        self.download_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        logger.info(f"Scraper inicializado com diretório: {self.download_directory}")

    @staticmethod
    def get_default_chrome_options(
        download_directory: Path,
    ) -> webdriver.ChromeOptions:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

        prefs = {
            "download.default_directory": str(Path(download_directory).resolve()),
            "download.prompt_for_download": False,
            "directory_upgrade": True,
            "safebrowsing.enabled": True,
        }

        options.add_experimental_option("prefs", prefs)

        return options

    @contextmanager
    def managed_browser(self):
        try:
            self.open_browser()
            logger.info("Browser aberto com sucesso")
            yield self.driver
        except Exception as e:
            logger.error(f"Erro durante execução: {e}")
            raise
        finally:
            self.close_browser()
            logger.info("Browser fechado")

    def open_browser(self) -> None:
        options = self.get_default_chrome_options(
            self.download_directory
        )

        self.driver = webdriver.Chrome(
            options=options
        )

    def close_browser(self) -> None:
        if self.driver is not None:
            self.driver.quit()
            self.driver = None

    def navigate_to_source(
        self,
        source_url: str,
    ) -> None:
        if self.driver is None:
            raise RuntimeError(
                "Browser must be opened before navigation."
            )

        self.driver.get(source_url)

    def expand_sections(self) -> None:
        if self.driver is None:
            raise RuntimeError(
                "Browser must be opened before expanding sections."
            )

        wait = WebDriverWait(
            self.driver,
            self.timeout_seconds,
        )

        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@aria-controls='collapse-organizacao']")
            )
        ).click()

        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@aria-controls='collapse-recursos']")
            )
        ).click()

    def list_download_targets(self) -> List[WebElement]:
        if self.driver is None:
            raise RuntimeError(
                "Browser must be opened before listing targets."
            )

        time.sleep(2)

        return self.driver.find_elements(
            By.CLASS_NAME,
            "col-10",
        )

    def infer_model_from_page_text(
        self,
        target_text: str,
    ) -> str:
        target_text = target_text.upper()

        for raw_model, normalized_model in self.model_mapping.items():
            if raw_model in target_text:
                return normalized_model

        return "UNKNOWN"

    def filter_targets(
        self,
        targets: List[WebElement],
    ) -> List[WebElement]:
        filtered_targets = []

        for target in targets:
            model = self.infer_model_from_page_text(
                target.text
            )

            if model != "UNKNOWN":
                filtered_targets.append(target)

        logger.info(
            f"Arquivos válidos: {len(filtered_targets)} de {len(targets)}"
        )

        return filtered_targets

    def download_matching_files(
        self,
        targets: List[WebElement],
    ) -> List[str]:
        if self.driver is None:
            raise RuntimeError(
                "Browser must be opened before downloading files."
            )

        downloaded_items = []
        failed_items = []

        for idx, target in enumerate(targets, 1):
            try:
                target_text = target.text
                model = self.infer_model_from_page_text(
                    target_text
                )

                logger.info(
                    f"[{idx}/{len(targets)}] Baixando: {target_text} | Modelo: {model}"
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView(true);",
                    target,
                )

                download_button = target.find_element(
                    By.ID,
                    "btnDownloadUrl",
                )

                download_button.click()

                downloaded_items.append(target_text)

                logger.info(
                    f"Download iniciado: {target_text}"
                )

                time.sleep(2)

            except Exception as e:
                logger.error(
                    f"Erro ao baixar {target.text}: {e}"
                )

                failed_items.append(
                    (target.text, str(e))
                )

        if failed_items:
            logger.warning(
                f"Total de falhas: {len(failed_items)}"
            )

            for item, error in failed_items:
                logger.warning(
                    f"- {item}: {error}"
                )

        return downloaded_items

    def run(
        self,
        source_url: str,
    ) -> List[str]:
        with self.managed_browser():
            self.navigate_to_source(source_url)
            self.expand_sections()

            targets = self.list_download_targets()

            logger.info(
                f"Total de arquivos encontrados: {len(targets)}"
            )

            matching_targets = self.filter_targets(
                targets
            )

            logger.info(
                f"Total de arquivos correspondentes: {len(matching_targets)}"
            )

            return self.download_matching_files(
                matching_targets
            )


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    create_directories()

    scraper = AnatelPerformanceScraper(
        download_directory=RAW_DIR,
    )

    matched_items = scraper.run(
        source_url=SOURCE_URL_IDA_ANATEL,
    )

    print(
        "Downloaded items:",
        len(matched_items),
    )