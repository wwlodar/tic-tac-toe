from app.app.main import create_app
from app.config import TestConfig

app = create_app(config_class=TestConfig)
