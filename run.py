import os
from src import create_app
from src.config import DevelopmentConfig, ProductionConfig

# Detect deployment environment
env = os.environ.get('FLASK_ENV', 'development')
if env == 'production':
    config = ProductionConfig
else:
    config = DevelopmentConfig

app = create_app(config)

if __name__ == '__main__':
    host = app.config.get('HOST', '0.0.0.0')
    port = app.config.get('PORT', 19191)
    debug = app.config.get('DEBUG', True)
    
    print(f" * Starting AeroDash Flask server on http://{host}:{port}/")
    print(f" * Current environment: {env.upper()}")
    
    app.run(host=host, port=port, debug=debug)
