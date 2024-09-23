from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from models import ScraperSettings
from scraper import Scraper

app = FastAPI()
security = HTTPBearer()

@app.post("/scrape")
async def scrape(settings: ScraperSettings):

    scraper = Scraper(settings)
    scraper.scrape()
    print(scraper.scraped_products)
    return scraper.scraped_products
