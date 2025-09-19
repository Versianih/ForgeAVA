from os import path
from time import sleep
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

DEBUG = True

class AvaManager:
    BASE_URL = "https://ava3.cefor.ifes.edu.br/"
    LOGIN_TIMEOUT = 10
    POST_ACTION_DELAY = 1

    _SELECTORS = {
        "login_username": "#username",
        "login_password": "#password",
        "activity_text_container": """
            document.getElementById("region-main")
                .firstElementChild
                .nextElementSibling
                .firstElementChild
                .nextElementSibling
                .nextElementSibling
                .nextElementSibling
                .lastElementChild
                .firstElementChild;
        """,
        "send_field_button": """
            document.getElementById("region-main")
                .firstElementChild
                .nextElementSibling
                .firstElementChild
                .nextElementSibling
                .firstElementChild
                .nextElementSibling
                .firstElementChild;
        """,
        "file_upload_enter_button": """
            document.getElementById("region-main")
                .firstElementChild
                .nextElementSibling
                .firstElementChild
                .nextElementSibling
                .nextElementSibling
                .firstElementChild
                .nextElementSibling
                .firstElementChild
                .nextElementSibling
                .firstElementChild
                .nextElementSibling
                .firstElementChild
                .nextElementSibling
                .firstElementChild
                .firstElementChild
                .nextElementSibling
                .nextElementSibling
                .firstElementChild
                .firstElementChild;
        """,
        "confirm_send_file": """
            document.getElementById("region-main")
                .firstElementChild
                .nextElementSibling
                .firstElementChild
                .nextElementSibling
                .nextElementSibling
                .firstElementChild
                .nextElementSibling
                .nextElementSibling
                .firstElementChild
                .nextElementSibling
                .firstElementChild
                .firstElementChild
                .nextElementSibling
                .firstElementChild
                .firstElementChild
                .firstElementChild;
        """,
        "edit_submission_button": """
            document.getElementById("region-main")
                .firstElementChild
                .nextElementSibling
                .firstElementChild
                .nextElementSibling
                .firstElementChild
                .nextElementSibling
                .nextElementSibling
                .firstElementChild;
        """
    }

    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.wait = None

    def _setup_driver(self, force_visible=False):
        chrome_options = Options()
        effective_headless = self.headless
        if force_visible:
            effective_headless = False
        if effective_headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, self.LOGIN_TIMEOUT)

    def _login(self, login, password):
        self.driver.get(self.BASE_URL + "login/index.php")
        username_field = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_field.send_keys(login)
        password_field = self.wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys(password)
        password_field.send_keys(Keys.TAB)
        password_field.send_keys(Keys.ENTER)
        sleep(self.POST_ACTION_DELAY)

    def _navigate_to_activity(self, activity_id):
        url = f"{self.BASE_URL}mod/assign/view.php?id={activity_id}"
        self.driver.get(url)

    @staticmethod
    def extract_id_from_url(url):
        parsed = urlparse(url.strip())
        query_params = parse_qs(parsed.query)
        activity_id = query_params.get("id", [None])[0]
        if not activity_id:
            raise RuntimeError("Parâmetro 'id' não encontrado na URL.")
        return activity_id

    def get_activity_text(self, login, password, activity_id):
        self._setup_driver(force_visible=DEBUG)
        try:
            self._login(login, password)
            self._navigate_to_activity(activity_id)
            text_container = self.driver.execute_script(self._SELECTORS["activity_text_container"])
            if not text_container:
                raise RuntimeError("Container de texto não encontrado.")
            paragraphs = text_container.find_elements(By.TAG_NAME, "p")
            text = "\n".join(p.text.strip() for p in paragraphs if p.text.strip())
            return text if text else "Nenhum texto encontrado."
        except Exception as e:
            raise RuntimeError(f"Falha ao extrair texto da atividade {activity_id}: {e}")
        finally:
            if self.driver:
                self.driver.quit()

    def submit_file(self, login, password, activity_id, file_path, filename):
        full_path = path.join(file_path, filename)
        if not path.isfile(full_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {full_path}")
        self._setup_driver()
        action = ActionChains(self.driver)
        try:
            self._login(login, password)
            self._navigate_to_activity(activity_id)
            send_button = self.driver.execute_script(self._SELECTORS["send_field_button"])
            if send_button:
                self.driver.execute_script("arguments[0].click();", send_button)
            else:
                raise RuntimeError("Botão de envio não encontrado.")
            sleep(2)
            upload_enter = self.driver.execute_script(self._SELECTORS["file_upload_enter_button"])
            if upload_enter:
                upload_enter.send_keys(Keys.ENTER)
            else:
                raise RuntimeError("Botão de upload não encontrado.")
            sleep(2)
            file_input = self.driver.find_element(By.NAME, "repo_upload_file")
            file_input.send_keys(full_path)
            sleep(1)
            action.send_keys(Keys.TAB * 6, Keys.ENTER).perform()
            sleep(1)
            confirm_button = self.driver.execute_script(self._SELECTORS["confirm_send_file"])
            if confirm_button:
                confirm_button.send_keys(Keys.ENTER)
            else:
                raise RuntimeError("Botão de confirmação de envio não encontrado.")
            sleep(1)
            edit_button = self.driver.execute_script(self._SELECTORS["edit_submission_button"])
            if edit_button:
                self.driver.execute_script("arguments[0].click();", edit_button)
            else:
                raise RuntimeError("Botão de visualização de envios não encontrado.")
            while True:
                try:
                    self.driver.title
                    sleep(1)
                except Exception:
                    break
            return True
        except Exception:
            return False
        finally:
            if self.driver:
                self.driver.quit()