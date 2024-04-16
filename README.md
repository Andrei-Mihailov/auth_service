# Backend сервиса авторизации

https://github.com/Andrei-Mihailov/auth_service

Backend сервиса авторизации с системой ролей на FastAPI.

---

## Установка

```bash
$ git clone https://github.com/Andrei-Mihailov/auth_service.git
```


## Подготовка переменных окружения
Перед первым запуском нужно подготовить переменные окружения.

В директории с проектом последовательно запустить:

```shell
$ mv .env.template .env
$ openssl genrsa -out rsa.key 2048
$ openssl rsa -in rsa.key -pubout > rsa.key.pub
```
Затем открыть файл `.env` в любом текстовом редакторе. 
В качестве значения переменной `AUTHJWT_PRIVATE_KEY` установить значение из файла `rsa.key`.
В качестве значения переменной `AUTHJWT_PUBLIC_KEY` установить значение из файла `rsa.key.pub`.


## Запуск

Выполнить команды

```console
$ docker-compose build
$ docker-compose up
```

После запуска можно сразу регистрировать нового пользователя.


## Документация API

Документация доступна по url: 
```
http://localhost:8000/api/openapi
```
