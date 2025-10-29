from PySide6.QtWidgets import QApplication,  QWidget, QPushButton, QVBoxLayout, QMainWindow
from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtGui import QIcon
import sys
from playwright.sync_api import sync_playwright, Playwright
from time import sleep



def browser_action():
    def run(playwright: Playwright):
        #inicia navegador e pega contexto inicial
        Chromium = playwright.chromium
        browser = Chromium.launch(headless=False)
        context = browser.new_context(storage_state="state.json")
        page = context.new_page()
        page.goto('https://www.facebook.com/groups/joins/?nav_source=tab&ordering=viewer_added')
        context.storage_state(path="state.json")
        list = page.locator('.x6s0dn4')
        itens = page.locator('[aria-label="Ver grupo"]')
        
        #itera sobre cada item dos grupos
        for i in range(itens.count()):
            #aqui vai entrar a UI porque quero a opção de seleção dos grupos a enviar
            try:
                itens.nth(i).click()
                page.wait_for_load_state("load")
                card = page.locator('.x1yztbdb')
                card.get_by_role('button').filter(has_text='Escreva algo...').first.click()
                page.wait_for_load_state("load")
                textbox = page.locator('[role="textbox"][aria-placeholder="Crie um post público…"]')
                texto = open("mensagem.txt" , "r", encoding="utf-8").read()
                textbox.fill(texto)
                page.locator('[aria-label="Postar"]').click()
                page.locator('[role="textbox"][aria-placeholder="Crie um post público…"]').wait_for(state='hidden')
            except(TimeoutError):
                page.wait_for_load_state("load")
                page.go_back()
                page.wait_for_load_state("load")

        browser.close()


    with sync_playwright() as playwright:
        run(playwright)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Facebook Posts ")
        self.resize(600,400)
        panel = QWidget(self);
        panel.setObjectName('panel')
        self.setCentralWidget(panel)
        panel.setLayout(QVBoxLayout())
        self.setStyleSheet('#panel{background:#FFFFFF; border-radius: 12px}')

class ButtonHome(QPushButton):
    
    def __init__(self):
        super().__init__()
        self.start_btn = QPushButton("Iniciar", self)
        self.start_btn.setObjectName("btnStart")
        self.start_btn.setEnabled(True)
        self.panel.addWidget(self.start_btn)
        self.start_btn.clicked.connect(self.on_start)


def main():

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__": 
    main()
