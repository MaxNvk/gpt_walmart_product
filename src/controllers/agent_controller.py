import logging
from flask import Blueprint
from src.services.agent_service import get_initial_message_async
from src.utils.response_util import prepare_success_response, prepare_error_response
from prometheus_client import Counter

logger = logging.getLogger(__name__)

initial_message_get = Counter('initial_message_proceeded', 'Total count of initial messages proceeded')

agent_blueprint = Blueprint('agent_blueprint', __name__)

@agent_blueprint.route("/get-initial-message", methods=["GET"])
async def get_initial_message_route():
    try:
        logger.info("Handling get_initial_message request")

        initial_message_get.inc()
        
        response = await get_initial_message_async()
        return prepare_success_response({"message": response})
    except Exception as e:
        logger.exception("Error processing initial message")
        return prepare_error_response({"message": "Internal server error"}), 500