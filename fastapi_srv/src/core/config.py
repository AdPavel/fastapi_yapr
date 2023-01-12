import os
from logging import config as logging_config

from .logger import LOGGING
from .settings import settings

logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = settings.project_name

# Настройки Redis
REDIS_HOST = settings.redis_host
REDIS_PORT = settings.redis_port

# Настройки Elasticsearch
ELASTIC_HOST = settings.els_host
ELASTIC_PORT = settings.els_port

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
