from a2wsgi import ASGIMiddleware
from .application import app  # Import your FastAPI app.

application = ASGIMiddleware(app)