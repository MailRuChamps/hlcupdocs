FROM nginx:1.13
MAINTAINER Maksim Kislenko <m.kislenko@corp.mail.ru>

WORKDIR /etc/nginx/conf.d
COPY ./deploy/nginx.conf ./minimal.conf

RUN rm -f /etc/nginx/conf.d/default.conf

RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
	ln -sf /dev/stderr /var/log/nginx/error.log

EXPOSE 80

STOPSIGNAL SIGTERM

CMD ["nginx", "-g", "daemon off;"]
