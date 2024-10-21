from flask import Flask
from src.config.logging import configure_logging
from src.controllers.product_controller import product_blueprint
from src.controllers.agent_controller import agent_blueprint
import os
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flasgger import Swagger
from flask_cors import CORS


# Set the environment variable to use the in-project folder
os.environ['PROMETHEUS_MULTIPROC_DIR'] = os.path.join(os.getcwd(), 'prometheus_data')

# Initialize Flask app
app = Flask(__name__)

CORS(app)

swagger = Swagger(app, {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
})

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

# Configure logging
configure_logging()

# Register blueprints for routes
app.register_blueprint(product_blueprint, url_prefix='/product')
app.register_blueprint(agent_blueprint, url_prefix='/agent')

if __name__ == "__main__":
    app.run(debug=True)