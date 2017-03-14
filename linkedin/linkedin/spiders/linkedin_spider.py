
import scrapy as _scrapy
from scrapy.spiders import init as _init

class LinkedinSpider(_init.InitSpider):
    name = "linkedin"
    login_page = 'https://www.linkedin.com/uas/login'

    def __init__(self, keyword=None, user=None, password=None, *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = keyword
        self.user = user
        self.password = password
        self.log('init done')

    def init_request(self):
        """ Initialize the spider by logging in """
        self.log('creating login request')
        return _scrapy.Request(url=self.login_page, callback=self.login)

    def login(self, response):
        """ Try to login """
        data = dict(session_key=self.user, session_password=self.password)
        return FormRequest.from_response(response, formdata=data,
                                         callback=self.check_login_response)

    def check_login_response(self, response):
        """ Check whether the login was successful """
        if "Sign Out" in response.body:
            self.log('Logged in...')
            return self.initialized()
        else:
            self.log('Login failed')

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

