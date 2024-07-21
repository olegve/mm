FROM nginx:latest
LABEL authors="ove"

RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
