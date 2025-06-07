import json
import os
from datetime import datetime
from itemadapter import ItemAdapter


class AlkotekaPipeline:
    """Основной pipeline"""

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        required_fields = ["timestamp", "RPC", "url", "title", "section"]
        for field in required_fields:
            if not adapter.get(field):
                spider.logger.warning(
                    f"Отсутствует поле {field} для товара {adapter.get('url', 'unknown')}"
                )

        if adapter.get("title"):
            adapter["title"] = adapter["title"].strip()

        if adapter.get("brand"):
            adapter["brand"] = adapter["brand"].strip()

        if not isinstance(adapter.get("marketing_tags"), list):
            adapter["marketing_tags"] = []

        if not isinstance(adapter.get("price_data"), dict):
            adapter["price_data"] = {}

        if not isinstance(adapter.get("stock"), dict):
            adapter["stock"] = {"in_stock": None, "status": "Неизвестно"}

        if not isinstance(adapter.get("assets"), dict):
            adapter["assets"] = {}

        if not isinstance(adapter.get("metadata"), dict):
            adapter["metadata"] = {}

        if not isinstance(adapter.get("variants"), list):
            adapter["variants"] = []

        return item


class JsonWriterPipeline:
    """Pipeline для сохранения данных в JSON файл"""

    def open_spider(self, spider):
        self.results_dir = "results"
        os.makedirs(self.results_dir, exist_ok=True)
        self.filename = f"{self.results_dir}/result.json"
        self.file = open(self.filename, "w", encoding="utf-8")
        self.items = []
        spider.logger.info(f"Создан файл: {self.filename}")

    def close_spider(self, spider):
        import json

        json.dump(self.items, self.file, ensure_ascii=False, indent=2)
        self.file.close()
        spider.logger.info(f"Сохранено {len(self.items)} товаров в {self.filename}")

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item


class DuplicatesPipeline:
    """Pipeline для фильтрации дубликатов"""

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        item_id = adapter.get("RPC")

        if item_id in self.ids_seen:
            spider.logger.warning(f"Дубликат товара: {item_id}")
            return None
        else:
            self.ids_seen.add(item_id)
            return item


class ValidationPipeline:
    """Pipeline для валидации данных"""

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        url = adapter.get("url")
        if not url or not url.startswith("http"):
            spider.logger.error(f"Некорректный URL: {url}")
            return None

        title = adapter.get("title")
        if not title or title == "Название не найдено":
            spider.logger.warning(f"Отсутствует название для товара: {url}")

        price_data = adapter.get("price_data", {})
        current_price = price_data.get("current")
        if not current_price or current_price <= 0:
            spider.logger.warning(f"Некорректная цена для товара: {url}")

        return item


class StatsPipeline:
    """Pipeline для сбора статистики"""

    def __init__(self):
        self.stats = {
            "total_items": 0,
            "categories": {},
            "with_discounts": 0,
            "with_images": 0,
            "price_ranges": {
                "under_500": 0,
                "500_1000": 0,
                "1000_5000": 0,
                "over_5000": 0,
            },
        }

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        self.stats["total_items"] += 1

        section = adapter.get("section", "Неизвестно")
        if isinstance(section, list):
            section_key = "/".join(section)
        else:
            section_key = str(section)
        if section_key not in self.stats["categories"]:
            self.stats["categories"][section_key] = 0
        self.stats["categories"][section_key] += 1

        marketing_tags = adapter.get("marketing_tags", [])
        if any("скидка" in tag.lower() for tag in marketing_tags):
            self.stats["with_discounts"] += 1

        assets = adapter.get("assets", {})
        if assets.get("main_image"):
            self.stats["with_images"] += 1

        price_data = adapter.get("price_data", {})
        current_price = price_data.get("current")
        if current_price:
            if current_price < 500:
                self.stats["price_ranges"]["under_500"] += 1
            elif current_price < 1000:
                self.stats["price_ranges"]["500_1000"] += 1
            elif current_price < 5000:
                self.stats["price_ranges"]["1000_5000"] += 1
            else:
                self.stats["price_ranges"]["over_5000"] += 1

        return item

    def close_spider(self, spider):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        stats_filename = f"results/alkoteka_stats_{timestamp}.json"

        os.makedirs("results", exist_ok=True)
        with open(stats_filename, "w", encoding="utf-8") as f:
            json.dump(self.stats, f, ensure_ascii=False, indent=2)

        spider.logger.info(f"Статистика сохранена в {stats_filename}")
        spider.logger.info(f"Всего обработано товаров: {self.stats['total_items']}")
        spider.logger.info(f"По категориям: {self.stats['categories']}")
