import scrapy

class BooksSpider(scrapy.Spider):
    name = 'books'

    start_urls = [
        "https://books.toscrape.com/"
    ]

    def parse(self, response):
        products = response.css("ol.row li")
        all_books_link = []
        for product in products:
            book_link = product.css("h3 a::attr(href)").get()
            all_books_link.append(book_link)

        for book_link in all_books_link:
            yield response.follow(url=book_link , callback=self.parse_book)

        next_page = response.css("li.next a::attr(href)").get()

        if next_page is not None:
            yield response.follow(next_page , callback=self.parse)
    def parse_book(self,response):

        def table_ex(table):
            trs = table.css("tr")
            info = {}
            for tr in trs:
                info[tr.css("th::text").get()] = tr.css("td::text").get()
            return info

        book_info = response.css("article.product_page")

        yield {
            "book_image": book_info.css("div.carousel-inner div img::attr(src)").get(),
            "book_title": book_info.css("div.product_main h1::text").get(),
            "price": book_info.css("p.price_color::text").get(),
            "stock_availability": book_info.css("p.availability::text").get(),
            "book_description": book_info.css("div#product_description + p::text").get(),
            "book_info": table_ex(book_info.css("div.sub-header + table")),
        }
