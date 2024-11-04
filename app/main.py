import graphql_router as graphql_router
from api.v1.routers import author, health, user
from core.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi_pagination import add_pagination

app = FastAPI(title="Book Reviews", version=settings.RELEASE_ID)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


add_pagination(app)

app.include_router(
    router=graphql_router.graphql_app, prefix="/graphql", tags=["GraphQL"]
)

app.include_router(router=health.router, prefix=settings.API_V1_STR, tags=["health"])

app.include_router(router=user.router, prefix=settings.API_V1_STR, tags=["user"])
app.include_router(router=author.router, prefix=settings.API_V1_STR, tags=["author"])


@app.get(path="/", include_in_schema=False)
def refirect_to_docs() -> RedirectResponse:
    return RedirectResponse(url="/docs")
