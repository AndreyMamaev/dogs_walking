# Сервис выгула собак
### Описание
Тестовое задание
### Запуск проекта
Клонировать репозиторий и перейти в него в командной строке:

```git clone https://github.com/AndreyMamaev/miner.git```

Перейти в директорию проекта:

```cd miner```

Создать /backend/.env файл (по образцу .envexample)

Создать контейнеры:

```docker-compose up -d --build```

Выполнить начальную миграцию:

```./create_migration.sh```

Для последующих запусков проекта:

```docker-compose up -d --build```

Для остановки проекта:

```docker-compose down```
