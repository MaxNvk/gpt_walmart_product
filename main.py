import logging
from flask import Flask, request
from swarm import Swarm
from src.config.agents import user_interface_agent, product_info_agent, validation_agent, setup_completion_agent
from src.utils import prepare_success_response, prepare_error_response

app = Flask(__name__)

# Initialize Swarm client
client = Swarm()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.before_request
def log_request_info():
    logger.info(f"Received request: {request.method} {request.url}")
    logger.info(f"Request body: {request.get_json()}")

@app.after_request
def log_response_info(response):
    logger.info(f"Response status: {response.status}")
    logger.info(f"Response body: {response.get_data(as_text=True)}")
    return response

@app.route("/get-initial-message", methods=["GET"])
def get_initial_message():
    logger.info("Handling get_initial_message request")
    response = client.run(
        agent=user_interface_agent,
        messages=[{"role": "user", "content": "Hi!"}]
    )

    return prepare_success_response({"message": response.messages[-1]["content"]})

@app.route("/process-product", methods=["POST"])
def process_product():
   logger.info("Handling process_product request")
   try:
        product_data = request.json.get("data")
        logger.info(f"Product data received: {product_data}")

        product_info_response = client.run(
            agent=product_info_agent,
            messages=[{"role": "user", "content": product_data}]
        )
        product_info = product_info_response.messages[-1]["content"]
        logger.info(f"Product info response: {product_info}")

        validation_response = client.run(
            agent=validation_agent,
            messages=[{"role": "user", "content": product_info}]
        )
        validation_result = validation_response.messages[-1]["content"]
        logger.info(f"Validation result: {validation_result}")

        if "error" in validation_result.lower():
            logger.error(f"Validation failed: {validation_result}")
            return prepare_error_response({"message": validation_result}), 400

        setup_response = client.run(
            agent=setup_completion_agent,
            messages=[{"role": "user", "content": validation_result}]
        )
        setup_result = setup_response.messages[-1]["content"]
        logger.info(f"Setup completion result: {setup_result}")

        return prepare_success_response({
            "status": "success",
            "product_info": product_info,
            "validation_result": validation_result,
            "setup_result": setup_result
        })
   except Exception as e:
       logger.exception("Error processing product")
       return prepare_error_response({"message": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True)