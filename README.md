# How to run

## Step 1

Для начала создайте папку для проекта и выполните команду:

```
git clone https://github.com/Nikolrusik/anon_shop.git /yourfolder
```

## Step 2

Откройте проект в терминале и создайте виртуальное окружение:

```
cd yourfolde
python3 -m venv venv
```

## Step 3

Активируйте окружение и установите зависимости:

```
source './venv/bin/activate'
pip install requirements.txt
```

## Step 4

Выполните следующие команды, чтобы у вас отобразились тестовые данные и запустился сервер:

```
python3 manage.py migrate
python3 manage.py loaddata dump.json
python3 manage.py runserver
```

## Step 5

Перейдите на http://127.0.0.1:8000/mainapp

**Done!**
