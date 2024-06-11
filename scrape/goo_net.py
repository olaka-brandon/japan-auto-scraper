from libraries.base_scrape import Scraper
from dataclasses import dataclass, asdict

@dataclass
class Dict_Goo_Net:
    title: str
    price: str
    details: str  # Contains date of manufacture, colour, mileage, displacement, drive, transmission

class Goo_Net(Scraper):
    def __init__(self) -> None:
        fieldnames = ["title", "price", "details"]
        output_file = "data/goo_net_data.csv"
        super().__init__(fieldnames, output_file)

    def parser(self, html):
        cars = html.css("div.sub-content")
        results = []
        
        for item in cars:
            title_elem = item.css_first("h3.title")
            price_elem = item.css_first("p.price.currency-jpy")
            details_elem = item.css_first("ul.details")
            
            title = self.clean_text(title_elem.text()) if title_elem else None
            price = self.clean_text(price_elem.text()) if price_elem else None
            details = self.clean_text(details_elem.text()) if details_elem else None
            
            if title or price or details:
                auto = Dict_Goo_Net(
                    title=title,
                    price=price,
                    details=details
                )
                results.append(asdict(auto))
        return results

if __name__ == '__main__':
    scraper = Goo_Net()
    url_template = "https://www.goo-net-exchange.com/php/search/summary.php?search_type=new_arrival_popular_jdm&page={page}"
    scraper.main(start_page=1, end_page=3, url_template=url_template)
