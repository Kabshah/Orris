# import requests
# from dotenv import load_dotenv
# load_dotenv()
# import os

# url = "https://api.scrapingdog.com/google"

# params = {
#     "api_key": os.getenv("SCRAPINGDOG_API_KEY"),
#     "results": 10,
#     "country": "us",
#     "advance_search": "true",
#     "domain": "google.com"
#   }

# response = requests.get(url, params=params)

# if response.status_code == 200:
#       data = response.json()
#       print(data)
# else:
#       print(f"Request failed with status code: {response.status_code}")

import os
from dotenv import load_dotenv
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

load_dotenv()

class ScrapingDogSearchInput(BaseModel):
    """Input for ScrapingDog search tool."""
    query: str = Field(..., description="Search query to scrape")
    results: int = Field(default=10, description="Number of results to return")
    country: str = Field(default="us", description="Country for search")

class scrapingdog_tool(BaseTool):
    name: str = "ScrapingDog Search"
    description: str = "Search and scrape data using ScrapingDog API"
    args_schema: Type[BaseModel] = ScrapingDogSearchInput

    def _run(self, query: str, results: int = 10, country: str = "us") -> str:
        import requests
        
        url = "https://api.scrapingdog.com/google"
        params = {
            "api_key": os.getenv("SCRAPINGDOG_API_KEY"),
            "q": query,
            "gl": country,
            "num": results
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return str(data)
            else:
                return f"Request failed with status code: {response.status_code}"
        except Exception as e:
            return f"Error during scraping: {str(e)}"