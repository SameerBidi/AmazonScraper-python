import scraper
import json

print(json.dumps(scraper.get_best_sellers_list(), indent=2))