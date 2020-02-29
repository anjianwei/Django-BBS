server {
    listen 81 ssl;
    ssl_certificate / root / anjianwei / domain.pem;
    ssl_certificate_key / root / anjianwei / domain.key;

    server_name neroi.xyz;  # here can also be the IP address of the server

    keepalive_timeout 5;
    client_max_body_size 4G;

    access_log /home/an/logs/nginx-access.log;
    error_log /home/an/logs/nginx-error.log;

    location /static/ {
        alias /home/an/staticfiles/;
    }

    # checks for static file, if not found proxy to app
    location / {
        try_files $uri @proxy_to_app;
    }

    location @proxy_to_app {
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header Host $http_host;
      proxy_redirect off;
      proxy_pass http://app_server;
    }


#uwsgi+nginx
    server{
        listen 8989 ssl;
        charset utf - 8;
        ssl_certificate /root/anjianwei/domain.pem;
        ssl_certificate_key /root/anjianwei/domain.key;
        server_name neroi.xyz;
        keepalive_timeout 5;
        client_max_body_size 4G;
        access_log  /home/an/logs/nginx-access.log;
        error_log   /home/an/logs/nginx-error.log;

        location / {
            include uwsgi_params;
            uwsgi_pass 0.0.0.0:8989;
            uwsgi_param UWSGI_SCRIPT myproject.wsgi;
            uwsgi_param UWSGI_CHDIR /home/an/Django-BBS/;
        }
        location /static/ {
            alias /home/an/Django-BBS/assets/
        }
    }
}