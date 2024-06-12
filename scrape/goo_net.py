from libraries.base_scrape import Scraper
from dataclasses import dataclass, asdict

@dataclass
class Dict_Goo_Net:
    title: str
    price: str
    details: str  # Contains date of manufacture, colour, mileage, displacement, drive, transmission
    img_link:str

class Goo_Net(Scraper):
    def __init__(self) -> None:
        fieldnames = ["title", "price", "details", "img_link"]
        output_file = "data/goo_net_data.csv"
        super().__init__(fieldnames, output_file)

    def parser(self, html):
        cars = html.css("a.spread_link_new_tab")
        results = []
        
        for item in cars:
            title_elem = item.css_first("h3.title")
            price_elem = item.css_first("p.price.currency-jpy")
            details_elem = item.css_first("ul.details")
            video_elem = item.css_first("p.video-item")
            img_link_elem = item.css_first("img.lazyload")
            
            title = self.clean_text(title_elem.text()) if title_elem else None
            price = self.clean_text(price_elem.text()) if price_elem else None
            details = self.clean_text(details_elem.text()) if details_elem else None
            image = img_link_elem.attributes.get("src") if img_link_elem else None
            
            links = []
            if video_elem:
                video_link = video_elem.css_first("img.lazyload").attributes.get("data-src")
                links.append(video_link)
            
            if img_link_elem:
                img_link = img_link_elem.attributes.get("data-src")
                links.append(img_link_elem)

            # Join all links into a single string separated by a delimiter
            img_link = " | ".join(links) if links else None
            
            auto = Dict_Goo_Net(
                title=title,
                price=price,
                details=details,
                img_link=img_link
            )
            results.append(asdict(auto))
        return results

if __name__ == '__main__':
    scraper = Goo_Net()
    url_template = "https://www.goo-net-exchange.com/php/search/summary.php?search_type=new_arrival_popular_jdm&page={page}"
    scraper.main(start_page=1, end_page=3, url_template=url_template)
