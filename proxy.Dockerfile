# Build web part
FROM node:20-alpine AS build

COPY ./web /web
WORKDIR /web

RUN npm install && npm run build

# Make proxy
FROM nginx:1.29-alpine-slim AS proxy

RUN /bin/sh -c 'mkdir -p /etc/nginx/sites-enabled /var/www/hikehub.ru && rm /etc/nginx/conf.d/default.conf'
COPY ./nginx/ /etc/nginx/

COPY --from=build /web/dist /var/www/hikehub.ru
COPY ./app/organizer/static /var/www/hikehub.ru/static

EXPOSE 6161
