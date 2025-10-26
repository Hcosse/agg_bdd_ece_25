import csv

def save_to_csv(data, filename="output/annonces.csv"):
    keys = data[0].keys()
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)