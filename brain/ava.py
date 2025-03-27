# Python Libs
import os
import time
from urllib.parse import urlparse, parse_qs

# Libs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def get_ava_text(login, password, id):
    # AVA Settings
    WEBSITE_URL = "https://ava3.cefor.ifes.edu.br/"
    ACTIVITY_URL = f"https://ava3.cefor.ifes.edu.br/mod/vpl/view.php?id={id}"
    
    # Selenium Settings
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(WEBSITE_URL)
        wait = WebDriverWait(driver, 10)

        user_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        user_field.send_keys(login)

        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys(password)
        
        password_field.send_keys(Keys.TAB)
        password_field.send_keys(Keys.ENTER)

        time.sleep(1)

        driver.get(ACTIVITY_URL)

        # Find the container that holds all the text paragraphs and copy the text
        element = driver.execute_script("""
            return document.getElementById("region-main")
                .firstElementChild
                .nextElementSibling
                .firstElementChild
                .nextElementSibling
                .nextElementSibling
                .nextElementSibling
                .lastElementChild
                .firstElementChild;
        """)

        paragraphs = element.find_elements("tag name", "p")
        ava_text = "\n".join(paragraph.text for paragraph in paragraphs)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return "error"
    finally:
        driver.quit()
        return ava_text


def send_file_to_ava(login, password, id, file_path, file):
    # AVA Settings
    WEBSITE_URL = "https://ava3.cefor.ifes.edu.br/"
    ACTIVITY_URL = f"https://ava3.cefor.ifes.edu.br/mod/vpl/view.php?id={id}"
    full_file_path = os.path.join(file_path, file)
    
    # Selenium Settings
    driver = webdriver.Chrome()
    action = ActionChains(driver)

    try:
        driver.get(WEBSITE_URL)
        wait = WebDriverWait(driver, 10)

        user_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        user_field.send_keys(login)

        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys(password)
        
        password_field.send_keys(Keys.ENTER)

        time.sleep(2)

        driver.get(ACTIVITY_URL)

        send_field_button = driver.execute_script("""
            return document.getElementById("region-main")
                .firstElementChild
                .nextElementSibling
                .firstElementChild
                .nextElementSibling
                .firstElementChild
                .nextElementSibling
                .firstElementChild;
        """)

        if send_field_button:
            driver.execute_script("arguments[0].click();", send_field_button)
        else:
            raise Exception("Botão de envio não encontrado.")

        time.sleep(2)

        # Find the button to choose a file
        send = driver.execute_script("""
            return document.getElementById("region-main")
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
                .firstElementChild
        """)
        
        send.send_keys(Keys.ENTER)

        time.sleep(2)

        # Select file
        send_button = driver.find_element(By.NAME, "repo_upload_file")
        send_button.send_keys(full_file_path)

        time.sleep(1)

        # Click the first submit button to save the file
        action.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER).perform()

        time.sleep(1)

        # Find the button to send the file and click
        send_file = driver.execute_script("""
            return document.getElementById("region-main")
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
                .firstElementChild
        """)
        send_file.send_keys(Keys.ENTER)

        time.sleep(1)

        edit_submit = driver.execute_script("""
            return document.getElementById("region-main")
                .firstElementChild
                .nextElementSibling
                .firstElementChild
                .nextElementSibling
                .firstElementChild
                .nextElementSibling
                .nextElementSibling
                .firstElementChild
        """)

        if edit_submit:
            driver.execute_script("arguments[0].click();", edit_submit)
        else:
            raise Exception("Botão de visualizar envios não encontrado.")
        
        while True:
            try:
                driver.title
                time.sleep(1)
            except Exception as e:
                break
        return 0

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return "error"
    
    finally:
        driver.quit()


def get_id(url):
    try:
        parsed_url = urlparse(url)
        query_parameters = parse_qs(parsed_url.query)
        id = query_parameters.get("id", [None])[0]
        
        return id
    except Exception as e:
        print(f"ocorreu um erro {e}")
        return "error"