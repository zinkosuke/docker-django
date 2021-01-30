#!/bin/sh

usage() {
    cat << EOS
Usage: ./scripts/runserver.sh

Environment variables:
  DJANGO_SETTINGS_MODULE : Django settings module (required).
EOS
    exit 1
}

run_development() {
    ./manage.py migrate
    ./manage.py compilemessages
    PYTHONUNBUFFERED=1 ./manage.py runserver 0:8000
}

run_production() {
    ./manage.py compilemessages
    gunicorn \
        --bind 0:8000 \
        --workers 1 \
        --threads 1 \
        --capture-output \
        --preload \
        settings.wsgi:application
}

case "${DJANGO_SETTINGS_MODULE}" in
    settings.env.unit|settings.env.dev)
        run_development
        ;;
    settings.env.stg|settings.env.prod)
        run_production
        ;;
    *)
        usage
        ;;
esac
