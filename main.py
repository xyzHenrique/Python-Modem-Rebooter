"""
Created by: Henrique Rodrigues Pereira <https://github.com/RIick-013> 
 
RIick - ")
"""

SCRIPT_VERSION = "2.5 - 26/07/23"

### Native libraries ###
import json, requests, time

### Third-party libraries ###
import colorama
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

### Local libraries ###
from informations import Informations
from logger import *

class ModemRebooter:
    def __init__(self, config_path):
        # Initialize third-party libraries
        colorama.init()

        # Initialize local libraries
        self.logger = Logger()
        self.logger.initialize()
        
        # Load configuration from the JSON file
        with open(config_path) as file:
            data = json.load(file)
            self.IP = data["IP"]
            self.username = data["username"]
            self.password = data["password"]

        self.chrome_driver = ".\chromedriver.exe"
        self.options = webdriver.ChromeOptions()
        
        self.max_retries = 5
        
        # Log script information
        self.logger.write(f"{Informations['app_name']} ({SCRIPT_VERSION}) by {Informations['app_owner']}", "DEBUG")

    def test_internet_connectivity(self):
        # Check internet connectivity up to 5 times
       
        for retry in range(1, self.max_retries + 1):
            try:
                # Test internet connectivity by making a request to google.com
                self.logger.write(f"Conectando ao IP: ({self.IP})", "INFO")
                response = requests.get(f"http://{self.IP}/", timeout=5)
                
                if response.status_code == 200:
                    self.logger.write(f"Conectado ao IP: ({self.IP})", "INFO")
                    return True
            except requests.RequestException:
                pass

            # Print the message when retrying
            if retry < self.max_retries:
                self.logger.write(f"Tentando reconectar {retry} de {self.max_retries}...", "WARNING")
                time.sleep(5)

        return False

    def login_and_execute_js(self):
        # Check internet connectivity before proceeding
        if not self.test_internet_connectivity():
            self.logger.write(f"Falha na conexão no IP: ({self.IP}) Abortando a execução do programa, aguarde.", "CRITICAL")
            time.sleep(10)
            return

        try:
            driver = webdriver.Chrome(executable_path=self.chrome_driver, options=self.options)
        except Exception as e:
            self.logger.write(f"Ocorreu um erro no driver: {e}", "WARNING")
            driver.quit()
            return

        try:
            driver.get(f"http://{self.IP}/index.html")

            # Find the login elements
            username_element = driver.find_element(By.ID, "login_name")
            password_element = driver.find_element(By.ID, "login_passwd")
            login_button = driver.find_element(By.ID, "set_system_user_login")

            # Input login credentials
            username_element.send_keys(self.username)
            password_element.send_keys(self.password)

            # Click the login button
            login_button.click()

            print()
            self.logger.write("Login realizado com sucesso!", "INFO")
            
            WebDriverWait(driver, 10)

            # Access the reboot page
            driver.get(f"http://{self.IP}/system/reboot.html")

            # Execute script function to reboot modem
            time.sleep(2)
            driver.execute_script("""SetSystemWanPower()""")

            self.logger.write(f"Script executado! Validando reinicialização...", "INFO")

            self.max_retries = 3

            # Wait for a short period before checking internet connectivity again
            time.sleep(3)

            # Check internet connectivity after reboot
            if not self.test_internet_connectivity():
                # Reboot was successful
                self.logger.write(f"Modem reiniciado com sucesso!", "SUCCESS")
            else:
                # Reboot failed, retrying the script
                self.logger.write(f"A reinicialização falhou. Tentando novamente...", "WARNING")
                driver.quit()
                self.login_and_execute_js()

            # Wait for a short period before quitting the driver
            time.sleep(3)
            driver.quit()

        except Exception as e:
            self.logger.write(f"Ocorreu um erro na execução principal: {e}", "CRITICAL")

if __name__ == "__main__":
    config_path = "config.json"
    rebooter = ModemRebooter(config_path)
    rebooter.login_and_execute_js()
