from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape():

    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path)
    #if you want to use headless actions
    #browser = Browser('chrome', **executable_path, headless=False)
    nasa_data = {}
    # nasa new products
    nasa_url = "https://www.nasa.gov/webbfirstimages"
    browser.visit(nasa_url)

    html = browser.html
    soup = bs(html, 'html.parser')
    products = soup.find_all('div', class_="dnd-drop-wrapper")

    nasa_products = []
    for product in products:
        # Error handling
        try:
            # Extract href
            href = product.a['href']

            browser.visit(href)
            html = browser.html
            soup = bs(html, 'html.parser')

            product_title = soup.find('h1').text
            product_desc = soup.find('div', class_="text").li.text
            product_img = soup.find('img', class_="feature-image")['src']

            nasa_dict = {
                "product_src": product_img,
                "product_title": product_title,
                "product_desc": product_desc
            }
            nasa_products.append(nasa_dict)
        except Exception as e:
            print(e)

    # nasa mars Facts
    facts_url = "https://galaxyfacts-mars.com/"
    tables = pd.read_html(facts_url)

    fact_df = tables[0]
    fact_df = fact_df.rename(columns={0: "nasa - Earth Comparison", 1: "nasa", 2: "Earth"})

    fact_df = fact_df.drop([0, 0])
    fact_df.set_index("nasa - Earth Comparison", inplace=True)

    html_table = fact_df.to_html()
    html_table.replace('\n', '')

    # nasa Hemispheres
    hemis_url = "https://marshemispheres.com/"
    browser.visit(hemis_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    product = soup.find_all('div', class_="item")

    hemisphere_products = []
    for image in product:
        # Error handling
        try:
            # Extract href
            href = image.a['href']
            title = image.h3.text
            desc = image.p.text

            browser.visit(hemis_url + href )
            html = browser.html
            soup = bs(html, 'html.parser')

            image_url = hemis_url + soup.find('img',class_="wide-image")['src']
            hemisphere_dict = {
                "title": title,
                "imgurl": image_url,
                "desc": desc
            }
            hemisphere_products.append(hemisphere_dict)


        except Exception as e:
            print(e)

    # Store data in a dictionary
    nasa_data = {
        "hemisphere_products": hemisphere_products,
        "html_table": html_table,
        "discoveries": nasa_products
    }

    # Quit the browser
    browser.quit()

    return nasa_data
