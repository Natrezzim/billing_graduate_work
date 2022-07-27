# Проектная работа: диплом
***
Платежная система
- https://github.com/MoJoVi/graduate_work
***
Прием платежей
-

• Регистрируемся в платежной системе; 

• Получаем API ключи; 

• Устанавливаем соответствующий пакет; 

• Реализовываем форму оплаты; 

• Реализовываем функцию зачисления средств на баланс после оплаты.

До создания платежа необходимо зарегистрироваться. Отправляем POST-запрос на адрес:
```
https://moviesbilling.ddns.net/auth/api/v1/registration
```
Тело запроса:
```
{
    "username": "user_name",
    "password": "newpassword1",
    "email": "user_name@test.com"
}
```
После регистрации, отправляем POST-запрос для получения **access_token** на адрес:
```
https://moviesbilling.ddns.net/auth/api/v1/login
```
Тело запроса:
```
{
    "username": "user_name",
    "password": "newpassword1"
}
```
C **access_token** можем создавать платежы, получать список платежей и детальную информацию по конкретному платежу.

Создаем платеж:
```
{
    "value": 1342.00,
    "currency": "RUB",
    "description": "Оплата подписки"
}
```

Отправляем POST-запрос на адрес:
```
https://moviesbilling.ddns.net/api/v1/payment
```

Получить список платежей. Отправляем GET-запрос на адрес:

```
https://moviesbilling.ddns.net/api/v1/payment
```

Получить информацию по конкретному платежу. Отправляем GET-запрос на адрес:

```
https://moviesbilling.ddns.net/api/v1/payment/{payment_id}
```


В ответ получаем **confirmation_url**
по которому должен проследовать пользователь и произвести оплату


***
Списание средств 
-
***
Повторяющиеся списания
-
***
Безопасность
-
Настроено SSL шифрование  
Сертификат Let's Encrypt получен с помощью Certbot
```nginx configuration
server {
    listen 443 default_server ssl http2;
    listen [::]:443 ssl http2;

    root /home/app;

    server_name moviesbilling.ddns.net www.moviesbilling.ddns.net.com;

    ssl_certificate /etc/nginx/ssl/live/moviesbilling.ddns.net/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/live/moviesbilling.ddns.net/privkey.pem;

  	ssl_session_cache shared:SSL:10m;
  	ssl_session_timeout 10m;

  	ssl_protocols TLSv1.2;
	ssl_prefer_server_ciphers on;
	ssl_ciphers "ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384";

    ssl_dhparam /etc/nginx/ssl/ffdhe4096.pem;
    ssl_ecdh_curve secp521r1:secp384r1;

	add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

	add_header X-Frame-Options DENY always;

	add_header X-Content-Type-Options nosniff always;

	add_header X-Xss-Protection "1; mode=block" always;

  	ssl_stapling on;
  	ssl_stapling_verify on;
  	ssl_trusted_certificate /etc/nginx/ssl/live/moviesbilling.ddns.net/fullchain.pem;
  	resolver 1.1.1.1 1.0.0.1 [2606:4700:4700::1111] [2606:4700:4700::1001] valid=300s;
  	resolver_timeout 5s;
}
```
***

CI/CD
-
Сервис развернут в яндекс облаке  
Доступен по статическому адресу 51.250.91.209 moviesbilling.ddns.net  
Настроен автоматический deploy с помощью github actions при мерже в ветку main  
Все образы сохраняются в Yandex Container Registry. Образы храняться в течении 24 часов, затем автоматически удаляются.
Все переменные среды берутся из github secrets  
Виртуальная машина создается командой  
```text
yc compute instance create-with-container --name ubuntu20-billing-ci --zone ru-central1-a --network-interface subnet-name=default-ru-central1-a,nat-ip-version=ipv4,nat-address=51.250.91.209 --service-account-name user-for-vm --docker-compose-file "путь к docker-compose.yaml файлу расположенному на локальной машине" --ssh-key "путь к публичному ключу .pub расположенному на локальной машине"
```
Пользователь для доступа к ВМ - yc-user  

Используются два файла docker-compose.yml
* docker-compose.dev.yaml - для удобной разработки локально
* docker-compose.prod.yaml - для разворачивания в облаке

