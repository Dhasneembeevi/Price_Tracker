from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from scraper import fetch_amazon_price, fetch_flipkart_price

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/get-prices")
async def get_prices(request: Request):
    data = await request.json()
    product_name = data.get("product_name", "")
    amazon_price = fetch_amazon_price(product_name)
    flipkart_price = fetch_flipkart_price(product_name)
    return {
        "amazon_price": amazon_price,
        "flipkart_price": flipkart_price
    }