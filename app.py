from flask import Flask
from src.config.logging import configure_logging
from src.controllers.product_controller import product_blueprint
from src.controllers.agent_controller import agent_blueprint

# Initialize Flask app
app = Flask(__name__)

# Configure logging
configure_logging()

# Register blueprints for routes
app.register_blueprint(product_blueprint, url_prefix='/product')
app.register_blueprint(agent_blueprint, url_prefix='/agent')

if __name__ == "__main__":
    app.run(debug=True)