from flask import jsonify

def prepare_success_response(data: object):
    return jsonify({
        "success": True,
        "data": data,
    })

def prepare_error_response(error): 
    return jsonify({
        "success": False,
        "error": error
    })