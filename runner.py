from scrapers.osteoweb_fr import get_info_remplacement
import pandas as pd

if __name__ == "__main__":
    
    data = get_info_remplacement()

    df = pd.DataFrame(data)
    df.to_csv(r"C:\Users\hugoc\Documents\ECE\Aggregation de données\Projet final\output\test.csv", index=False)