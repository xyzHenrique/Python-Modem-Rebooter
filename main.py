"""
Created by: Henrique Rodrigues Pereira <https://github.com/RIick-013> 
 
RIick - ")
"""

### Bibliotecas nativas ###
import json
import requests
import time
import sys

### Bibliotecas de terceiros ###
import colorama
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

### Bibliotecas locais ###
from informations import Informations
from logger import *

class ModemRebooter:
    def __init__(self, config_path):
        # Inicializa as bibliotecas de terceiros
        colorama.init()

        # Inicializa as bibliotecas locais
        self.logger = Logger()
        self.logger.initialize()

        # Carrega as configurações do arquivo JSON
        with open(config_path) as file:
            data = json.load(file)
            self.IP = data["IP"]
            self.username = data["username"]
            self.password = data["password"]

        # Configurações do driver
        self.chrome_driver = ".\chromedriver.exe"
        self.options = webdriver.ChromeOptions()

        # Informações do script no log
        self.logger.write(f"{Informations['app_name']} - ({Informations['app_version']}) by {Informations['app_owner']}", "DEBUG")

    def test_internet_connectivity(self, max_retries):
        # Verifica a conectividade com a internet com um número máximo de tentativas
        for retry in range(1, max_retries + 1):
            self.logger.write(f"Tentando conexão com o IP: ({self.IP})", "INFO")
            try:
                response = requests.get(f"http://{self.IP}/", timeout=5)

                if response.status_code == 200:
                    self.logger.write(f"Conectado com sucesso ao IP: ({self.IP})", "INFO")
                    return True
            except requests.RequestException as error:
                self.logger.write(f"Ocorreu um erro ao conectar no IP {self.IP}\nERRO:\n{error}", "WARNING")

            if retry < max_retries:
                self.logger.write(f"Tentativa {retry} de {max_retries}. Tentando novamente...", "WARNING")
                time.sleep(5)

        return False

    def login_and_execute_js(self):
        def quit(message=""):
            # Finaliza o script com uma mensagem (ou sem mensagem)
            if message:
                self.logger.write(message, "INFO")
            else:
                self.logger.write("O aplicativo será finalizado em breve, aguarde...", "INFO")

            time.sleep(10)
            driver.quit()
            sys.exit()

        # Executa a verificação de conexão
        if not self.test_internet_connectivity(5):
            self.logger.write(f"Falha na conexão no IP: ({self.IP}) Abortando a execução do programa, aguarde...", "CRITICAL")
            quit()

        try:
            driver = webdriver.Chrome(executable_path=self.chrome_driver, options=self.options)
        except Exception as error:
            self.logger.write(f"Ocorreu um erro na execução do driver\nERRO:\n{error}", "CRITICAL")
            driver.quit()
            return

        # Executa as ações de login
        def login_actions():
            try:
                driver.get(f"http://{self.IP}/index.html")

                username_element = driver.find_element(By.ID, "login_name")
                password_element = driver.find_element(By.ID, "login_passwd")
                button_element = driver.find_element(By.ID, "set_system_user_login")

                username_element.send_keys(self.username)
                password_element.send_keys(self.password)
                button_element.click()

                WebDriverWait(driver, 10)

                print()
                return True

            except Exception as error:
                self.logger.write(f"Ocorreu um erro na execução da ação de login\nERRO:\n{error}", "CRITICAL")
                return False

        # Executa as ações de reboot
        def reboot_actions():
            try:
                driver.get(f"http://{self.IP}/system/reboot.html")

                time.sleep(5)
                driver.execute_script("""SetSystemWanPower()""")

                self.logger.write(f"Script executado! Validando reinicialização, aguarde!", "INFO")
                time.sleep(5)

                # Verifica se o modem foi reiniciado
                if not self.test_internet_connectivity(1):
                    # Se não for verdadeiro, o modem foi reiniciado
                    return True
                else:
                    # Se for verdadeiro, o modem não foi reiniciado e tenta reiniciar novamente
                    self.logger.write(f"A reinicialização falhou. Tentando novamente...", "WARNING")
                    return self.login_and_execute_js()

            except Exception as error:
                self.logger.write(f"Ocorreu um erro na execução da ação de reboot\nERRO:\n{error}", "CRITICAL")
                return False

        if login_actions():
            self.logger.write("Login realizado com sucesso!", "SUCCESS")

            if reboot_actions():
                self.logger.write("Reboot realizado com sucesso!", "SUCCESS")

        quit()

if __name__ == "__main__":
    config_path = "config.json"
    rebooter = ModemRebooter(config_path)
    rebooter.login_and_execute_js()
