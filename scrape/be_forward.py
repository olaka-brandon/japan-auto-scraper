from libraries.base_scrape import Scraper
from dataclasses import dataclass, asdict

@dataclass
class Dict_Be_Forward:
    title: str
    price: str
    total_price: str
    year: str
    mileage: str

class Be_Forward(Scraper):
    def __init__(self) -> None:
        fieldnames = ["title", "price", "total_price", "year", "mileage"]
        output_file = "data/be_forward_data.csv"
        super().__init__(fieldnames, output_file)

    def parser(self, html):
        cars = html.css("li.vehicle.vehicle-link")
        results = []

        for item in cars:
            title_elem = item.css_first("div.vehicle-make-model")
            price_elem = item.css_first("div.fob-price")
            total_price_elem = item.css_first("div.total-price")
            year_elem = item.css_first("div.vehicle-year")
            mileage_elem = item.css_first("div.vehicle-mileage")

            title = self.clean_text(title_elem.text()) if title_elem else None
            price = self.clean_text(price_elem.text()) if price_elem else None
            total_price = self.clean_text(total_price_elem.text()) if total_price_elem else None
            year = self.clean_text(year_elem.text()) if year_elem else None
            mileage = self.clean_text(mileage_elem.text()) if mileage_elem else None

            auto = Dict_Be_Forward(
                title=title,
                price=price,
                total_price=total_price,
                year=year,
                mileage=mileage
            )
            results.append(asdict(auto))
        return results

if __name__ == '__main__':
    scraper = Be_Forward()
    url_template = "https://sp.beforward.jp/stocklist/alt_port_id=32/page={page}/protection=1/sar=steering/shipping_method=1/sortkey=n/steering=Right/tp_country_id=27/tp_port_id=32"
    scraper.main(start_page=1, end_page=3, url_template=url_template)
