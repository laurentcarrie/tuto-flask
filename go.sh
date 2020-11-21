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
  -p 8000:5000 \
  --rm \
  --link some-postgres:dbserver \
  --link elasticsearch:elasticsearch \
  --link redis:redis-server \
  -e DATABASE_HOST=dbserver \
  -e DATABASE_PASSWORD=lolo \
  -e DATABASE_USER=postgres \
  -e DATABASE_DB=dbtest \
  -e ELASTICSEARCH_HOST=elasticsearch \
  -e REDIS_URL=redis://redis-server:6379/0 \
  lc92/microblog:latest \
  bash boot.sh
}


function rq() {
sudo docker run \
  --name rq-worker \
  -d \
  --rm \
  --link some-postgres:dbserver \
  --link elasticsearch:elasticsearch \
  --link redis:redis-server \
  -e DATABASE_HOST=dbserver \
  -e DATABASE_PASSWORD=lolo \
  -e ELASTICSEARCH_HOST=elasticsearch \
  -e REDIS_URL=redis://redis-server:6379/0 \
  --entrypoint venv/bin/rq \
  lc92/microblog:latest \
  worker -u redis://redis-server:6379/0 microblog-tasks
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
  sudo docker exec -it tuto-flask_yyy_1 psql -U postgres dbtest $*
}


function redis() {
  sudo docker run --name redis -d -p 6379:6379 redis:3-alpine
}

function start() {
  stop || true
  redis
  postgres
  es
  rq
  microblog
}

function stop() {
  sudo docker stop \
    tuto-flask_microblog_1 tuto-flask_yyy_1 tuto-flask_elasticsearch_1 tuto-flask_redis_1 tuto-flask_worker_1 \
    microblog some-postgres elasticsearch redis rq-worker || true
  sudo docker rm \
    tuto-flask_microblog_1 tuto-flask_yyy_1 tuto-flask_elasticsearch_1 tuto-flask_redis_1 tuto-flask_worker_1 \
    lc92/microblog some-postgres elasticsearch redis rq-worker

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
rq)
  rq
  ;;
default)
	echo "no default"
esac
