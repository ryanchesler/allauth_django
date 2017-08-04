docker stop allauth_django
docker rm allauth_django
docker run -it -p 443:443 --name allauth_django -v /home/arifur/workspace_python/allauth_app:/code  allauth_django