BOT_NAME = "Alkoteka"

SPIDER_MODULES = ["Alkoteka.spiders"]
NEWSPIDER_MODULE = "Alkoteka.spiders"

# User-Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Robotstxt
ROBOTSTXT_OBEY = False

# Конфигурация запросов
CONCURRENT_REQUESTS = 2
DOWNLOAD_DELAY = 3
RANDOMIZE_DOWNLOAD_DELAY = 0.5  # Рандомизация задержки
CONCURRENT_REQUESTS_PER_DOMAIN = 16

# Cookies
COOKIES_ENABLED = True

# Telnet
TELNETCONSOLE_ENABLED = False

# Заголовки запроса
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "no-cache",
    "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}


# Middleware для паука
SPIDER_MIDDLEWARES = {
    "Alkoteka.middlewares.AlkotekaSpiderMiddleware": 543,
}


# Middleware для загрузчика
DOWNLOADER_MIDDLEWARES = {
    "Alkoteka.middlewares.CookieMiddleware": 100,
    "Alkoteka.middlewares.ProxyMiddleware": 200,
    "Alkoteka.middlewares.UserAgentMiddleware": 300,
    "Alkoteka.middlewares.AlkotekaDownloaderMiddleware": 543,
    "Alkoteka.middlewares.JavaScriptMiddleware": 560,
}


# Расширения
EXTENSIONS = {
    "scrapy.extensions.telnet.TelnetConsole": None,
}


# Pipeline
ITEM_PIPELINES = {
    "Alkoteka.pipelines.ValidationPipeline": 100,
    "Alkoteka.pipelines.DuplicatesPipeline": 200,
    "Alkoteka.pipelines.AlkotekaPipeline": 300,
    "Alkoteka.pipelines.JsonWriterPipeline": 400,
    "Alkoteka.pipelines.StatsPipeline": 500,
}

# Автоматическая регулировка скорости
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Кэш
HTTPCACHE_ENABLED = False

# Кодировка
FEED_EXPORT_ENCODING = "utf-8"

# Уровень логирования
LOG_LEVEL = "INFO"

# Прокси
PROXY_LIST = []

# Cookies
ALKOTEKA_COOKIES = {
    "age_verified": "true",
    "city_selected": "krasnodar",
    "cookie_accepted": "true",
    "adult_confirmed": "1",
    "region": "krasnodar",
    "cookies_accepted": "1",
}

ALKOTEKA_REGION = "krasnodar"  # Краснодар

# User-Agent
USER_AGENT_LIST = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
]

# Retry
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# Timeout
DOWNLOAD_TIMEOUT = 30
JAVASCRIPT_TIMEOUT = 10
