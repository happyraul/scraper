
import scrapy as _scrapy

class LinkedinSpider(_scrapy.Spider):
    name = 'linkedin'
    login_page = 'https://www.linkedin.com/uas/login'

    def __init__(self, keyword=None, user=None, password=None, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = keyword
        self.user = user
        self.password = password

    def start_requests(self):
        url = 'https://www.linkedin.com/uas/login'
        yield _scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = dict(session_key=self.user, session_password=self.password)
        return _scrapy.FormRequest.from_response(response, formdata=data,
                                                 callback=self.after_login)

    def after_login(self, response):
        # if b'Sign Out' in response.body:
        if True:
            self.log('Logged in...')
            if self.keyword is not None:
                url = (
                    f'https://www.linkedin.com/search/results/index/'
                    f'?keywords={self.keyword}'
                )
                return _scrapy.Request(url=url, callback=self.parse_search)
        else:
            self.log('Login failed')
            with open('login.html', 'wb') as f:
                f.write(response.body)

    def parse_search(self, response):
        keyword = response.url.split('/?keywords=')[-1]
        filename = f'linkedin-{keyword}.csv'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

