# Домашнее задание 1 

Этот git-репозиторий создан исключительно для выполнения требований для прохождения стажировки в компании Y-Lab. Более подробная информация предназначена для модераторов, которые собираются ее протестировать. 

# Установка и настройка проекта 
## 1. Клонировать репозиторий git 

1. Откройте терминал. 
2. Измените текущую папку либо путь на тот, где вы хотите клонировать проект с ДЗ. 
3. Скопируйте эту строку кода. 

```
git clone https://github.com/eddy-di/learning_fastapi.git
```

4. Вставьте приведенную выше команду в терминал и нажмите Enter.
## 2. Настройка базы данных

1. Поднимаем базу данных через Docker командой
```
docker-compose -f local.yaml up -d
```  
2. Чтобы этот проект работал правильно, убедитесь, что существует переменная окружения `SQLALCHEMY_DATABASE_URL` со значением `postgresql://menu_db_admin:menu_db_admin@localhost:5432/menu_db` для локальных тестов. Для этого надо убедиться есть ли файл `.env` со значением `SQLALCHEMY_DATABASE_URL = "postgresql://menu_db_admin:menu_db_admin@localhost:5432/menu_db"`
3. В данном проекте уже существует `.env` и `example.env` файлы.

## 3. Загрузка пакета Poetry

1. Я предполагаю, что на вашем компьютере предустановлен пакет Poetry. Если нет, обязательно проверьте, доступна ли она вам, введя следующую команду в терминале:

```
poetry --version
```

2. Если вы видите такой вывод: `Poetry (version 1.X.X)`, то все готово переходите к 4 шагу "Установка пакетов". В большинстве случаев Poetry должен быть доступен по умолчанию. 
3. Если вам не удалось получить какие-либо выходные данные, как указано на предыдущем шаге, перейдите по следующей ссылке: https://python-poetry.org/docs/#installing-with-pipx. 
4. Или используйте следующие команды для установки Poetry в Windows или Linux/MacOS:

Для Windows: 
Запустите следующую команду в Терминале:

```
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

Для Linux/MacOS: 
Запустите следующую команду в Терминале:

```
curl -sSL https://install.python-poetry.org | python3 -
```

## 4. Установка пакетов

1. В терминале перейдите в папку, где находится клонированный репозиторий. 
2. Чтобы установить все необходимые пакеты, которые помогут правильно выполнить ДЗ проект, введите:

```
poetry install
```

3. Это позволит настроить необходимые пакеты для ДЗ проекта.
4. Затем выполните следующую команду для инициализации виртуальной среды:

```
poetry shell
```

5. Команда `shell` позволяет вам работать в отдельной среде и соответственно запускать тесты. 
6. Убедитесь, что виртуальная среда активирована.

```
(env-name) username@computer-name:path/to/the/cloned/repo$  <-- [это пример]
```

7. Приведенный выше пример применим к Linux/MacOS.

## 5. Инициализация сервера

1. Чтобы убедиться, что проект домашнего задания будет доступен для тестирования через Postman, важно инициализировать локальный сервер. Запустите эту команду в своем терминале:

```
uvicorn main:app --reload
```

2. Обязательно проверьте, получаете ли вы вывод, подобный этому, с другими сведениями, специфичными только для вашего компьютера.

```
INFO:     Will watch for changes in these directories: ['path/to/the/cloned/repo']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [101969] using WatchFiles
INFO:     Started server process [101971]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Теперь вы можете приступить к проверке домашнего задания на Postman. 

Спасибо!


# Homework 1

This git repository is made purely to fulfill the requirements for getting the internship at Y-Lab company. 
Further details are for moderators who are going to test it.

# Installation and setting project up
## 1. Clone git repository

1. Open terminal.
2. Change the current working directory to the location where you want the cloned directory.
3. Copy this line of code.

HTTPS:

```
git clone https://github.com/eddy-di/learning_fastapi.git
```

4. Paste the command above into the terminal and press enter.
## 2. Setting up database

1. Raise the database via Docker with the command

```
docker-compose -f local.yaml up -d
```

2. For this project to work correctly, ensure that the environment variable `SQLALCHEMY_DATABASE_URL` exists with the value `postgresql://menu_db_admin:menu_db_admin@localhost:5432/menu_db` for local tests. To do this, you need to make sure there is a `.env` file with the value `SQLALCHEMY_DATABASE_URL = "postgresql://menu_db_admin:menu_db_admin@localhost:5432/menu_db"`.
3. This project already has `.env` and `example.env` files.

## 3. Downloading Poetry package

1. I would assume that you have preinstalled poetry on your computer, if not please make sure to check if it is available to you by typing this command in your terminal:

```
poetry --version
```

2. If you see an output like this: `Poetry (version 1.X.X)` then you are good to go follow the instructions in 4th part "Installing packages". In most of the cases, Poetry has to be available by default.
3. If you were unable to get any output as mentioned in the previous step, then please follow the following link: https://python-poetry.org/docs/#installing-with-pipx 
4. Or use the following commands to install poetry to Windows or Linux/MacOS:

For Windows:
Run the following command in Terminal:

```
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

For Linux/MacOS:
Run the following command in Terminal:

```
curl -sSL https://install.python-poetry.org | python3 -
```

## 4. Installing packages

1. In your terminal, go to the location where the cloned repository is.
2. To install all the necessary packages that will help to execute homework properly type in:

```
poetry install
```

3. This will set up the required packages for the homework project.
4. Then run the following command to initialize the virtual environment:

```
poetry shell
```

5. The `shell` command allows you to work in a separate environment, and to run tests accordingly.
6. Make sure to see if the virtual environment has been activated.

```
(env-name) username@computer-name:path/to/the/cloned/repo$  <-- [this is an example]
```

7. The above example applies to Linux/MacOS 

## 5. Initiating server

1. To make sure that the homework project will be available for tests via Postman, it is important to initiate the local server. Run this command in your terminal:

```
uvicorn main:app --reload
```

2. Make sure to check if you are getting an output similar to this, with the other details specific to your computer only.

```
INFO:     Will watch for changes in these directories: ['path/to/the/cloned/repo']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [101969] using WatchFiles
INFO:     Started server process [101971]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Now you are good to go testing homework on Postman.

Thank you!