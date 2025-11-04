from PySide6.QtWidgets import QApplication, QWidget , QPushButton, QVBoxLayout, QMainWindow
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
import sys
from playwright.sync_api import sync_playwright, Playwright, Error


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
        page.set_default_timeout(30000)
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
                with page.expect_file_chooser(timeout=5000) as fc_info:
                    page.locator('[role="button"][aria-label="Foto/vídeo"]').click()
                file_chooser = fc_info.value
                file_chooser.set_files('./Video_Project.mp4')
                page.locator('[aria-label="Postar"]').click()
                page.locator('[role="textbox"][aria-placeholder="Crie um post público…"]').wait_for(state='hidden')
                page.go_back()
            except(TimeoutError, Error):            
                page.go_back()


        browser.close()


    with sync_playwright() as playwright:
        run(playwright)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Facebook Posts")
        self.resize(300,150)
        self.setStyleSheet('background-color: #1877F2; border-radius: 25px;')

        central = QWidget(self)
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0,0,0,0)

        self.setWindowIcon(QIcon('./facebook.png'))

        buttons_box = QWidget()

        vbox = QVBoxLayout(buttons_box)
        vbox.setContentsMargins(0,0,0,0)
        vbox.setSpacing(10)

        btn2 = MainButton('Editar texto')
        btn3 = MainButton('Executar')

        btn3.clicked.connect(browser_action)

        vbox.addWidget(btn2)
        vbox.addWidget(btn3)


        main_layout.addWidget(buttons_box, alignment=Qt.AlignCenter)


class MainButton(QPushButton):

    def __init__(self, text=""):
        super().__init__(text)
        self.setStyleSheet(""" 
                        QPushButton {
                            background-color: #365FCF;
                            border-radius: 5px;
                            color: white;
                            border: 1px solid black;
                        }
                           
                        QPushButton:hover {
                            background-color: #4c76ff;
                        }
                        
                        QPushButton:pressed {
                        
                            background-color: #2948a8;
                        
                        }
                           
                           """)
        self.setFixedSize(100,30)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__": 
    main()
