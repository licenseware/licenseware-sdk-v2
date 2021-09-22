DEBUG=true
ENVIRONMENT=local
PERSONAL_SUFFIX=_{{ personal_suffix }}
USE_BACKGROUND_WORKER=true

APP_ID={{ app_id }}
APP_HOST=http://localhost:5000

LWARE_IDENTITY_USER=John
LWARE_IDENTITY_PASSWORD=secret

AUTH_SERVICE_URL=http://localhost:5000/auth

REGISTRY_SERVICE_URL=http://localhost:5000/registry-service

FILE_UPLOAD_PATH=/tmp/lware

MONGO_DATABASE_NAME=db
MONGO_CONNECTION_STRING=mongodb://localhost:27017/db
REDIS_CONNECTION_STRING=redis://localhost:6379/0


