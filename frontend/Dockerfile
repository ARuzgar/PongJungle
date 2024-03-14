FROM nginx:alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf
#COPY ./proxy_params /etc/nginx/proxy_params

COPY templates /usr/share/nginx/html/templates
COPY static /usr/share/nginx/html/static
EXPOSE 80