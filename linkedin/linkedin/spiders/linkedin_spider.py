
import scrapy as _scrapy

class LinkedinSpider(_scrapy.Spider):
    name = "linkedin"

    def __init__(self, keyword=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = keyword

    def start_requests(self):
        if self.keyword is not None:
            url = (
                f'https://www.linkedin.com/search/results/index/?keywords='
                f'{self.keyword}'
            )
            yield _scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        keyword = response.url.split('/?keywords=')[-1]
        filename = f'linkedin-{keyword}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

