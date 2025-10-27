from scrapers.osteopathe_syndicat_fr import scrape_osteopathe_syndicat
from scrapers.osteofrance_com import scrape_osteofrance

all_data = []
all_data += scrape_osteopathe_syndicat()
all_data += scrape_osteofrance()

from storage.storage import save_to_csv
save_to_csv(all_data)
