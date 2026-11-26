#!/usr/bin/env bash
# Cloudflare Pages / any PaaS build script
set -e

pip install -r requirements.txt

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py seed_indian_data
