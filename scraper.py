from playwright.sync_api import sync_playwright


def verify_product(name, title):
    for word in (name.lower()).split():
        if word not in (title.lower()).split():
            return False
    return True

def scrap_kabum(playwright, product):
    url = 'https://www.kabum.com.br'
    
    browser = playwright.chromium.launch()
    page = browser.new_page()
    page.goto(url + '/busca/' + product.lower().replace(' ', '-'))

    final_product = {}
    products = page.locator('xpath=//*[@id="listing"]/div[3]/div/div/div[2]/div[1]/main/a').all()
    for p in products:
        name = p.locator('span.text-sm').text_content()
        price = float(p.locator('xpath=div[4]/div/span[2]').text_content().replace('.', '').replace(',', '.'))
        href = p.get_attribute('href')

        if verify_product(product, name) and final_product.get('price', price) >= price:
            final_product = {
                'name': name,
                'price': price,
                'href': url + href
            }

    browser.close()


product = 'Asus Vivobook 15 16gb 512gb ryzen 7'
with sync_playwright() as playwright:
    scrap_kabum(playwright, product)
