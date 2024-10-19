from flask import Flask, request, jsonify
from swarm import Swarm
from agents import product_info_agent, validation_agent, setup_completion_agent

app = Flask(__name__)

# Initialize Swarm client
client = Swarm()

# Endpoint to process the product data through the agents
@app.route('/process-product', methods=['POST'])
def process_product():
    # Step 1: Get product data from the user request
    product_data = request.json.get('data')

    # Step 2: Product Info Agent gathers and structures the data
    product_info_response = client.run(
        agent=product_info_agent,
        messages=[{"role": "user", "content": product_data}]
    )
    product_info = product_info_response.messages[-1]["content"]

    # Step 3: Validate the product info using Validation Agent
    validation_response = client.run(
        agent=validation_agent,
        messages=[{"role": "user", "content": product_info}]
    )
    validation_result = validation_response.messages[-1]["content"]

    # If validation fails, return an error message
    if "error" in validation_result.lower():
        return jsonify({"status": "error", "message": validation_result}), 400

    # Step 4: Finalize the setup with Setup Completion Agent
    setup_response = client.run(
        agent=setup_completion_agent,
        messages=[{"role": "user", "content": validation_result}]
    )
    setup_result = setup_response.messages[-1]["content"]

    # Return the final result
    return jsonify({
        "status": "success",
        "product_info": product_info,
        "validation_result": validation_result,
        "setup_result": setup_result
    })


if __name__ == '__main__':
    app.run(debug=True)