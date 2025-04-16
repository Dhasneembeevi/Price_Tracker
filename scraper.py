import time
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO)

def get_driver():
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(options=options)
    return driver
from selenium.webdriver.common.by import By
import time
def fetch_amazon_price(product_name):
    try:
        driver = get_driver()
        search_url = f"https://www.amazon.in/s?k={product_name.replace(' ', '+')}"
        logging.info(f"Amazon URL: {search_url}")
        
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        driver.get(search_url)
        
        time.sleep(5)
        
        results = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.s-main-slot div[data-component-type="s-search-result"]'))
        )

        price = "Price not found"

        for item in results:
            try:
                title = item.find_element(By.CSS_SELECTOR, "h2 span").text
                price_tag = item.find_element(By.CSS_SELECTOR, "span.a-price-whole")
                if price_tag:
                    price = price_tag.text.strip()
                    break
                
            except Exception as e:
                logging.error(f"Error fetching price for item: {e}")
        
        driver.quit()
        
        if price != "Price not found":
            return "₹" + price
        else:
            return "Price not found"
    
    except Exception as e:
        logging.error(f"Amazon error: {e}")
        driver.quit()
        return "Failed to fetch page"


def fetch_flipkart_price(product_name):
    try:
        driver = get_driver()
        search_url = f"https://www.flipkart.com/search?q={product_name.replace(' ', '+')}"
        logging.info(f"Flipkart URL: {search_url}")
        driver.get(search_url)

        try:
            close_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button._2KpZ6l._2doB4z"))
            )
            close_btn.click()
            logging.info("Login popup closed")
        except:
            logging.info("Login popup not shown or already closed.")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div._4b5DiR"))
        )

        soup = BeautifulSoup(driver.page_source, 'lxml')
        price_tag = soup.select_one("div._4b5DiR")

        driver.quit()

        if price_tag:
            return price_tag.text.strip()
        else:
            return "Price not found"
    except Exception as e:
        logging.error(f"Flipkart error: {e}")
        driver.quit()  
        return "Failed to fetch page"
