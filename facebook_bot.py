from playwright.sync_api import sync_playwright, Playwright
from time import sleep


def run(playwright: Playwright):
    Chromium = playwright.chromium
    browser = Chromium.launch(headless=False)
    context = browser.new_context(storage_state="state.json")
    page = context.new_page()
    page.goto('https://www.facebook.com/groups/joins/?nav_source=tab&ordering=viewer_added')
    input('Pressione enter apos o login')
    context.storage_state(path="state.json")
    list = page.locator('.x6s0dn4')
    itens = page.locator('[aria-label="Ver grupo"]')
    
    for i in range(itens.count()):
        itens.nth(i).click()
        page.wait_for_load_state("load")
        card = page.locator('.x1yztbdb')
        card.get_by_role('button').filter(has_text='Escreva algo...').first.click()
        page.wait_for_load_state("load")
        textbox = page.locator('.x1lliihq').filter(getattr='[role=none]')
        print(textbox)
        

        page.wait_for_load_state("load")
        input('Pressione enter apos o login')

        browser.close()

    
    



with sync_playwright() as playwright:
    run(playwright)
    