### Настройки nginx
Конфиг nginx.conf
```nginx configuration
worker_processes  1;

events {
  worker_connections  1024;
}

http {
  include       mime.types;
  include       conf.d/*.conf;
  log_format  json '{ "time": "$time_local", '
                   '"remote_ip": "$remote_addr", '
                   '"remote_user": "$remote_user", '
                   '"request": "$request", '
                   '"response": "$status", '
                   '"bytes": "$body_bytes_sent", '
                   '"referrer": "$http_referer", '
                   '"agent": "$http_user_agent", '
                   '"request_id": "$request_id"}';

  access_log /var/log/nginx/access-log.json json;

  sendfile        on;
  tcp_nodelay     on;
  tcp_nopush      on;
  client_max_body_size 200m;
  server_tokens   off;

  gzip on;
  gzip_comp_level 3;
  gzip_min_length 1000;
  gzip_types
        text/plain
        text/css
        application/json
        application/x-javascript
        text/xml
        text/javascript;

  proxy_redirect     off;
  proxy_set_header   Host             $host;
  proxy_set_header   X-Real-IP        $remote_addr;
  proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
  proxy_set_header   X-Request-ID     $request_id;


} 
```
Конфиг site.conf
```nginx configuration
server {
    listen       80 default_server;
    listen       [::]:80 default_server;
    server_name moviesbilling.ddns.net www.moviesbilling.ddns.net.com;
    server_tokens off;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }

}

server {
    listen 443 default_server ssl http2;
    listen [::]:443 ssl http2;

    root /home/app;

    server_name moviesbilling.ddns.net www.moviesbilling.ddns.net.com;

    ssl_certificate /etc/nginx/ssl/live/moviesbilling.ddns.net/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/live/moviesbilling.ddns.net/privkey.pem;

  	ssl_session_cache shared:SSL:10m;
  	ssl_session_timeout 10m;

  	ssl_protocols TLSv1.2;
	ssl_prefer_server_ciphers on;
	ssl_ciphers "ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384";

    ssl_dhparam /etc/nginx/ssl/ffdhe4096.pem;
    ssl_ecdh_curve secp521r1:secp384r1;

	add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

	add_header X-Frame-Options DENY always;

	add_header X-Content-Type-Options nosniff always;

	add_header X-Xss-Protection "1; mode=block" always;

  	ssl_stapling on;
  	ssl_stapling_verify on;
  	ssl_trusted_certificate /etc/nginx/ssl/live/moviesbilling.ddns.net/fullchain.pem;
  	resolver 1.1.1.1 1.0.0.1 [2606:4700:4700::1111] [2606:4700:4700::1001] valid=300s;
  	resolver_timeout 5s;

    location / {
        proxy_pass http://billing_api:8010;
    }

    location /auth/ {
        proxy_pass http://auth_api:8001/;
    }

    location /swagger.json {
        proxy_pass http://auth_api:8001/swagger.json;
    }

    location /swaggerui/ {
        proxy_pass http://auth_api:8001/swaggerui/;
    }

    location /admin_panel {
        proxy_pass_header Server;
        proxy_set_header Host $host;
        proxy_redirect off;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header USE_X_FORWARDED_HOST True;
        proxy_set_header SCRIPT_NAME /admin_panel;
        proxy_connect_timeout 6000;
        proxy_read_timeout 6000;
        proxy_pass http://admin_django:8011;
    }

    location /static/ {
        autoindex on;
        alias /home/app/static/;
    }
}

```

***

Адреса сервисов
-

### Сервис оплаты(FastAPI)
Основной адрес https://moviesbilling.ddns.net  
Документация https://moviesbilling.ddns.net/app/openapi

### Сервис аутентификации(Flask)
Основной адрес https://moviesbilling.ddns.net/auth/  
Документация https://moviesbilling.ddns.net/auth/docs/  - swagger не работает(кидать запросы через Postman)

### Админ-панель(Django)
Основной адрес https://moviesbilling.ddns.net/admin_panel/  
Панель администратора https://moviesbilling.ddns.net/admin_panel/admin/  

### ELK
Основной адрес https://moviesbilling.ddns.net/kibana/

***

База данных
-
На проекте используется БД PostgreSQL 12.0.
Созданы 3 БД:  
*  billing_db - использует сервис оплаты
*  auth_db - использует сервис аутентификации
*  admin_db - использует сервис Админ-панель

***

Статьи
-
https://habr.com/ru/company/bitcalm/blog/234861/  
https://fingers.by/blog/how-to-integrate-a-payment-gateway-part-1 часть 1  
https://fingers.by/blog/how-to-integrate-a-payment-gateway-part-2 часть 2  
https://stripe.com/docs/api?lang=python Stripe документация  
https://medium.com/@mishraranjeet122/integrate-stripe-payment-with-a-card-in-python-e90989d39bca Stripe интеграция  
https://habr.com/ru/post/580866/ Как настроить SQLAlchemy, SQLModel и Alembic для асинхронной работы с FastAPI
