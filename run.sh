docker stop allauth_django
docker rm allauth_django
docker run -itd -p 443:443 --name allauth_django -v /root/allauth_django:/code  allauth_django
