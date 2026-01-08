import logging
from fastapi import FastAPI
from app.api.v1 import auth, product
from app.core.config import settings
import sentry_sdk


logging.basicConfig(level=logging.INFO if settings.ENVIRONMENT == "production" else logging.DEBUG)

sentry_sdk.init(
    dsn="https://a68d25b1e9f67726586c7d2ecf3a5eee@o4510676295352320.ingest.de.sentry.io/4510676297384016",
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)
app = FastAPI(title="FastAPI E-commerce")


app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
app.include_router(product.router, prefix=settings.API_V1_STR, tags=["products"])


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI E-commerce!"}
