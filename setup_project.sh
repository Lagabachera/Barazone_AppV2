#!/bin/bash

PROJECT_NAME="Barazone_AppV2"
DJANGO_APPS=("purchases" "inventory" "sales" "transfers" "payments" "finance")
DB_NAME="barazone_db"
DB_USER="barazone_user"
DB_PASSWORD="Lezamoid35$&@"

echo "Step 1: Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Step 2: Installing Django and PostgreSQL adapter..."
pip install django psycopg2-binary djangorestframework

echo "Step 3: Creating Django project: $PROJECT_NAME"
django-admin startproject $PROJECT_NAME

cd $PROJECT_NAME

# Step 4: Create apps
echo "Step 4: Creating Django apps..."
for app in "${DJANGO_APPS[@]}"
do
  python manage.py startapp $app
  echo "App $app created!"
done

# Step 5: Update settings.py to include all apps
SETTINGS_FILE="$PROJECT_NAME/settings.py"

echo "Updating $SETTINGS_FILE"
cat <<EOL >> $SETTINGS_FILE

# Installed Django Apps for Barazone
INSTALLED_APPS += [
    'rest_framework',
EOL

for app in "${DJANGO_APPS[@]}"
do
  echo "    '$app'," >> $SETTINGS_FILE
done

cat <<EOL >> $SETTINGS_FILE
]

# PostgreSQL configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '$DB_NAME',
        'USER': '$DB_USER',
        'PASSWORD': '$DB_PASSWORD',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Static Files Setup
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
EOL

echo "Settings updated successfully!"

# Step 6: Create migrations for the apps
echo "Step 6: Making migrations..."
python manage.py makemigrations
python manage.py migrate

# Step 7: Create superuser
echo "Step 7: Creating superuser..."
python manage.py createsuperuser --username admin --email admin@example.com

echo "Step 8: Running the Django development server..."
python manage.py runserver
