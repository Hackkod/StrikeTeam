<!-- Консоль -->
<!-- Создание вирт. окружения -->
python -m venv venv
.\venv\Scripts\activate   
<!-- Установка пакетов -->
pip install django
pip install djangorestframework
<!-- Создание проекта -->
django-admin startproject volgait .
<!-- Запуск проекта -->
python manage.py runserver
<!-- Мигрировать изменения -->
python manage.py makemigrations
python manage.py migrate
<!-- Создание приложения -->
python manage.py startapp appname
<!-- Создание суперпользователя -->
python manage.py createsuperuser <!--путь: /admin-->



<!-- Работа с файлами -->
<!-- В основном модуле -->
<!-- settings: -->
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
<!-- Добавить в INSTALLEDAPPS название приложения -->
'volgait',
'rest_framework',
<!-- Ну и дальше создаем модели, делаем миграцию и пишем вьюшки, маршрутизаторы и сериализаторы -->

<!-- В модуле приложения нужно зарегистрировать его в админке -->
<!-- admin.py: -->


