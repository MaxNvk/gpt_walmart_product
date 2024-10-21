import logging
from flask import Blueprint, request
from src.services.agent_service import process_product_data_async
from src.utils.response_util import prepare_success_response, prepare_error_response

logger = logging.getLogger(__name__)

product_blueprint = Blueprint('product_blueprint', __name__)

@product_blueprint.route("/process", methods=["POST"])
async def process_product():
    logger.info("Handling process_product request")
    try:
        product_data = request.json.get("data")
        logger.info(f"Product data received: {product_data}")

        response = await process_product_data_async(product_data)
        return prepare_success_response(response)

    except Exception as e:
        logger.exception("Error processing product")
        return prepare_error_response({"message": "Internal server error"}), 500