# YLAB Ads API

REST API для сервиса объявлений (тестовое задание Y_LAB).

## Стек

- Python 3.12
- Django 6.1.1
- Django REST Framework 3.18.1
- PostgreSQL 16
- Docker + Docker Compose
- pytest + pytest-django
- pre-commit + Ruff

## Модели

### Author

| Поле | Тип | Правила |
|------|-----|---------|
| id | AutoField | Генерируется сервером |
| name | CharField(120) | Обязательное, непустое |

### Ad

| Поле | Тип | Правила |
|------|-----|---------|
| id | AutoField | Генерируется сервером |
| title | CharField(120) | Обязательное, непустое |
| description | TextField(5000) | Обязательное, непустое |
| price | DecimalField(11, 2) | От 0 до 999 999 999.99 |
| status | CharField | draft / published / archived, по умолчанию draft |
| author | ForeignKey | Ссылка на Author |
| created_at | DateTimeField | Автоматически при создании |
| updated_at | DateTimeField | Автоматически при обновлении |

## API

| Метод | Путь | Поведение |
|-------|------|-----------|
| POST | `/api/ads/` | Создать объявление. 201 |
| GET | `/api/ads/` | Список с фильтрами. 200 |
| GET | `/api/ads/{id}/` | Получить объявление. 200 |
| PATCH | `/api/ads/{id}/` | Частично обновить. 200 |
| DELETE | `/api/ads/{id}/` | Удалить. 204 |

### Фильтры

- `?status=draft` — фильтр по статусу (по умолчанию `published`)
- `?search=ноутбук` — поиск подстроки в title (без учёта регистра)
- Фильтры работают совместно.

### Сортировка

Новые записи первыми, при совпадении `created_at` — по `id` по убыванию.

## Запуск через Docker Compose

### 1. Клонировать репозиторий

```bash
git clone https://github.com/chernousovanton84-sketch/ylab-ads-api.git
cd ylab-ads-api
