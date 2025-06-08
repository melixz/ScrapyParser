# Парсер alkoteka.com для региона Краснодар

Scrapy-парсер для сбора данных о товарах с сайта alkoteka.com, настроенный для региона Краснодар.

## Описание

Парсер собирает информацию о товарах из трех основных категорий:
- **Вино** - более 1000 товаров
- **Крепкий алкоголь** - более 1000 товаров  
- **Шампанское и игристое** - более 200 товаров

### Особенности реализации

- Автоматическая смена региона на Краснодар
- Обработка возрастных ограничений (18+)
- Принятие cookies и политик конфиденциальности
- Ротация User-Agent'ов для имитации браузера
- Поддержка работы через прокси
- Фильтрация дубликатов товаров
- Валидация и очистка данных
- Сохранение в JSON формате

## Настройка

1. Установите [uv](https://github.com/astral-sh/uv):

```bash
# На Linux/macOS через curl
curl -LsSf https://astral.sh/uv/install.sh | sh
# или через pipx
pipx install uv
```

2. Создайте виртуальное окружение и активируйте его:

```bash
uv venv
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate  # Windows
```

3. Установите зависимости проекта:

```bash
uv sync
```

4. Быстрый старт

```bash
scrapy crawl alkoteka_api -O results/result.json
```

## Структура данных

Каждый товар содержит следующие поля:

```json
{
    "timestamp": "2024-01-15T14:30:00.123456",
    "RPC": "55714",
    "url": "https://alkoteka.com/product/vino-tikhoe/belbek-roze-kaberne-sovinon_55714",
    "title": "Бельбек Розе Каберне Совиньон",
    "marketing_tags": ["Новинка", "Скидка"],
    "brand": "Бельбек",
    "section": "Вино",
    "price_data": {
        "current": 1650.0,
        "original": 1850.0,
        "sale_tag": "Скидка 11%"
    },
    "stock": {
        "in_stock": true,
        "status": "В наличии"
    },
    "assets": {
        "main_image": "https://alkoteka.com/images/products/55714.jpg",
        "additional_images": []
    },
    "metadata": {
        "description": "Розовое сухое вино...",
        "characteristics": [
            "Объем: 0.75 л",
            "Тип: Вино тихое",
            "Крепость: 12-14%",
            "Страна: Россия"
        ],
        "category_slug": "vino"
    },
    "variants": []
}
```

## Особенности

Все файлы сохраняются в директории `results/` с timestamp'ом:

- `alkoteka_all_products_YYYYMMDD_HHMMSS.json` - все товары
- `alkoteka_vino_YYYYMMDD_HHMMSS.json` - только вино
- `alkoteka_krepkiy-alkogol_YYYYMMDD_HHMMSS.json` - крепкий алкоголь
- `alkoteka_shampanskoe-i-igristoe_YYYYMMDD_HHMMSS.json` - шампанское
- `alkoteka_stats_YYYYMMDD_HHMMSS.json` - статистика парсинга
- `scrapy_log_YYYYMMDD_HHMMSS.log` - логи выполнения


### Middleware цепочка

1. **CookieMiddleware** - обработка cookies и региона
2. **ProxyMiddleware** - ротация прокси
3. **UserAgentMiddleware** - ротация User-Agent'ов
4. **AlkotekaDownloaderMiddleware** - основная обработка

### Pipeline цепочка

1. **ValidationPipeline** - валидация данных
2. **DuplicatesPipeline** - фильтрация дубликатов
3. **AlkotekaPipeline** - очистка и нормализация
4. **JsonWriterPipeline** - сохранение в JSON
5. **StatsPipeline** - сбор статистики

## Дополнительные возможности

### Добавление прокси

Создайте файл `proxy_list.txt`:

```
http://proxy1:port
http://proxy2:port
http://user:pass@proxy3:port
```

### Ошибки парсинга

1. Проверьте логи в `results/scrapy_log_*.log`
2. Убедитесь что сайт доступен
3. Проверьте селекторы в браузере