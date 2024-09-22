from flask import jsonify, request, current_app
from loguru import logger
import sys
import traceback
from flask import HTTPException
import sentry_sdk

def setup_logging():
    logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
    logger.add("logs/app.log", rotation="500 MB", retention="10 days")

def handle_error(e):
    error_details = {
        'error': str(e),
        'endpoint': request.endpoint,
        'method': request.method,
        'url': request.url,
        'headers': dict(request.headers),
        'args': request.args.to_dict(),
        'form': request.form.to_dict(),
        'json': request.json if request.is_json else None,
        'traceback': traceback.format_exc()
    }
    logger.error(f"An error occurred: {error_details}")
    
    if not current_app.config['DEBUG']:
        sentry_sdk.capture_exception(e)

    if isinstance(e, HTTPException):
        return jsonify(error=str(e)), e.code
    
    return jsonify(error="An unexpected error occurred. Our team has been notified."), 500

def initialize_error_handling(app):
    setup_logging()
    app.register_error_handler(Exception, handle_error)