## LMS - Проект самообучения


### Описание проекта

Данный проект является образовательным сервисом для обучения студентов. 
В проекте предусмотрен многопользовательский функционал, обеспечивающий разноуровневый доступ к его материалам 
и опциям в зависимости от статуса пользователя. В базовой версии созданы группы пользователей: администратор, педагог и
студент, однако предусмотрена возможность безгранично расширять количество групп и их права доступа.

Функционал сервиса позволяет администраторам иметь неограниченный доступ к всем опциям, а также назначать права 
доступа другим пользователям и распределять их по группам, педагогам - создавать, просматривать, редактировать 
учебные курсы и материалы к ним, загружать графические файлы и подкреплять учебный процесс видео-уроками, студенам - 
просматривать учебные материалы, проходить тестирование на предмет освоения изученного материала.

Для хранения данных используется PostgreSQL.

В проекте реализована бэкенд-часть с возмождностью управления через административную панель Django, а также REST API.


### Документация

Для установки сервиса необходимо:

Клонировать репозиторий.
Настроить и активировать виртуальное окружение.

Установить зависимости:
* pip install -r requirements.txt.

Подключиться к СУБД и создать БД:
* psql -p 5434 -U postgres
* create database LMS

Создать и применить миграции:
* python manage.py makemigrations
* python manage.py migrate

Заполнить БД: 
* python manage.py loaddata data.json

Заполнить переменные окружения:
* в файле <.env.sample> и переименовать его в <.env> .

Создать администратора:
* python manage.py csu

В качестве локального сервера используется:
* http://127.0.0.1:8000/ или http://localhost:8000/
* http://127.0.0.1:8000/users/ - регистрация нового пользователя (POST запрос) и управление пользователями,
* http://127.0.0.1:8000/token/ - получение токенов для расширенных прав доступа (POST запрос),
* http://127.0.0.1:8000/courses/ (lesson/, questions/, answers/ и choices/) - управление курсами, уроками, 
заданиями и ответами
* http://127.0.0.1:8000/swagger/ (redoc/) - документация


### Запуск

Запуск проекта:
* python manage.py runserver


Запуск тестов:
* python manage.py test
* coverage run --source='.' manage.py test
* coverage report


### Контакты

9232485@gmail.com
