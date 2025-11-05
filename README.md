# effMobProject — Полное руководство по установке и запуску

UI‑тесты сайта Effective Mobile, контейнеризированные для стабильного запуска в Docker с генерацией отчёта Allure.

## Что внутри
- База `python:3.10-slim` и рабочая директория `/app`.
- Установлены `chromium` и `chromium-driver` (совместимые версии), Java Runtime (`default-jre`) для Allure CLI.
- `Allure CLI` (версия задаётся `ARG ALLURE_VERSION`, по умолчанию `2.29.0`).
- Python‑зависимости: `pytest`, `selenium`, `allure-pytest` из `requirements.txt`.
- Тесты запускают Chrome в headless‑режиме с флагами для Docker: `--headless=new`, `--no-sandbox`, `--disable-dev-shm-usage`, `--disable-gpu`, `--window-size=1920,1080`.

## Требования
- Установленный Docker (Desktop) на хосте.
- Свободный порт `8080` для показа Allure‑репорта.

## Сборка образа
В корне `effMobProject` выполните:

```bash
docker build -t effmob-tests .
```

## Быстрый запуск: тест + отчёт Allure (одной командой)
Запустить тесты и сразу поднять сервер Allure на `8080`:

```bash
docker rm -f effmob-allure || true && \
docker run --name effmob-allure \
  -p 8080:8080 \
  --shm-size=1g \
  effmob-tests bash -lc \
  "python -m pytest --alluredir=test_results/ tests/test_select_main_page.py ; allure serve test_results/ -h 0.0.0.0 -p 8080"
```

Откройте отчёт: `http://localhost:8080/`.

## Интерактивный режим
Если хотите зайти внутрь контейнера и запускать команды вручную:

```bash
docker run -it --rm -p 8080:8080 --shm-size=1g effmob-tests bash
```

Далее внутри контейнера (`/app`):

- Запустить все тесты:

```bash
python -m pytest -s -v
```

- Запустить конкретный тест с генерацией Allure‑результатов:

```bash
python -m pytest --alluredir=test_results/ tests/test_select_main_page.py
```

- Поднять сервер Allure:

```bash
allure serve test_results/ -h 0.0.0.0 -p 8080
```

## Сохранение результатов на хосте
Чтобы папка `test_results` сохранялась вне контейнера:

```bash
mkdir -p test_results
docker run -it --rm \
  -v "$(pwd)/test_results:/app/test_results" \
  -p 8080:8080 \
  --shm-size=1g \
  effmob-tests bash -lc "python -m pytest --alluredir=test_results/ tests/test_select_main_page.py ; allure serve test_results/ -h 0.0.0.0 -p 8080"
```

## Локальный запуск без Docker (опционально)
Если хотите запускать тесты на хосте:
- Установите Python 3.10 и зависимости: `pip install -r requirements.txt`.
- Установите совместимые `Chromium/Chrome` и `Chromedriver`.
- Отредактируйте пути в тесте, если отличаются от контейнера:
  - `options.binary_location = "/usr/bin/chromium"`
  - `Service(executable_path="/usr/bin/chromedriver")`

Запуск:

```bash
python -m pytest --alluredir=test_results/ tests/test_select_main_page.py
allure serve test_results/ -h 0.0.0.0 -p 8080
```

## Структура проекта
- `tests/test_select_main_page.py` — тест, конфигурирует Chrome и запускает сценарий.
- `pages/main_page.py` — Page Object: ожидания `presence_of_element_located`, клики через JavaScript с прокруткой, проверки якорных URL.
- `Dockerfile` — окружение (Chromium, Chromedriver, Java, Allure CLI, Python).
- `requirements.txt` — версии зависимостей.

## Режимы запуска браузера
- По умолчанию: headless (`--headless=new`).
- Нехедлесс (если нужно визуально): запускайте через виртуальный дисплей:

```bash
xvfb-run -a python -m pytest -s -v
```

## Советы и устранение проблем
- Ошибка `session not created / Chrome instance exited`:
  - Убедитесь, что используется headless‑режим (`--headless=new`) или виртуальный дисплей (`xvfb-run`).
  - Задайте `--shm-size=1g` для контейнера или используйте флаг `--disable-dev-shm-usage`.
  - Проверьте совместимость версий `chromium` и `chromedriver`.
- Таймауты кликов/поиска элементов:
  - В Page Object применён `presence_of_element_located` + клик через JS после прокрутки.
  - Добавлено ожидание `document.readyState == "complete"` после загрузки.

## Полезные команды
- Пересобрать образ после изменений:

```bash
docker build -t effmob-tests .
```

- Зайти внутрь контейнера для отладки:

```bash
docker run -it --rm effmob-tests bash
```

- Остановить/перезапустить контейнер с отчётом:

```bash
docker rm -f effmob-allure || true
```

Готово: после выполнения раздела «Быстрый запуск» отчёт доступен по адресу `http://localhost:8080/`.
