from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.service import Service
from app.models.booking import Booking
from fastapi.templating import Jinja2Templates
from app.core.deps import try_get_current_user, role_required

router = APIRouter(tags=["Pages"])

templates = Jinja2Templates(directory="app/templates")

@router.get("/services")
def services_list(request: Request, db: Session = Depends(get_db)):
    # Protect page: redirect unauthenticated to /login
    current_user = try_get_current_user(request, db)
    if not current_user:
        return RedirectResponse(url="/login?reason=auth", status_code=302)
    services = db.query(Service).order_by(Service.created_at.desc()).limit(24).all()
    return templates.TemplateResponse("services/list.html", {"request": request, "services": services})


@router.get("/services/{service_id}/view")
def service_detail(service_id: int, request: Request, db: Session = Depends(get_db)):
    # Protect page
    current_user = try_get_current_user(request, db)
    if not current_user:
        return RedirectResponse(url="/login?reason=auth", status_code=302)
    service = db.query(Service).filter(Service.id == service_id).first()
    return templates.TemplateResponse("services/detail.html", {"request": request, "service": service})

# Back-compat: if someone hits the JSON API path directly, show the page instead
@router.get("/services/{service_id}")
def service_detail_redirect(service_id: int):
    return RedirectResponse(url=f"/services/{service_id}/view", status_code=302)

@router.get("/dashboard")
def dashboard_page(request: Request, db: Session = Depends(get_db)):
    # Require auth and redirect to role-specific dashboard
    current_user = try_get_current_user(request, db)
    if not current_user:
        return RedirectResponse(url="/login?reason=auth", status_code=302)
    role = getattr(current_user, "role", None)
    if role == "admin":
        return RedirectResponse(url="/dashboard/admin", status_code=302)
    if role == "freelancer":
        return RedirectResponse(url="/dashboard/freelancer", status_code=302)
    if role == "client":
        return RedirectResponse(url="/dashboard/client", status_code=302)
    return templates.TemplateResponse("dashboard/index.html", {"request": request})

@router.get("/dashboard/admin")
def dashboard_admin(request: Request, _user=Depends(role_required(["admin"]))):
    return templates.TemplateResponse("dashboard/index.html", {"request": request})

@router.get("/dashboard/freelancer")
def dashboard_freelancer(request: Request, _user=Depends(role_required(["freelancer"]))):
    return templates.TemplateResponse("dashboard/index.html", {"request": request})

@router.get("/dashboard/client")
def dashboard_client(request: Request, _user=Depends(role_required(["client"]))):
    return templates.TemplateResponse("dashboard/index.html", {"request": request})


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.get("/my/bookings")
def my_bookings(request: Request, db: Session = Depends(get_db)):
    current_user = try_get_current_user(request, db)
    if not current_user:
        return RedirectResponse(url="/login?reason=auth", status_code=302)
    bookings = db.query(Booking).order_by(Booking.created_at.desc()).limit(50).all()
    return templates.TemplateResponse("bookings/my.html", {"request": request, "bookings": bookings})

@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})

@router.get("/bookings/create")
def booking_create_page(request: Request, db: Session = Depends(get_db)):
    current_user = try_get_current_user(request, db)
    if not current_user:
        return RedirectResponse(url="/login?reason=auth", status_code=302)
    return templates.TemplateResponse("bookings/create.html", {"request": request})

@router.get("/book")
def book_page(request: Request, db: Session = Depends(get_db)):
    current_user = try_get_current_user(request, db)
    if not current_user:
        return RedirectResponse(url="/login?reason=auth", status_code=302)
    return templates.TemplateResponse("bookings/book.html", {"request": request})

@router.get("/availability/create")
def availability_create_page(request: Request, db: Session = Depends(get_db)):
    current_user = try_get_current_user(request, db)
    if not current_user:
        return RedirectResponse(url="/login?reason=auth", status_code=302)
    return templates.TemplateResponse("availability/create.html", {"request": request})

@router.get("/reviews/create")
def review_create_page(request: Request, db: Session = Depends(get_db)):
    current_user = try_get_current_user(request, db)
    if not current_user:
        return RedirectResponse(url="/login?reason=auth", status_code=302)
    return templates.TemplateResponse("reviews/create.html", {"request": request})

# Category pages
@router.get("/c/software-consultation")
def page_software_consultation(request: Request):
    return templates.TemplateResponse("categories/software-consultation.html", {"request": request})

@router.get("/c/language-tutoring")
def page_language_tutoring(request: Request):
    return templates.TemplateResponse("categories/language-tutoring.html", {"request": request})

@router.get("/c/business-coaching")
def page_business_coaching(request: Request):
    return templates.TemplateResponse("categories/business-coaching.html", {"request": request})

@router.get("/c/personal-training")
def page_personal_training(request: Request):
    return templates.TemplateResponse("categories/personal-training.html", {"request": request})

@router.get("/c/nutrition-consultation")
def page_nutrition_consultation(request: Request):
    return templates.TemplateResponse("categories/nutrition-consultation.html", {"request": request})


