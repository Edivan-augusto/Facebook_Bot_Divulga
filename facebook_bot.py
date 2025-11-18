from PySide6.QtWidgets import QApplication, QWidget , QPushButton, QVBoxLayout, QMainWindow
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
import sys
from playwright.sync_api import sync_playwright, Playwright, Error
import time

def browser_action():

    def run(playwright: Playwright):
        #inicia navegador e pega contexto inicial
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(storage_state="./state.json")
        page = context.new_page()
        
        page.goto('https://www.facebook.com/groups/joins/?nav_source=tab&ordering=viewer_added')
        
        scroll_ate_parar_de_carregar(page)

        itens = page.locator('[aria-label="Ver grupo"]')
        
        total = itens.count()
        item_atual = 0

        page.set_default_timeout(30000)
        #itera sobre cada item dos grupos
        for i in range(50):
            #aqui vai entrar a UI porque quero a opção de seleção dos grupos a enviar
            try:
                itens.nth(item_atual).click()
               
                page.get_by_role("button", name="Escreva algo...").click()
                page.get_by_role("textbox").click()

                with open("./mensagem.txt", "r", encoding="utf-8") as f:
                    msg = f.read().strip()

                textbox = page.get_by_role("textbox")
                textbox.click()
                textbox.fill(msg)

                with page.expect_file_chooser(timeout=5000) as fc_info:
                    page.locator('[role="button"][aria-label="Foto/vídeo"]').click()
                file_chooser = fc_info.value
                file_chooser.set_files('./anuncio.png')
                
                page.get_by_role("button", name="Postar").click()
                page.wait_for_load_state("networkidle")

                page.locator('[role="textbox"][aria-placeholder="Crie um post público…"]').wait_for(state='hidden')
                
                if page.locator('[role="textbox"][aria-placeholder="Escreva algo..."]'):
                    page.locator('[role="textbox"][aria-placeholder="Escreva algo..."]').wait_for(state='hidden')

                page.go_back()
                
                item_atual += 1
                print(item_atual)

                if(i == 49):
                    browser.close()
                    context.close()
                    page , browser, context, itens = abrindo_navegador(playwright)
                    i = 0
                
                if (item_atual >= total):
                    break

            except(TimeoutError, Error):
                page.go_back()
                item_atual += 1
           
        
        context.storage_state(path="state.json")
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

        self.setWindowIcon(QIcon('./anuncio.png'))

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

def scroll_ate_parar_de_carregar(page, pausa=1.0, max_loops=50):
    last_count = -1
    loops = 0

    while loops < max_loops:
        # desce até o final da página
        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(pausa)

        count = page.get_by_role("listitem").count()
        

        # se não aumentou, provavelmente acabou
        if count == last_count:
            
            break

        last_count = count
        loops += 1

def clicar_sair(page, timeout=2000) -> bool:
    try:
        page.get_by_text("Sair", exact=True).click(timeout=timeout)
        return True
    except:
        return False

def abrindo_navegador(playwright: Playwright):
        #inicia navegador e pega contexto inicial
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(storage_state="./state.json")
        page = context.new_page()
        
        page.goto('https://www.facebook.com/groups/joins/?nav_source=tab&ordering=viewer_added')
        
        scroll_ate_parar_de_carregar(page)

        page.set_default_timeout(30000)

        itens = page.locator('[aria-label="Ver grupo"]')
        
        return page , browser, context, itens

def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__": 
    main()
