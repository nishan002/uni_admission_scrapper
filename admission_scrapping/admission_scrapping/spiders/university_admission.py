import scrapy

class UniversityAdmissionsSpider(scrapy.Spider):
    name = "university_admissions"
    start_urls = ["https://searchenginesmarketer.com/company/resources/university-college-list/"]

    def parse(self, response):
        # Extract university names and links from the initial page
        university_data = {}
        universities = response.xpath('//table/tbody/tr')[1:]  # Skip the header row

        for link in universities:
            university_name = link.xpath('td[1]/text()').get()
            university_name = university_name.lower()

            # Replace spaces with underscores
            university_name = university_name.replace(" ", "_")

            # Remove special characters (non-alphanumeric and non-underscore characters)
            university_name = ''.join(c for c in university_name if c.isalnum() or c == '_')
            university_link = link.xpath('td[2]/a/@href').get()

            university_data[university_name] = {"university_link": university_link}

            # Follow the link to the university's page to get admission links
            yield response.follow(university_link, self.parse_admission_links, meta={"university_name": university_name, "university_data": university_data})

    def parse_admission_links(self, response):
        global all_links
        university_name = response.meta["university_name"]
        university_data = response.meta["university_data"]

        # Extract links under the "Admission" nav menu
        # admission_links = response.xpath("//li[a[contains(text(), 'Admission')]]").extract_first()
        admission_links_dict = {}

        admission_links = response.xpath("//li[a[contains(text(), 'Admission')]]").extract_first()

        if admission_links:
            li_selector = scrapy.selector.Selector(text=admission_links)
            all_links = li_selector.xpath("//a")

        for link in all_links:
            link_text = link.xpath('text()').get()
            link_url = link.xpath('@href').get()
            # admission_links_dict[link_text] = link_url

            # Update the university's data with the admission links
            university_data[university_name][link_text] = link_url

        # Yield the university's data
        yield {university_name: university_data[university_name]}