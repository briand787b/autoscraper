import scrape


def main():
    for listings in scrape.scrape('ferrari', 'f40', {}):
        print(f'saving {listings} to db')
