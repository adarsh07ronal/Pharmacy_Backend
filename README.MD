
# Pharmacy Backend
## Deployment Setup

## Steps:

#### ssh -i "pharmacy.pem" ubuntu@domain

#### sudo apt-get upgrade -y
#### sudo apt-get update -y

## Deploy Python virtual env
#### sudo apt-get install python3-venv -y
#### python3 -m venv env

## Install Django
#### pip3 install django

## Clone the git project

## Instal NGINX
#### sudo apt-get install nginx -y

## Create nginx configuration for django site
####     sudo vim /etc/nginx/sites-available/django.conf

    ####inhalt##
    server {
        listen 80;
        server_name IP-Address;

        location / {
            include proxy_params;
            proxy_pass http://unix:/home/ubuntu/Project/app.sock;
        }       
    }

## Secure Nginx
####  Follow https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04

################

## Test file configuration

    sudo ln /etc/nginx/sites-available/django.conf /etc/nginx/sites-enabled/

    1.open /etc/nginx/nginx.conf with write privileges
    2.uncomment or add server_names_hash_bucket_size 64 and change it to 128;
    3.restart nginx sudo service nginx restart

    sudo nginx -t


## restart NGINX server
#### sudo service nginx restart

-------------------------------------------------
#### Database Backup and DMS (POSTGRESQL/ OPTIONAL)
------------------------------------
    python -Xutf8 manage.py dumpdata > datadump.json
    python manage.py migrate --run-syncdb
    python manage.py loaddata datadump.json
-------------------------------------------------

-------------------------------------------------
#### Docker Microservices
------------------------------------

    Basic Installation (default Ubuntu) : https://docs.docker.com/engine/install/ubuntu/

    build containers : docker-compose -f docker-compose.prod.yml up --build -d

    restart services : docker-compose -f docker-compose.prod.yml restart

    Active Microservices : web, redis

    Currently Using Microservices: web
-------------------------------------------------

-------------------------------------------------
#### Cronjobs
------------------------------------
    docker container exec -it <container-id-main> bash
    python manage.py crontab add
    service cron restart
-------------------------------------------------

#### Github Actions:

## 1. Create Workflows

    name: Django CI

    on:
    push:
        branches: [ dev-main ]
    pull_request:
        branches: [ dev-main ]

    workflow_dispatch:
        branches: [ dev-main ]
    

    jobs:
    build:
        runs-on: ubuntu-latest
        steps:
        - uses: actions/checkout@v2

        - name: Project Server
            uses: appleboy/ssh-action@master
            with:
            HOST: ${{ secrets.Project}}
            USERNAME: ubuntu
            PASSWORD: ${{ secrets.Project_KEY }}
            PORT: 22
            script: ./deploy

#### sudo passwd ubuntu ----> creates password

#### sudo nano /etc/ssh/sshd_config
    PermitRootLogin prohibit-password to PermitRootLogin yes 
    PasswordAuthentication no to PasswordAuthentication yes

#### sudo service ssh restart

## 2. Add HOST nd KEY at Secrets.

    $ ssh-keygen -t ed25519 -C "your_email@example.com"
    $ eval "$(ssh-agent -s)"
    $ ssh-add ~/.ssh/id_ed25519

    copy the text from < ~/.ssh/id_ed25519.pub

    Add ssh key to account
    -----------------------------------------------------------------------------
    cat .ssh/id_rsa.pub | ssh ubuntu@ip-address 'cat >> .ssh/authorized_keys'

    clip < ~/.ssh/id_rsa        #(priv)
------------------------------------------------------------------------------
#### KEY : rsa private key
#### HOST : server hosT