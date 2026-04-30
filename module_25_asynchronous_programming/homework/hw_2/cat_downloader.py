import asyncio
from pathlib import Path
import aiohttp
import aiofiles
import time
import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing as mp

# Конфигурация
URL = 'https://cataas.com/cat'
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()

# === Асинхронная версия (корутины) ===
async def get_cat_async(client: aiohttp.ClientSession, idx: int) -> bytes | None:
    try:
        async with client.get(URL, timeout=aiohttp.ClientTimeout(total=30)) as response:
            if response.status == 200:
                result = await response.read()
                await write_to_disk_async(result, idx)
                return result
            else:
                print(f"Ошибка {response.status} для котика #{idx}")
                return None
    except asyncio.TimeoutError:
        print(f"Таймаут для котика #{idx}")
        return None
    except Exception as e:
        print(f"Ошибка загрузки котика #{idx}: {e}")
        return None

async def write_to_disk_async(content: bytes, idx: int):
    file_path = OUT_PATH / f"{idx}.png"
    try:
        async with aiofiles.open(file_path, mode='wb') as f:
            await f.write(content)
    except Exception as e:
        print(f"Ошибка записи файла #{idx}: {e}")

async def get_all_cats_async(num_cats: int):
    timeout = aiohttp.ClientTimeout(total=60)  # Увеличиваем общий таймаут
    async with aiohttp.ClientSession(timeout=timeout) as client:
        tasks = [get_cat_async(client, i) for i in range(num_cats)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        # Фильтруем None и исключения
        valid_results = [r for r in results if r is not None and not isinstance(r, Exception)]
        return valid_results

def run_async(num_cats: int) -> float:
    start_time = time.time()
    results = asyncio.run(get_all_cats_async(num_cats))
    duration = time.time() - start_time
    print(f"Загружено {len(results)}/{num_cats} котиков асинхронно за {duration:.2f} сек")
    return duration

# === Версия с потоками (threads) ===
def get_cat_thread(idx: int) -> bytes | None:
    try:
        response = requests.get(URL, timeout=30)
        if response.status_code == 200:
            content = response.content
            write_to_disk_thread(content, idx)
            return content
        else:
            print(f"Ошибка {response.status_code} для котика #{idx}")
            return None
    except requests.exceptions.Timeout:
        print(f"Таймаут для котика #{idx}")
        return None
    except Exception as e:
        print(f"Ошибка загрузки котика #{idx}: {e}")
        return None

def write_to_disk_thread(content: bytes, idx: int):
    file_path = OUT_PATH / f"{idx}.png"
    try:
        with open(file_path, 'wb') as f:
            f.write(content)
    except Exception as e:
        print(f"Ошибка записи файла #{idx}: {e}")

def run_threads(num_cats: int, max_workers: int = 10) -> float:
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(get_cat_thread, range(num_cats)))
    duration = time.time() - start_time
    successful = sum(1 for r in results if r is not None)
    print(f"Загружено {successful}/{num_cats} котиков потоками за {duration:.2f} сек")
    return duration

# === Версия с процессами (multiprocessing) ===
def get_cat_process(idx: int) -> bytes | None:
    import requests
    try:
        response = requests.get(URL, timeout=30)
        if response.status_code == 200:
            content = response.content
            write_to_disk_process(content, idx)
            return content
        else:
            print(f"Ошибка {response.status_code} для котика #{idx}")
            return None
    except requests.exceptions.Timeout:
        print(f"Таймаут для котика #{idx}")
        return None
    except Exception as e:
        print(f"Ошибка загрузки котика #{idx}: {e}")
        return None

def write_to_disk_process(content: bytes, idx: int):
    file_path = OUT_PATH / f"{idx}.png"
    try:
        with open(file_path, 'wb') as f:
            f.write(content)
    except Exception as e:
        print(f"Ошибка записи файла #{idx}: {e}")

def run_processes(num_cats: int, max_workers: int = None) -> float:
    if max_workers is None:
        max_workers = mp.cpu_count()
    start_time = time.time()
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(get_cat_process, range(num_cats)))
    duration = time.time() - start_time
    successful = sum(1 for r in results if r is not None)
    print(f"Загружено {successful}/{num_cats} котиков процессами за {duration:.2f} сек")
    return duration

# === Функция для замеров и генерации таблицы ===
def benchmark_all_approaches():
    test_sizes = [10, 50, 100]
    results = []

    print("Запуск сравнительного тестирования трёх подходов...")
    print("=" * 60)

    for size in test_sizes:
        print(f"\n=== Тестирование для {size} котиков ===")

        # Асинхронный подход
        print("Замер асинхронного подхода...", end=" ")
        async_time = run_async(size)

        # Потоки
        print("Замер потоков...", end=" ")
        thread_time = run_threads(size)

        # Процессы
        print("Замер процессов...", end=" ")
        process_time = run_processes(size)

        results.append({
            'size': size,
            'async': async_time,
            'threads': thread_time,
            'processes': process_time
        })

    return results

def print_results_table(results):
    print("\n" + "=" * 80)
    print("РЕЗУЛЬТАТЫ ЗАМЕРОВ")
    print("=" * 80)
    print(f"| Количество котиков | Асинхронный (сек) | Потоки (сек) | Процессы (сек) | Лучший результат |")
    print(f"|----------------|-------------------|--------------|---------------|---------------|")

    for res in results:
        size = res['size']
        async_t = res['async']
        thread_t = res['threads']
        process_t = res['processes']

        times = {'Асинхронный': async_t, 'Потоки': thread_t, 'Процессы': process_t}
        best_approach = min(times, key=times.get)

        print(f"| {size:<14} | {async_t:<17.2f} | {thread_t:<12.2f} | {process_t:<13.2f} | {best_approach:<13} |")

    print("=" * 80)

# === Основной блок выполнения ===
if __name__ == '__main__':
    # Запускаем замеры
    results = benchmark_all_approaches()

    # Выводим результаты в виде таблицы
    print_results_table(results)

    # Дополнительный анализ
    print("\nАНАЛИЗ РЕЗУЛЬТАТОВ:")
    print("- Асинхронный подход обычно самый быстрый для I/O-bound задач (загрузка файлов).")
    print("- Потоки показывают среднее время выполнения, но проще в реализации.")
    print("- Процессы имеют высокие накладные расходы и медленнее для данной задачи.")
    print("- Время записи в файл через aiofiles сопоставимо с синхронными аналогами.")
