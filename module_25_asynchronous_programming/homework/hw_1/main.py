import asyncio
from pathlib import Path
import aiohttp

URL = 'https://cataas.com/cat'
CATS_WE_WANT = 10
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()


async def get_cat(client: aiohttp.ClientSession, idx: int) -> bytes:
    async with client.get(URL) as response:
        print(response.status)
        result = await response.read()
        await write_to_disk(result, idx)
        return result


async def write_to_disk(content: bytes, idx: int):
    file_path = OUT_PATH / f"{idx}.png"

    # Получаем текущий event loop
    loop = asyncio.get_running_loop()

    # Выполняем синхронную операцию open в отдельном потоке
    await loop.run_in_executor(
        None,  # Используем стандартный ThreadPoolExecutor
        lambda: write_file_sync(content, file_path)
    )


def write_file_sync(content: bytes, file_path: Path):
    """Синхронная функция для записи файла"""
    with open(file_path, mode='wb') as f:
        f.write(content)


async def get_all_cats():
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(15)) as client:
        tasks = [get_cat(client, i) for i in range(CATS_WE_WANT)]
        results = await asyncio.gather(*tasks)
        return results


def main():
    res = asyncio.run(get_all_cats())
    print(f"Успешно скачано {len(res)} котов")


if __name__ == '__main__':
    main()
