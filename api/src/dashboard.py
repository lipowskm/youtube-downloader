from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, Response, request
import rq_dashboard


def check_auth(
    username: str, valid_username: str, password: str, valid_password: str
) -> bool:
    """This function is called to check if a username password combination is valid."""
    return username == valid_username and password == valid_password


def authenticate() -> Response:
    """Sends a 401 response that enables basic auth."""
    return Response(
        "Could not verify your access level for that URL.\n"
        "You have to login with proper credentials",
        401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'},
    )


def basic_auth(username: Optional[str], password: Optional[str]) -> Optional[Response]:
    """Ensure basic authorization."""
    if not username or not password:
        return None
    auth = request.authorization
    if not auth or not check_auth(auth.username, username, auth.password, password):
        return authenticate()


def register_rq_dashboard(
    app: FastAPI,
    redis_url: str,
    endpoint: str,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> None:
    """Creates Flask app with RQ Dashboard and mounts it to FastAPI app."""
    flask_app = Flask(__name__)
    flask_app.config["RQ_DASHBOARD_REDIS_URL"] = redis_url
    rq_dashboard.web.setup_rq_connection(flask_app)
    rq_dashboard.blueprint.before_request(lambda: basic_auth(username, password))
    flask_app.register_blueprint(
        rq_dashboard.blueprint,
        url_prefix=f"/{endpoint.lstrip('/')}",
    )
    app.mount("/", WSGIMiddleware(flask_app))
