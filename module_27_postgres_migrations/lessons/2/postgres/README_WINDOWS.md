# PostgreSQL на Windows 10 без Docker

## 🚀 Быстрая установка PostgreSQL

### Вариант 1: Установщик Windows (рекомендуется)

1. **Скачайте PostgreSQL:**
   - Перейдите на https://www.postgresql.org/download/windows/
   - Скачайте установщик для Windows
   - Выберите последнюю стабильную версию

2. **Установка:**
   - Запустите установщик
   - Укажите пароль для пользователя `postgres` (запомните его!)
   - Оставьте остальные настройки по умолчанию
   - Установите pgAdmin (графический интерфейс)

3. **Запуск службы:**
   - PostgreSQL автоматически запустится как служба Windows
   - Проверьте в Службах Windows, что "postgresql-x64-XX" работает

### Вариант 2: Chocolatey (если установлен)

```powershell
# Установка PostgreSQL
choco install postgresql

# Перезапустите PowerShell после установки
```

## 🗄️ Настройка базы данных

После установки выполните:

```powershell
# Перейдите в папку с проектом
cd C:\Users\getto\python_advanced\module_27_postgres_migrations\lessons\2\postgres

# Запустите скрипт настройки
python local_setup.py
```

## 🔧 Подключение к базе данных

**Параметры подключения:**
- Host: `localhost`
- Port: `5432`
- Database: `postgres_migrations`
- User: `admin`
- Password: `admin`

## 🛠️ Полезные команды

```powershell
# Проверка статуса службы
Get-Service postgresql*

# Перезапуск службы
Restart-Service postgresql-x64-XX

# Подключение через psql
psql -U admin -d postgres_migrations -h localhost
```

## 📊 Графический интерфейс

Используйте **pgAdmin**, который устанавливается вместе с PostgreSQL:
- Найдите pgAdmin в меню Пуск
- Создайте новое подключение с указанными выше параметрами

## 🐛 Поиск проблем

**Если не удается подключиться:**
1. Проверьте, что служба PostgreSQL запущена
2. Проверьте брандмауэр Windows (порт 5432)
3. Убедитесь, что пароль правильный
4. Попробуйте подключиться как пользователь `postgres`

**Сброс пароля:**
```powershell
# Остановите службу
Stop-Service postgresql-x64-XX

# Запустите в безопасном режиме и измените пароль
# (см. документацию PostgreSQL)
```

## 🎯 Готово!

После настройки ваша база данных готова для работы с миграциями PostgreSQL.
