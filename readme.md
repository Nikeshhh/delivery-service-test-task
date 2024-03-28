# Тестовое задание для компании WelbeX

Необходимо разработать REST API сервиc для поиска ближайших машин к грузам.

[вакансия](https://hh.ru/vacancy/95118011)

### Для запуска:
Запустить контейнер:
```
docker compose up
```

Загрузить начальные данные:
```
docker exec -it django-application sh load_fixtures.sh
```

### Все эндпоинты описаны в сваггере по адресу [http://127.0.0.1:8000/swagger-ui/](http://127.0.0.1:8000/swagger-ui/)