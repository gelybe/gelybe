import sys
from pathlib import Path

# Добавляем текущую директорию в sys.path для корректного импорта модулей
sys.path.insert(0, str(Path(__file__).parent))
