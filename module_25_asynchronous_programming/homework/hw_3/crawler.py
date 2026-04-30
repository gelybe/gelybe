import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AsyncWebCrawler:
    def __init__(self, start_urls, max_depth=3, output_file="external_links.txt"):
        self.start_urls = [url.rstrip("/") for url in start_urls]
        self.max_depth = max_depth
        self.output_file = output_file
        self.visited = set()
        self.external_links = set()
        self.base_domains = {urlparse(url).netloc for url in self.start_urls}

    def is_external(self, url):
        try:
            domain = urlparse(url).netloc
            return domain and domain not in self.base_domains
        except Exception:
            return False

    async def fetch_page(self, session, url):
        try:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    text = await response.text()
                    logger.info(f"Успешно загружена страница: {url}")
                    return text
                else:
                    logger.warning(f"Ошибка {response.status}: {url}")
                    return None
        except Exception as e:
            logger.error(f"Исключение при запросе {url}: {e}")
            return None

    async def crawl_page(self, session, url, depth):
        if depth > self.max_depth or url in self.visited:
            return
        self.visited.add(url)

        html = await self.fetch_page(session, url)
        if not html:
            return

        # Попробуем найти хотя бы базовые ссылки
        soup = BeautifulSoup(html, "html.parser")
        found_any_links = False

        for tag in soup.find_all("a", href=True):
            full_url = urljoin(url, tag["href"]).rstrip("/")
            found_any_links = True

            if self.is_external(full_url):
                self.external_links.add(full_url)
                logger.info(f"🔗 Найдена внешняя ссылка: {full_url}")
            elif depth < self.max_depth:
                # Внутренняя ссылка — добавляем в обход
                if full_url.startswith("http"):
                    await self.crawl_page(session, full_url, depth + 1)

        if not found_any_links:
            logger.info(f"❌ На странице {url} не найдено ни одной ссылки <a href>")

    async def run(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.crawl_page(session, url, 1) for url in self.start_urls]
            await asyncio.gather(*tasks)

        # Сохраняем результат
        with open(self.output_file, "w", encoding="utf-8") as f:
            for link in sorted(self.external_links):
                f.write(link + "\n")

        print(f"\n✅ Готово! Найдено внешних ссылок: {len(self.external_links)}")
        print(f"📄 Результат сохранён в '{self.output_file}'")

        if self.external_links:
            print("\n🔗 Примеры внешних ссылок:")
            for link in list(self.external_links)[:5]:
                print(f"  - {link}")
        else:
            print("\n🔍 Внешние ссылки не найдены. Возможно, сайт использует JS для навигации.")

# Запуск
if __name__ == "__main__":
    urls = ["https://cataas.com"]
    crawler = AsyncWebCrawler(start_urls=urls, max_depth=2)
    asyncio.run(crawler.run())