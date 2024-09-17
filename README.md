# Handsome of the Day Bot

**Handsome of the Day Bot** — это Telegram-бот, который решает кто сегодня "Красавчика дня", а кому придется называться "Лузера дня".

## Оглавление

- [Описание](#описание)
- [Функционал](#функционал)
- [Требования](#требования)
- [Установка и запуск](#установка-и-запуск)
  - [1. Локальный запуск](#Локальный-запуск-(не-рекомедуется))
  - [2. Запуск в Docker](#Запуск-в-Docker-(рекомендуется))
- [Использование](#использование)
- [Логирование](#логирование)
- [Лицензия](#лицензия)

## Описание

Этот бот предназначен для автоматической оценки пользователей в чате Telegram, ежедневно выбирая одного "Красавчика дня" и "Пидора дня". Результаты сохраняются в базе данных PostgreSQL и могут быть использованы для создания статистики.

## Функционал

- Команда `/run` — выполняет ежедневный выбор "Красавчика" и "Пидора" дня.
- Автоматическое выполнение в 12:00 каждый день через **APScheduler**.
- Логирование событий в файл для дальнейшего анализа.
- Мониторинг и сбор метрик с помощью **Prometheus** и **Grafana**.

## Требования

- **Ubuntu 24.04.1 LTS** (Данный дистрибутив использовался для разработки и отладки)
- **Docker** 
- **Telegram API Token**

## Установка и запуск

### Локальный запуск (не рекомедуется)

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/rpglit/handsome-of-the-day.git
   cd handsome-of-the-day

2. Установите зависимости:
   ```bash
   git pip install -r requirements.txt

3. Создайте базу данных PostgreSQL и настройте подключение в файле config.py.

4. Запустите бота:
   ```bash
   python main.py
   
### Запуск в Docker (рекомендуется)

1. Убедитесь, что Docker установлен на вашем компьютере.

2. Соберите Docker образ самого бота:
   ```bash
   docker build -t handsome-of-the-day-bot ./Docker/.

3. Используйте Docker Compose для создания всех контейнеров:
   ```bash
   docker-compose up -d

## Использование

1. Добавьте Telegram бота в групповой чат, выдав ему права администратора.

2. Используйте команду /reg чтобы принять участие в розыгрыше званий.

3. Запустите поиск героев дня с помощью команды /run или дождитесь 9 часов по Гринвичу.

4. Для отображения полной личной и общей за месяц статистикой используйте команды /my и /stat соответственно.

## Логирование

Логи бота сохраняются в папке /logs на хост-машине, если установка осуществлялась с использованием Docker. Для анализа работы бота и просмотра событий за день используйте сохраненные логи:
   ```bash
   cat ~/logs/bot.log
   ```
Для вывода логов в файл при локальной установке запускайте бота следующей командой:
   ```bash
   python3 -u main.py >> /logs/bot.log 2>&1
   ```

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности можно найти в файле LICENSE.


### Объяснение разделов:
1. **Оглавление** — удобно для быстрой навигации по README.
2. **Описание** — краткое объяснение проекта.
3. **Функционал** — описание ключевых возможностей бота.
4. **Требования** — список зависимостей и версий ПО.
5. **Установка и запуск** — пошаговые инструкции для локального запуска и через Docker.
6. **Использование** — примеры команд и сообщений бота.
7. **Логирование** — информация о том, как сохранять и просматривать логи.
8. **Лицензия** — указывает, что проект распространяется по открытой лицензии.
