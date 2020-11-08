#!/bin/sh

usage() {
    cat << EOS
Usage: ./scripts/runserver.sh

Environment variables:
  DJANGO_SETTINGS_MODULE : Django settings module (required).
EOS
    exit 1
}

setup() {
    ./manage.py migrate
    ./manage.py compilemessages
}

run_unit() {
    setup
    ./manage.py runserver 0:8000
}

run_dev() {
    setup
    gunicorn \
        --bind 0:8000 \
        --workers 1 \
        --threads 1 \
        --capture-output \
        --reload \
        settings.wsgi:application
}

run_production() {
    gunicorn \
        --bind 0:8000 \
        --workers 1 \
        --threads 1 \
        --capture-output \
        --preload \
        settings.wsgi:application
}

case "${DJANGO_SETTINGS_MODULE}" in
    settings.env.unit)
        run_unit
        ;;
    settings.env.dev)
        run_dev
        ;;
    settings.env.stg|settings.env.prod)
        run_production
        ;;
    *)
        usage
        ;;
esac
