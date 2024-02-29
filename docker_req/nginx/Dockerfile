# Dockerfile for Nginx

# Base image olarak Nginx'in en son stabil sürümünü kullan
FROM nginx:latest

# Yazar/maintainer bilgisi (isteğe bağlı)
LABEL maintainer="berkay_inam@hotmail.com"
LABEL version="0.1" description="Bu docker nginx imizin ilk testi olacak kanzi xD"


# Nginx yapılandırma dosyasını kopyala
# Bu, container içindeki default Nginx yapılandırma dosyasını özelleştirilmiş yapılandırmanla değiştirir
COPY nginx.conf /etc/nginx/nginx.conf

# Eğer statik dosyalarınız varsa (HTML, CSS, JS, vb.) ve bunları Nginx ile servis etmek istiyorsanız,
# aşağıdaki gibi bir COPY komutu kullanabilirsiniz. Bu, dosyalarınızı Nginx'in
# statik dosya dizinine kopyalar
# COPY path/to/your/static/files /usr/share/nginx/html

# Nginx'in varsayılan portu olan 80'i dinlemesi için EXPOSE komutunu kullanabilirsiniz
# Bu, Dockerfile'ınızın okunabilirliğini artırır ve Nginx'in hangi portu dinlediğini belgelemiş olursunuz
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
