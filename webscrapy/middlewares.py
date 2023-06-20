# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals, Request
import random
from webscrapy.settings import USER_AGENT_LIST
from scrapy.exceptions import IgnoreRequest, NotConfigured

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


def get_cookies_dict():
    cookies_str = 'anonymous-consents=%5B%5D; cookie-notification=NOT_ACCEPTED; YROUTEID=no_header_non_nz_z1-0; rxVisitor=16871741519167EH1F4TSH7UUDD283O6IM1OFEGCHQ4H4; _rm=0cd619a1-cf15-4c75-a892-c8c59af59fc0; _dy_csc_ses=t; BVImplmain_site=14909; _dy_c_exps=; unbxd.userId=uid-1687174153651-17607; _dycnst=dg; _gcl_au=1.1.1221596953.1687174154; scarab.visitor=%2258AD1B62916B3607%22; BVBRANDID=4170c642-8569-45f1-a6a4-a3e9b4323a1f; _dyid=7930839903264324617; _dyjsession=065341bbd96800d21f42437b92798af4; _dycst=dk.m.c.ws.; _dy_geo=GB.EU.GB_ENG.GB_ENG_Durham; _dy_df_geo=United%20Kingdom..Durham; _rdt_uuid=1687174154210.7542d149-8682-4929-95a8-5e07284225be; _gid=GA1.3.1587094136.1687174154; _cs_c=0; _tt_enable_cookie=1; _ttp=BIY-_rIecGyBdl1lSGwnSA8qirq; _fbp=fb.2.1687174154935.1201960612; _dyid_server=7930839903264324617; _dy_c_att_exps=; _dyfs=1687174160336; scarab.profile=%22348319%7C1687192246%22; ___uLangPref=en_US; JSESSIONID=93A118B9BC9EFD736A97A58DF90E5B06; unbxd.visitId=visitId-1687250938928-38503; gtm-session-start=undefined; dy_fs_page=www.mitre10.co.nz; dtCookie=v_4_srv_5_sn_59E474E892B03896FEE8888848F60BAE_perc_100000_ol_0_mul_1_app-3Adab812fd9e575017_1_app-3Aea7c4b59f27d43eb_1; bv_metrics=true; _cs_cvars=%7B%221%22%3A%5B%22no_search_results%22%2C%22true%22%5D%7D; BVBRANDSID=b9096f28-d705-4e21-b81b-5e595112eaf2; 1PCPageCount=17; _dy_lu_ses=065341bbd96800d21f42437b92798af4%3A1687255722371; _dy_toffset=-2; _ga=GA1.3.1079103096.1687174154; _cs_id=38b9f876-982a-a557-f16c-c95a145ff6e7.1687174154.7.1687255724.1687252404.1679360835.1721338154833; _cs_s=24.0.0.1687257524705; _dy_soct=1118906.1354032.1687251500*1131428.1385551.1687255726*1131432.1385555.1687255726*1139785.1485539.1687254598*1139785.1485542.1687255723*1155170.1442203.1687254513*1164596.1461476.1687255701*1175882.1485546.1687255722*1175883.1485547.1687192247; __cf_bm=NEK.rvTAXCpQUqq7AehpmMVPYZ3BCIO0lKzAe1ilWsY-1687257108-0-AcfMGtaGSFt894ZzpxHU/bg2nOha0mRLAkhmhhkF1RtE+gKNfxf6zcoeLSUUFpztPmThJptgJe6U4pP4/V+agCQalZJ67P2JINk/Q05myqI0; rxvt=1687258908388|1687257108388; dtPC=5$57108379_948h1vFRSRAAUIFOQCCKECRFOAMQELCEDUCHGL-0e0; _dy_ses_load_seq=21903%3A1687257109450; unbxd.visit=repeat; _ga_K5DE1X631G=GS1.1.1687250939.3.1.1687257167.60.0.0'

    cookies_dict = {}
    for item in cookies_str.split('; '):
        key, value = item.split('=', maxsplit=1)
        cookies_dict[key] = value
    return cookies_dict


COOKIES = get_cookies_dict()


class WebscrapySpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

class WebscrapyDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request: Request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # request.cookies = COOKIES
        # request.meta = {'proxy': 'socks5://127.0.0.1:10808'}
        ua = random.choice(USER_AGENT_LIST)
        request.headers['User-Agent'] = ua

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

class RotateProxyMiddleware:
    def __init__(self, proxies_file):
        self.proxies_file = proxies_file
        self.proxies = self.load_proxies()
        self.current_proxy = None

    @classmethod
    def from_crawler(cls, crawler):
        proxies_file = crawler.settings.get('PROXIES_FILE')
        return cls(proxies_file)

    def load_proxies(self):
        with open(self.proxies_file, 'r') as file:
            proxies = file.read().splitlines()
        return proxies

    def process_request(self, request, spider):
        if not self.current_proxy:
            self.current_proxy = self.get_random_proxy()

        request.meta['proxy'] = self.current_proxy
        print('current_proxy')
        print(self.current_proxy)

    def process_response(self, request, response, spider):
        if response.status == 403:
            self.remove_current_proxy()
            self.current_proxy = self.get_random_proxy()
            new_request = request.copy()
            new_request.dont_filter = True  # Disable duplicate request filtering
            return new_request
        elif response.status == 307:
            self.remove_current_proxy()
            self.current_proxy = self.get_random_proxy()
            new_request = request.copy()
            new_request.dont_filter = True  # Disable duplicate request filtering
            return new_request
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, IgnoreRequest):
            # Handle IgnoreRequest exceptions
            if getattr(exception, 'response', None) is not None:
                return self.process_response(request, exception.response, spider)
            else:
                # IgnoreRequest without a response, re-raise the exception
                raise exception
        elif isinstance(exception, NotConfigured):
            # NotConfigured exception, re-raise it
            raise exception
        else:
            # Handle other exceptions
            self.remove_current_proxy()
            self.current_proxy = self.get_random_proxy()
            new_request = request.copy()
            new_request.dont_filter = True  # Disable duplicate request filtering
            return new_request

    def get_random_proxy(self):
        if not self.proxies:
            self.proxies = self.load_proxies()  # Reload proxies from the file if the list is empty
        return random.choice(self.proxies)

    def remove_current_proxy(self):
        if self.current_proxy in self.proxies:
            self.proxies.remove(self.current_proxy)




