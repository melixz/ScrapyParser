import scrapy


class ProductItem(scrapy.Item):
    """Структура товара"""

    # Основные поля
    timestamp = scrapy.Field()
    RPC = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    marketing_tags = scrapy.Field()
    brand = scrapy.Field()
    section = scrapy.Field()

    # Ценовые данные
    price_data = scrapy.Field()

    # Наличие товара
    stock = scrapy.Field()

    # Медиа-контент
    assets = scrapy.Field()

    # Метаданные и характеристики
    metadata = scrapy.Field()

    # Варианты товара
    variants = scrapy.Field()
