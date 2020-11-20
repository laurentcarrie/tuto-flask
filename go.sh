#!/bin/bash

set -e
set -x

function postgres() {
  sudo docker stop postgres || true
sudo docker run -d \
    --name some-postgres \
    --rm \
    -e POSTGRES_PASSWORD=lolo \
    -e PGDATA=/var/lib/postgresql/data/pgdata \
    -e POSTGRES_HOST_AUTH_METHOD=password \
    -v /home/laurent/xxx:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres
}

function microblog() {
sudo docker stop lc92/microblog || true
sudo docker run \
  --name microblog \
  -d \
  -p 8000:5000 \
  --rm \
  --link some-postgres:dbserver \
  --link elasticsearch:elasticsearch \
  -e DATABASE_HOST=dbserver \
  -e DATABASE_PASSWORD=lolo \
  -e ELASTICSEARCH_URL=http://elasticsearch:9200 \
  -e REDIS_URL=redis://redis-server:6379/0 \
  lc92/microblog:latest
}

function build() {
  sudo docker build -t lc92/microblog:latest .
}

function push() {
  sudo docker push lc92/microblog:latest
}

function es() {
sudo docker run --name elasticsearch -d -p 9200:9200 -p 9300:9300 --rm \
    -e "discovery.type=single-node" \
    docker.elastic.co/elasticsearch/elasticsearch-oss:7.6.2
}

function psql() {
  sudo docker exec -it some-postgres psql -U postgres dbtest
}

function psql2() {
  sudo docker exec -it tuto-flask_yyy_1 psql -U postgres dbtest
}


function redis() {
  sudo docker run --name redis -d -p 6379:6379 redis:3-alpine
}

function start() {
  redis
  postgres
  es
  microblog
}

function stop() {
  sudo docker stop \
    tuto-flask_microblog_1 tuto-flask_yyy_1 tuto-flask_elasticsearch_1  \
    microblog some-postgres elasticsearch redis || true
  sudo docker rm \
    tuto-flask_microblog_1 tuto-flask_yyy_1 tuto-flask_elasticsearch_1 \
    microblog some-postgres elasticsearch redis

}


case $1 in
postgres)
	postgres
	;;
microblog)
	microblog
	;;
psql)
  psql
  ;;
psql2)
  psql2
  ;;
es)
  es
  ;;
build)
  build
  ;;
push)
  push
  ;;
start)
  start
  ;;
stop)
  stop
  ;;
redis)
  redis
  ;;
default)
	echo "no default"
esac
