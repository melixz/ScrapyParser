import scrapy
import time
from Alkoteka.items import ProductItem

CATEGORIES = [
    ("vino", "Вино"),
    ("krepkiy-alkogol", "Крепкий алкоголь"),
    ("shampanskoe-i-igristoe", "Шампанское и игристое"),
]
CITY_UUID = "4a70f9e0-46ae-11e7-83ff-00155d026416"  # Краснодар
API_URL = "https://alkoteka.com/web-api/v1/product"
PER_PAGE = 100


class AlkotekaAPISpider(scrapy.Spider):
    name = "alkoteka_api"
    allowed_domains = ["alkoteka.com"]

    def start_requests(self):
        for slug, name in CATEGORIES:
            page = 1
            url = f"{API_URL}?city_uuid={CITY_UUID}&page={page}&per_page={PER_PAGE}&root_category_slug={slug}"
            meta = {"category_slug": slug, "category_name": name, "page": page}
            yield scrapy.Request(url, callback=self.parse_api, meta=meta)

    def parse_api(self, response):
        data = response.json()
        category_slug = response.meta["category_slug"]
        category_name = response.meta["category_name"]
        results = data.get("results", [])
        for product in results:
            item = ProductItem()
            item["timestamp"] = int(time.time())
            item["RPC"] = str(product.get("vendor_code") or product.get("uuid"))
            item["url"] = product.get("product_url")
            # Формируем title
            title = product.get("name", "")
            extra = []
            for label in product.get("filter_labels", []):
                if label.get("filter") in ("obem", "cvet"):
                    if label["title"] not in title:
                        extra.append(label["title"])
            if extra:
                title = f"{title}, {', '.join(extra)}"
            item["title"] = title
            # Маркетинговые теги
            tags = [
                tag["title"]
                for tag in product.get("action_labels", [])
                if tag.get("title")
            ]
            item["marketing_tags"] = tags
            item["brand"] = product.get("subname") or ""
            # Иерархия разделов
            section = []
            if product.get("category"):
                parent = product["category"].get("parent")
                if parent:
                    section.append(parent.get("name"))
                section.append(product["category"].get("name"))
            else:
                section = [category_name]
            item["section"] = section
            # Цена
            price = float(product.get("price") or 0)
            original = float(product.get("prev_price") or price)
            sale_tag = None
            if original > price:
                sale_tag = f"Скидка {int((1 - price / original) * 100)}%"
            item["price_data"] = {
                "current": price,
                "original": original,
                "sale_tag": sale_tag or "",
            }
            # Наличие
            item["stock"] = {
                "in_stock": bool(product.get("available", True)),
                "count": int(product.get("quantity_total") or 0),
            }
            # Картинки
            main_image = product.get("image_url")
            set_images = [main_image] if main_image else []
            if product.get("gallery"):
                set_images += [
                    img for img in product["gallery"] if img and img not in set_images
                ]
            item["assets"] = {
                "main_image": main_image,
                "set_images": set_images,
                "view360": product.get("view360", []),
                "video": product.get("video", []),
            }
            # Метаданные
            metadata = {
                "__description": product.get("description")
                or product.get("short_description")
                or "",
                "category_slug": category_slug,
            }
            for label in product.get("filter_labels", []):
                if label.get("filter") and label.get("title"):
                    metadata[label["filter"]] = label["title"]
            item["metadata"] = metadata
            # Варианты (цвет/объём)
            variants = [
                label
                for label in product.get("filter_labels", [])
                if label.get("filter") in ("obem", "cvet")
            ]
            item["variants"] = len(variants)
            yield item
        # Пагинация
        meta = response.meta.copy()
        if data.get("meta", {}).get("has_more_pages"):
            meta["page"] += 1
            next_url = f"{API_URL}?city_uuid={CITY_UUID}&page={meta['page']}&per_page={PER_PAGE}&root_category_slug={category_slug}"
            yield scrapy.Request(next_url, callback=self.parse_api, meta=meta)
