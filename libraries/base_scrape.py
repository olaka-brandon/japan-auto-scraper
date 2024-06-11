# A.py
import httpx
import csv
import time
from selectolax.parser import HTMLParser

class Scraper:
    def __init__(self, fieldnames, output_file) -> None:
        self.fieldnames = fieldnames
        self.output_file = output_file

    def get_html(self, url):
        try:
            response = httpx.get(url, timeout=30)
            response.raise_for_status()
            return HTMLParser(response.text)
        except httpx.RequestError as e:
            print(f"An error occurred while requesting {e.request.url!r}.")
        except httpx.HTTPStatusError as e:
            print(f"Error response {e.response.status_code} while requesting {e.request.url!r}.")
    
    def clean_text(self, text):
        """Clean up text by removing excessive whitespace and line breaks."""
        return ' '.join(text.split())

    def to_csv(self, res, mode='w', write_header=False):
        with open(self.output_file, mode, newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            if write_header:
                writer.writeheader()
            writer.writerows(res)
    
    def main(self, start_page, end_page, url_template):
        all_results = []
        for page in range(start_page, end_page + 1):
            url = url_template.format(page=page)
            html = self.get_html(url)
            if html:
                print(f"Successfully scraped page {page}")
                res = self.parser(html)
                all_results.extend(res)
                time.sleep(2)  # Be respectful to the server by adding a delay
        
        self.to_csv(all_results, mode='w', write_header=True)
        print("Data written to CSV file.")
    
    def parser(self, html):
        raise NotImplementedError("Subclasses should implement this method")
