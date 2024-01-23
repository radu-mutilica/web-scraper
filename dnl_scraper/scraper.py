import scrapy
from typing import Iterator

import items


class ProductsSpider(scrapy.Spider):
    name = "products"
    start_urls = ["https://www.urparts.com/index.cfm/page/catalogue"]
    allowed_domains = ["urparts.com"]

    def parse(self, response: scrapy.http.response.Response, **__) -> Iterator[scrapy.Request]:
        """Initial parsing entrypoint.

        Parse the homepage and, for each 'make' found, yield a new request and assign
        it to the next parsing step (parse_category()).

        Args:
            response: the http response from the request.
            __: any kwargs, not used.

        Returns:
            An iterator of further scrapy request objects.
        """
        for li in response.css('div.allmakes li'):
            make = li.css('a::text').get().strip()
            make_href = li.css('a::attr(href)').get()

            product = {
                'make': make,
            }

            yield scrapy.Request(
                response.urljoin(make_href),
                callback=self.parse_category,
                meta=product
            )

    def parse_category(self, response: scrapy.http.response.Response) -> Iterator[scrapy.Request]:
        """Second parse step.

        On this make's page, parse out all the product categories and initialize further scrapes
        for each one of them.

        Args:
            response: the http response from the request.

        Returns:
            An iterator of further scrapy request objects.
        """
        product = response.meta

        for li in response.css('div.allcategories li'):
            # I afforded myself a .lower() here because I noticed a lack of consistency
            # among different makes and categories when it came to this field
            category = li.css('a::text').get().strip().lower()
            category_href = li.css('a::attr(href)').get()

            product['category'] = category

            yield scrapy.Request(
                response.urljoin(category_href),
                callback=self.parse_model,
                meta=product
            )

    def parse_model(self, response: scrapy.http.response.Response) -> Iterator[scrapy.Request]:
        """Third parse step.

        On this category's page, parse out all the product models and initialize further scrapes
        for each one of them.

        Args:
            response: the http response from the request.

        Returns:
            An iterator of further scrapy request objects.
        """
        product = response.meta

        for li in response.css('div.allmodels li'):
            model = li.css('a::text').get().strip()
            model_href = li.css('a::attr(href)').get()

            product['model'] = model

            yield scrapy.Request(
                response.urljoin(model_href),
                callback=self.parse_part,
                meta=product
            )

    def parse_part(self, response: scrapy.http.response.Response) -> Iterator[scrapy.Request]:
        """Fourth parse step.

        On this model's page, parse out all the parts and (in a recursive fashion), return
        the 'part_number' and 'part_type' up the call stack. These are the final two bits of
        information that we had to crawl, at the very end of the sitemap.

        Args:
            response: the http response from the request.

        Returns:
            An iterator of further scrapy request objects.
        """
        product = response.meta

        for li in response.css('div.allparts li'):
            part_number = li.css('a::text').get().split('-')[0].strip()

            # I afforded myself a .lower() here because I noticed a lack of consistency
            # among different makes and categories when it came to this field
            try:
                part_type = li.css('a span::text').get().strip().lower()
            except AttributeError:
                # Noticed that sometimes the part_type component is missing all together
                part_type = None

            # Use a ProductItem class (as opposed to dict) since the MongoDBPipeline
            # expects an ItemAdapter
            return items.ProductItem(
                make=product['make'],
                category=product['category'],
                model=product['model'],
                part_type=part_type,
                part_number=part_number
            )
