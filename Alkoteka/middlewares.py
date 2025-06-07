import random
import time
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import (
    UserAgentMiddleware as BaseUserAgentMiddleware,
)
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware


class AlkotekaSpiderMiddleware:
    """Middleware для паука"""

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info(f"Spider opened: {spider.name}")


class CookieMiddleware:
    """Middleware для установки cookies"""

    def __init__(self, cookies):
        self.cookies = cookies

    @classmethod
    def from_crawler(cls, crawler):
        cookies = crawler.settings.get("ALKOTEKA_COOKIES", {})
        return cls(cookies)

    def process_request(self, request, spider):
        if "alkoteka.com" in request.url:
            for key, value in self.cookies.items():
                request.cookies[key] = value
        return None


class ProxyMiddleware(HttpProxyMiddleware):
    """Middleware для прокси"""

    def __init__(self, proxy_list):
        self.proxy_list = proxy_list

    @classmethod
    def from_crawler(cls, crawler):
        proxy_list = crawler.settings.get("PROXY_LIST", [])
        return cls(proxy_list)

    def process_request(self, request, spider):
        if self.proxy_list:
            proxy = random.choice(self.proxy_list)
            request.meta["proxy"] = proxy
        return None


class UserAgentMiddleware(BaseUserAgentMiddleware):
    """Middleware для User-Agent"""

    def __init__(self, user_agent_list):
        self.user_agent_list = user_agent_list

    @classmethod
    def from_crawler(cls, crawler):
        user_agent_list = crawler.settings.get("USER_AGENT_LIST", [])
        return cls(user_agent_list)

    def process_request(self, request, spider):
        if self.user_agent_list:
            user_agent = random.choice(self.user_agent_list)
            request.headers["User-Agent"] = user_agent
        return None


class JavaScriptMiddleware:
    """Middleware для обработки JavaScript-генерируемого контента"""

    def __init__(self, timeout):
        self.timeout = timeout

    @classmethod
    def from_crawler(cls, crawler):
        timeout = crawler.settings.get("JAVASCRIPT_TIMEOUT", 10)
        return cls(timeout)

    def process_request(self, request, spider):
        request.meta.update(
            {
                "dont_redirect": False,
                "handle_httpstatus_list": [200, 301, 302, 303, 307, 308],
                "download_timeout": self.timeout,
            }
        )

        if "alkoteka.com" in request.url:
            request.headers.update(
                {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Cache-Control": "no-cache",
                    "Pragma": "no-cache",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "none",
                    "Sec-Fetch-User": "?1",
                    "Upgrade-Insecure-Requests": "1",
                }
            )

        return None

    def process_response(self, request, response, spider):
        if "alkoteka.com" in response.url and response.status == 200:
            if "/catalog/" in response.url:
                spider.logger.info(f"Ожидание загрузки JavaScript для {response.url}")
                time.sleep(5)

                body = response.body.decode("utf-8")
                if "Найдено" not in body or "card-product" not in body:
                    spider.logger.warning(f"Товары не загрузились для {response.url}")
                    time.sleep(3)

        return response


class AlkotekaDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        if "alkoteka.com" in request.url:
            request.headers.update(
                {
                    "Referer": "https://alkoteka.com/",
                    "Origin": "https://alkoteka.com",
                    "Sec-Fetch-Site": "same-origin",
                    "Cache-Control": "max-age=0",
                }
            )

        return None

    def process_response(self, request, response, spider):
        if response.status == 200:
            spider.logger.debug(
                f"Успешный ответ от {response.url}: {len(response.body)} байт"
            )

        return response

    def process_exception(self, request, exception, spider):
        spider.logger.error(f"Ошибка при загрузке {request.url}: {exception}")
        return None

    def spider_opened(self, spider):
        spider.logger.info(f"Spider opened: {spider.name}")
