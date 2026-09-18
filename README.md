# QA Trainee Assignment — Autumn 2026

Автоматизированные тесты API сервиса объявлений.

## Инструкция по запуску
Используются команды в терминале.

### 1. Склонируйте репозиторий

Склонируйте репозиторий с проектом:

```bash
git clone https://github.com/talense-tasks/qa-trainee-assignment-autumn-2026-flow-2-narkyas-ea27435c.git
```

Перейдите в директорию проекта:

```bash
cd qa-trainee-assignment-autumn-2026-flow-2-narkyas-ea27435c
```

### 2. Убедитесь, что установлен Python

В командной строке выполните:

```bash
python --version
```


Для Windows также можно использовать:

```powershell
py --version
```
Если не отображается версия, значит программы нет на компьютере, [установите Python с официального сайта](https://www.python.org/downloads/). Для запуска тестов используется Python 3.10 или выше.

### 3. Установите  зависимости

В корневой директории проекта выполните:

```bash
pip install -r requirements.txt
```


### 4. Запустите тесты

Для запуска всех автоматизированных тестов выполните:

```bash
pytest -v
```
Если команда не работает, воспользуйтесь похожей: 
```bash
py -m pytest -v
```

Автотесты отправляют HTTP-запросы непосредственно к API сервиса и проверяют ответы:

```text
https://qa-internship.avito.com
```

## Что покрывают тесты

Автоматизировано **28 тестов**, которые проверяют:

* регистрацию пользователя;
* авторизацию;
* создание объявления;
* получение объявления;
* получение объявлений продавца;
* получение статистики;
* удаление объявления;
* проверку авторизации и доступа;
* негативные сценарии;
* проверку данных в ответах API;
* полный E2E-сценарий жизненного цикла объявления.

Подробное описание тест-кейсов находится в файле `TESTCASES.md`.

## Структура проекта

```text
.
├── BUGS.md
├── TESTCASES.md
├── README.md
├── PROMPTS.md
├── requirements.txt
├── postman_collection.json
├── images/
├── screenshots/
└── tests/
    ├── conftest.py
    ├── helpers.py
    ├── test_register.py
    ├── test_authorize.py
    ├── test_items.py
    ├── test_seller_items.py
    ├── test_statistics.py
    ├── test_delete.py
    └── test_e2e.py
```
