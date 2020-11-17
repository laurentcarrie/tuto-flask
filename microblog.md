



/etc/supervisor/conf.d/microblog.conf

    [program:microblog]
    command=/home/ubuntu/microblog/venv/bin/gunicorn -b localhost:8000 -w 4 microblog:app
    directory=/home/ubuntu/microblog
    user=ubuntu
    autostart=true
    autorestart=true
    stopasgroup=true
    killasgroup=true

sudo supervisorctl reload


    $ mkdir certs
    $ openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 \
      -keyout certs/key.pem -out certs/cert.pem

    nginx

/etc/nginx/sites-enabled/microblog

    server {
        # listen on port 80 (http)
        listen 80;
        server_name _;
        location / {
            # redirect any requests to the same URL but on https
            return 301 https://$host$request_uri;
        }
    }
    server {
        # listen on port 443 (https)
        listen 443 ssl;
        server_name _;

        # location of the self-signed SSL certificate
        ssl_certificate /home/ubuntu/microblog/certs/cert.pem;
        ssl_certificate_key /home/ubuntu/microblog/certs/key.pem;

        # write access and error logs to /var/log
        access_log /var/log/microblog_access.log;
        error_log /var/log/microblog_error.log;

        location / {
            # forward application requests to the gunicorn server
            proxy_pass http://localhost:8000;
            proxy_redirect off;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }

        location /static {
            # handle static files directly, without forwarding to the application
            alias /home/ubuntu/microblog/app/static;
            expires 30d;
        }
}



deploiement
-----------

    (venv) $ git pull                              # download the new version
    (venv) $ sudo supervisorctl stop microblog     # stop the current server
    ... pip install -r requirements.txt
    (venv) $ flask db upgrade                      # upgrade the database
    (venv) $ flask translate compile               # upgrade the translations
    (venv) $ sudo supervisorctl start microblog    # start a new server
