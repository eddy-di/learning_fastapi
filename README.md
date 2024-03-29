# Домашнее задание 4

Этот git-репозиторий создан исключительно для выполнения требований для прохождения стажировки в компании Y-Lab. Более подробная информация предназначена для модераторов, которые собираются ее протестировать.

# Установка и настройка проекта в docker
## 1. Клонировать репозиторий git

1. Откройте терминал.
2. Измените текущую папку либо путь на тот, где вы хотите клонировать проект с ДЗ.
3. Скопируйте эту строку кода.

```
git clone https://github.com/eddy-di/learning_fastapi.git
```

4. Вставьте приведенную выше команду в терминал и нажмите Enter.

## 2. Запуск WEB сервера в docker

1. предполагается что у вас уже установлен Docker.

> Данный образ и контейнеры в нем предназначены для просмотра выполнения фоновых задач через Celery и RabbitMQ. Прежде чем начать тестирование убедитесь в том что в докере не остались включенными или занимают порты/хосты другие образы или контейнеры, в случае если есть таковые просьба очистить или удалить все связанные с этим заданием по меню контейнеры, образы, волюмы (volumes) и билды (builds) через CLI или Docker Desktop.

2. Перейдите в корневую директорию проекта и введите в командную:

```
docker compose -f docker-compose.yaml up -d --build
```

3. Это позволит в виртуальной среде установить все пакеты и запустить проект в docker'e.
4. Проект доступен через браузер по адресу:

```
http://localhost:8000/docs
```

Вы должны будете увидеть такую страницу с реализованными эндпоинтами: ![image](./readme_images/schemas_menu.png "Пример эндпоинтов")

5. Проверить можно с запросами на эндпоинты. Через первый и второй видно будет что Celery таски отработали и создали в базе данных всё так как указано в `Menu.xlsx`, в случае если сразу не начнется то переотправьте запрос подождав несколько секунд.
6. Для того чтобы отключить поднятый сервер в docker'e находясь в корневой директории проекта введите:

```
docker compose -f docker-compose.yaml down -v
```

## 3. Запуск Pytest тестов в docker

> Данный образ и контейнеры предназначены для прогона тестов через pytest. Нижеуказанная команда в подпункте 1 реализует сценарий поднятия проекта, запроса команды `pytest -v` и удаления контейнеров проекта. Для корректной работы убедитесь что все другие контейнеры или образы docker не запущены. В случае если порты будут заняты другими проектами то необходимо остановить их.

1. Перейдите в корневую директорию проекта и введите в терминале данную команду:

```
docker-compose -f docker-compose-tests.yaml up -d && docker logs --follow test_web && docker compose -f docker-compose-tests.yaml down -v
```

Если вы тестируете через Windows PowerShell введите данную команду:

```
docker-compose -f docker-compose-tests.yaml up -d; docker logs --follow test_web; docker compose -f docker-compose-tests.yaml down -v
```

2. Это позволит вам увидеть в терминале результат успешно выполненных 33 тестов.
3. По тестовому сценарию проверки кол-ва блюд и подменю в меню из Postman с помощью pytest можете ознакомиться по [этой ссылке](https://github.com/eddy-di/learning_fastapi/blob/main/tests/test_case4_counters.py).
4. Юнит тесты проверяющие CRUD эндпоинтов по меню доступны [тут](https://github.com/eddy-di/learning_fastapi/blob/main/tests/test_menu_crud.py).
5. Юнит тесты проверяющие CRUD эндпоинтов по подменю доступны [тут](https://github.com/eddy-di/learning_fastapi/blob/main/tests/test_submenu_crud.py).
6. Юнит тесты проверяющие CRUD эндпоинтов по блюдам доступны [тут](https://github.com/eddy-di/learning_fastapi/blob/main/tests/test_dish_crud.py).


## 4. Пункты 4 Домашнего задания

1. Переход от синхронного к асинхронному при соединении к базе данных и кэшу, а также слой бизнес логики асинхронен.
2. Добавление фоновых Celery задач с проверками и перепроверками доступны [тут](app/celery/tasks.py).
3. Добавлен новый эндпоинт с выводом всех имеющихся объектов в базе данных [/api/v1/menus/preview](https://github.com/eddy-di/learning_fastapi/blob/187a08fcb6f9e9467308e404529dfbdca5d40eae/app/routers/menu.py#L25).
4. Реализация кеша через встроенный BackgroundTasks инициализируется в роутерах, [пример](https://github.com/eddy-di/learning_fastapi/blob/eee96466592b270213d0b2a4ace3a5482fab2732/app/routers/menu.py#L26), и полностью используется по всему файлу по этому [пути](app/services/api/), отвечающий за слой бизнес логики. Можно увидеть исполнение встроенных бэкграунд тасков, [пример тут](https://github.com/eddy-di/learning_fastapi/blob/0e5a0c414a9c2ea8b7659cea0c1dbea061f462f7/app/services/api/dish.py#L28), или [тут](https://github.com/eddy-di/learning_fastapi/blob/eee96466592b270213d0b2a4ace3a5482fab2732/app/services/api/menu.py#L71).
5. Обновление происходит не из GoogleSheets а из Menu.xlsx из папки [/app/admin/Menu.xlsx](app/admin/Menu.xlsx) посредством класса [ExcelSheetParser](https://github.com/eddy-di/learning_fastapi/blob/0e5a0c414a9c2ea8b7659cea0c1dbea061f462f7/app/celery/helpers/parser.py#L5) и метода [parse](https://github.com/eddy-di/learning_fastapi/blob/0e5a0c414a9c2ea8b7659cea0c1dbea061f462f7/app/celery/helpers/parser.py#L25).
6. Размер скидки просчитывается во время парсинга с экзеля [тут](https://github.com/eddy-di/learning_fastapi/blob/187a08fcb6f9e9467308e404529dfbdca5d40eae/app/celery/helpers/parser.py#L60), с 60 по 62 строку, что в дальнейшем идет на валидацию в pydantic схемах [тут](https://github.com/eddy-di/learning_fastapi/blob/187a08fcb6f9e9467308e404529dfbdca5d40eae/app/schemas/dish.py#L71), и в случае если была прописана скидка в G колонне в эксель файле то автоматически программа покажет цену со скидкой.
---
