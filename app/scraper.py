import time
import httpx
from bs4 import BeautifulSoup
from models import ScraperSettings, Product
from database import Database

class Scraper:
    def __init__(self, settings: ScraperSettings):
        self.settings = settings
        self.database = Database()
        self.scraped_products = []

    def scrape(self):
        for page in range(1, self.settings.page_limit + 1):
            if page == 1:
                url = "https://dentalstall.com/shop/"
            else:
                url = f"https://dentalstall.com/shop/page/{page}/"

            try:
                response = self.get_response(url)
                products = self.parse_products(response)
            except Exception as e:
                print(f"Error scraping page {page}: {e}")
                time.sleep(5)  # Simple retry mechanism
                continue
        
        self.notify_status()

    def get_response(self, url: str):
        with httpx.Client(proxies=self.settings.proxy) as client:
            response = client.get(url)
            response.raise_for_status()  # Raise error for bad responses
            return response.text

    def parse_products(self, html: str):

        
        soup = BeautifulSoup(html, 'html.parser')
        product_elements = soup.find_all('li', class_='product')

        products = []
        
        for product in product_elements:
            # Extract product title
            title_tag = product.find('h2', class_='woo-loop-product__title')
            title = title_tag.get_text(strip=True) if title_tag else "Unknown Product"
            
            # Extract product price (look for the 'ins' price tag first, if present)
            price_tag = product.find('ins')  # Sale price
            if not price_tag:
                price_tag = product.find('span', class_='woocommerce-Price-amount')  # Regular price
            
            price = price_tag.get_text(strip=True) if price_tag else "Price not available"
            
            # Extract product image (use 'data-lazy-src' if available, else fallback to normal 'src')
            image_tag = product.find('img')
            image_url = image_tag.get('data-lazy-src') if image_tag and image_tag.get('data-lazy-src') else image_tag.get('src')

            # Append the scraped product data to the products list
            products.append({
                "product_title": title,
                "product_price": price,
                "image_url": image_url
            })
        self.scraped_products = products
        return products

    def notify_status(self):
        print(f"Scraping completed. Total products scraped: {len(self.scraped_products)}")
