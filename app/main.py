# app/main.py

from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database.connection import Base, engine
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse

from app.core.jwt_bearer import JWTBearer
from app.core.deps import get_current_user


# Side-effect imports
import app.models.user          # noqa: F401
import app.models.service       # noqa: F401
import app.models.availability  # noqa: F401
import app.models.booking       # noqa: F401
import app.models.review        # noqa: F401

app = FastAPI()

# Static and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


from app.routers import auth
from app.routers.users import router as users_router
from app.routers.services import router as services_router
from app.routers.availability import router as availability_router
from app.routers.Booking import router as booking_router
from app.routers.review import router as reviews_router
from app.routers.pages import router as pages_router


Base.metadata.create_all(bind=engine)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Booking Platform",
        version="1.0.0",
        description="API for freelancers and users",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/auth/login",
                    "scopes": {}
                }
            }
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"OAuth2PasswordBearer": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Include routers
app.include_router(auth.router)
app.include_router(users_router)
app.include_router(services_router)
app.include_router(availability_router)
app.include_router(booking_router)
app.include_router(reviews_router)
app.include_router(pages_router)

# Root page
@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse, dependencies=[Depends(JWTBearer())])
def dashboard_page(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})
