FROM nginx:alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf
COPY certs     /etc/nginx/certs

COPY templates /usr/share/nginx/html/templates
COPY static /usr/share/nginx/html/static
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
