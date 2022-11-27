FROM nginx:1.23.2-alpine
# copiando o arquivo de configuração do nginx
COPY ./conf/nginx.conf /etc/nginx/nginx.conf
# copiando os arquivos de configuração do site
COPY ./conf/conf.d/* /etc/nginx/conf.d/
