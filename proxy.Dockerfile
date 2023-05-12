# Build web part
FROM node:20 as build

COPY ./web /web
WORKDIR /web

RUN npm install && npm run build

# Make proxy
FROM nginx:1.23 AS proxy

# install acme-nginx
RUN apt update -y; apt install python3-pip -y; pip3 install acme-nginx

RUN /bin/sh -c 'mkdir -p /etc/nginx/sites-enabled /var/www/hikehub.ru && rm /etc/nginx/conf.d/default.conf'
COPY ./nginx/ /etc/nginx/

COPY --from=build /web/dist /var/www/hikehub.ru
COPY ./app/organizer/static /var/www/hikehub.ru/static

VOLUME [ "/etc/ssl/private/" ]
EXPOSE 80 443
