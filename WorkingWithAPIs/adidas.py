from curl_cffi import requests
import os
from pydantic import BaseModel
from rich import print

class SearchItem(BaseModel):
    productId: str
    modelId: str
    price: float
    salePrice: float
    displayName: str
    rating: float | None

class SearchResponse(BaseModel):
    count: int
    startIndex: int
    searchTerm: str
    items: list[SearchItem]

class ItemDetail(BaseModel):
    id: str
    name: str
    product_description: dict
    pricing_information: dict

def new_session():
    session = requests.Session(impersonate="chrome", proxy=os.getenv("stickyproxy"))
    return session

def search_api(session: requests.Session, query: str, start_num: int):
    url = f"https://www.adidas.com/api/plp/content-engine/search?query={query}&start={str(start_num)}"
    resp = session.get(url)
    resp.raise_for_status()
    search = SearchResponse(**resp.json()["raw"]["itemList"])
    return search

def detail_api(session: requests.Session, item: SearchItem):
    url = f"https://www.adidas.com/api/products/{item.productId}"
    resp = session.get(url)
    resp.raise_for_status()
    product = ItemDetail(**resp.json())
    return product

def main():
    session = new_session()
    search = search_api(session, "hoody", 1)

    for item in search.items:
        prod = detail_api(session, item)
        print(prod.name)

if __name__ == "__main__":
    main()