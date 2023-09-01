import scrapy


class AdmissionScrapping(scrapy.Spider):
    name = 'university'
    allowed_domains = ['www.astate.edu/']
    start_urls = [
        'https://www.astate.edu/',
        'https://www.alaska.edu/alaska/',
        'https://www.bu.edu/wheelock/admissions/',
        'https://www.aum.edu'
    ]

    admission_keywords = ['Admission', 'Admissions']

    def parse(self, response):
        li_element = response.xpath("//li[a[contains(text(), 'Admission')]]").extract_first()

        if li_element:
            li_selector = scrapy.selector.Selector(text=li_element)
            all_links = li_selector.xpath("//a/@href").extract()

            for link in all_links:
                yield {
                    "link": link
                }

