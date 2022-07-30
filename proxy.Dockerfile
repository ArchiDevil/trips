FROM nginx:1.23 AS proxy

# install acme-nginx
RUN apt update -y; apt install python3-pip -y; pip3 install acme-nginx

EXPOSE 80 443

RUN /bin/sh -c 'mkdir -p /etc/nginx/sites-enabled /var/www/hikehub.ru'
RUN /bin/sh -c 'rm /etc/nginx/conf.d/default.conf'
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/conf.d /etc/nginx/conf.d/

COPY ./web/dist /var/www/hikehub.ru
COPY ./app/organizer/static /var/www/hikehub.ru/static

VOLUME [ "/etc/ssl/private/" ]
