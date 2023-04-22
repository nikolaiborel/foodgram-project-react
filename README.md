http://84.201.149.231/
login: admin@mail.ru
pass: trewq123

# Foodgram
## продуктовый помощник

С помощью Foodgram можно подобрать подходящий рецепт на завтрак, обед или ужин. С помощью Foodgram можно рассчитать необходимое количество ингердиентов на любое количество персон, добавить все к себе в корзину и раcпечатать.
Еще на Foodgram можно добавлять рецепты в избранное, подписываться на любимых авторов и не только.

### Компоненты
- backend - образ бэкенда (DRF)
- fronted - образ фронтенда (React)
- postgres - образ базы данных (PostgreSQL)
- nginx - образ веб-сервера

### Установка
1. Клонируйте себе репозиторий:
git clone https://github.com/nikolaiborel/foodgram-project-react.git
2. Заполните файл .env по образцу. Файл и образец должны находиться в директории backend/foodgram/
3. Установите Docker (если он у вас установлен, то можете пропустить этот шаг)
4. Перейдите в папку infra/ <br>
`cd infra`
5. Запустите сборку и docker-compose <br>
`docker compose up -d --build`

### Первоначальная настройка
1. Запустите миграции<br>
`sudo docker compose exec backend python manage.py migrate --noinput`
2. Соберите статику<br>
`sudo docker compose exec backend python manage.py collectstatic --no-input`
3. Создайте суперпользователя<br>
`sudo docker compose exec backend python manage.py createsuperuser`
4. Загрузите данные ингердиентов (их больше 2000)<br>
`sudo docker compose exec backend  python manage.py loaddata ingredients.json`

### Технологии
- Python
- Django Rest Framework
- Docker
- Nginx
- Postgres
- React

### Автор
Борель Николай