"""
Created by: Henrique Rodrigues Pereira <https://github.com/RIick-013> 
 
RIick - ")
"""

SCRIPT_VERSION = "2.5 - 26/07/23"

### Native libraries ###
import json, requests, time

### Third-party libraries ###
import colorama
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

### Local libraries ###
from informations import Informations
from logger import *

class ModemRebooter:
    def __init__(self, config_path):
        # Initialize third-party libraries
        colorama.init()

        # Initialize local libraries
        self.logger = Logger()
        self.logger.initialize()
        
        # Load configuration from the JSON file
        with open(config_path) as file:
            data = json.load(file)
            self.IP = data["IP"]
            self.username = data["username"]
            self.password = data["password"]

        self.chrome_driver = ".\chromedriver.exe"
        self.options = webdriver.ChromeOptions()
        
        self.max_retries = 5
        
        # Log script information
        self.logger.write(f"{Informations['app_name']} ({SCRIPT_VERSION}) by {Informations['app_owner']}", "DEBUG")

    def test_internet_connectivity(self):
        # Check internet connectivity up to 5 times
       
        for retry in range(1, self.max_retries + 1):
            try:
                # Test internet connectivity by making a request to google.com
                self.logger.write(f"Conectando ao IP: ({self.IP})", "INFO")
                response = requests.get(f"http://{self.IP}/", timeout=5)
                
                if response.status_code == 200:
                    self.logger.write(f"Conectado ao IP: ({self.IP})", "INFO")
                    return True
            except requests.RequestException:
                pass

            # Print the message when retrying
            if retry < self.max_retries:
                self.logger.write(f"Tentando reconectar {retry} de {self.max_retries}...", "WARNING")
                time.sleep(5)

        return False

    def login_and_execute_js(self):
        # Check internet connectivity before proceeding
        if not self.test_internet_connectivity():
            self.logger.write(f"Falha na conexão no IP: ({self.IP}) Abortando a execução do programa, aguarde.", "CRITICAL")
            time.sleep(10)
            return

        try:
            driver = webdriver.Chrome(executable_path=self.chrome_driver, options=self.options)
        except Exception as e:
            self.logger.write(f"Ocorreu um erro no driver: {e}", "WARNING")
            driver.quit()
            return

        try:
            driver.get(f"http://{self.IP}/index.html")

            # Find the login elements
            username_element = driver.find_element(By.ID, "login_name")
            password_element = driver.find_element(By.ID, "login_passwd")
            login_button = driver.find_element(By.ID, "set_system_user_login")

            # Input login credentials
            username_element.send_keys(self.username)
            password_element.send_keys(self.password)

            # Click the login button
            login_button.click()

            print()
            self.logger.write("Login realizado com sucesso!", "INFO")
            
            WebDriverWait(driver, 10)

            # Access the reboot page
            driver.get(f"http://{self.IP}/system/reboot.html")

            # Execute script function to reboot modem
            time.sleep(2)
            driver.execute_script("""SetSystemWanPower()""")

            self.logger.write(f"Script executado! Validando reinicialização...", "INFO")

            self.max_retries = 3

            # Wait for a short period before checking internet connectivity again
            time.sleep(3)

            # Check internet connectivity after reboot
            if not self.test_internet_connectivity():
                # Reboot was successful
                self.logger.write(f"Modem reiniciado com sucesso!", "SUCCESS")
            else:
                # Reboot failed, retrying the script
                self.logger.write(f"A reinicialização falhou. Tentando novamente...", "WARNING")
                driver.quit()
                self.login_and_execute_js()

            # Wait for a short period before quitting the driver
            time.sleep(3)
            driver.quit()

        except Exception as e:
            self.logger.write(f"Ocorreu um erro na execução principal: {e}", "CRITICAL")

if __name__ == "__main__":
    config_path = "config.json"
    rebooter = ModemRebooter(config_path)
    rebooter.login_and_execute_js()
