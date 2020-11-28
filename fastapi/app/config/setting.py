import os
SQLALCHEMY_DATABASE_URI = \
    "mysql://admin:9Nw8v9yhx8uOb2nXVL8n@" \
    "taro.caxktie247nu.eu-west-1.rds.amazonaws.com/db_product"


if os.environ.get('PYTHON_ENV') == 'production':
    REDIS_HOST = 'redis'
else:
    REDIS_HOST = "54.155.60.51"
