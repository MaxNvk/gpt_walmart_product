import logging
from flask import Blueprint
from src.services.agent_service import get_initial_message_async
from src.utils.response_util import prepare_success_response, prepare_error_response

logger = logging.getLogger(__name__)

agent_blueprint = Blueprint('agent_blueprint', __name__)

@agent_blueprint.route("/get-initial-message", methods=["GET"])
async def get_initial_message_route():
    try:
        logger.info("Handling get_initial_message request")
        response = await get_initial_message_async()
        return prepare_success_response({"message": response})
    except Exception as e:
        logger.exception("Error processing initial message")
        return prepare_error_response({"message": "Internal server error"}), 500