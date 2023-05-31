from app.app.main import create_app
from app.config import Config

app = create_app(config_class=Config)

if __name__ == "__main__":
    app.run(debug=True)
