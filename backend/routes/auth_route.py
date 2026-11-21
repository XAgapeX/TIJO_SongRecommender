import hashlib
import os
import re
import secrets
import smtplib
from email.message import EmailMessage
from time import time

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from ..database.db_init import get_db
from ..database.tables.users import Favorite, Session as UserSession, User
from ..database.tables.songs import Song
from ..schemas.auth_schema import (
    AuthRequest,
    AuthResponse,
    FavoriteRequest,
    RegisterRequest,
    RegistrationResponse,
    UserResponse,
)
from ..schemas.songs_schema import SongResponse

router = APIRouter(prefix="/auth", tags=["auth"])
registration_attempts: dict[str, list[float]] = {}


def validate_password(password: str) -> str | None:
    if len(password) < 8:
        return "Hasło musi mieć co najmniej 8 znaków"
    if not re.search(r"[a-z]", password) or not re.search(r"[A-Z]", password):
        return "Hasło musi zawierać małą i wielką literę"
    if not re.search(r"\d", password):
        return "Hasło musi zawierać cyfrę"
    return None


def send_verification_email(email: str, verification_url: str) -> None:
    host = os.getenv("SMTP_HOST")
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")
    if not host or not user or not password:
        return

    message = EmailMessage()
    message["Subject"] = "Potwierdź konto w Song Recommender"
    message["From"] = os.getenv("SMTP_FROM", user)
    message["To"] = email
    message.set_content(
        f"Cześć!\n\nPotwierdź swoje konto, klikając ten link:\n{verification_url}\n"
    )
    port = int(os.getenv("SMTP_PORT", "587"))
    with smtplib.SMTP(host, port, timeout=10) as server:
        server.starttls()
        server.login(user, password)
        server.send_message(message)


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000).hex()
    return f"{salt}${digest}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        salt, digest = password_hash.split("$", 1)
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000).hex()
        return secrets.compare_digest(actual, digest)
    except (ValueError, AttributeError):
        return False


def get_current_user(authorization: str | None = Header(default=None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Musisz się zalogować")

    token = authorization[7:]
    session = db.query(UserSession).filter(UserSession.token == token).first()
    if not session:
        raise HTTPException(status_code=401, detail="Sesja wygasła lub jest niepoprawna")

    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Użytkownik nie istnieje")
    return user


@router.post("/register", response_model=RegistrationResponse)
def register(http_request: Request, request: RegisterRequest, db: Session = Depends(get_db)):
    if request.website:
        raise HTTPException(status_code=400, detail="Nie udało się utworzyć konta")

    client_ip = http_request.client.host if http_request.client else "unknown"
    now = time()
    attempts = [attempt for attempt in registration_attempts.get(client_ip, []) if now - attempt < 3600]
    if len(attempts) >= 5:
        raise HTTPException(status_code=429, detail="Zbyt wiele prób rejestracji. Spróbuj ponownie później")
    attempts.append(now)
    registration_attempts[client_ip] = attempts

    email = request.email.strip().lower()
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise HTTPException(status_code=422, detail="Niepoprawny adres e-mail")
    if request.password != request.password_confirm:
        raise HTTPException(status_code=422, detail="Hasła muszą być identyczne")
    password_error = validate_password(request.password)
    if password_error:
        raise HTTPException(status_code=422, detail=password_error)
    if not request.terms_accepted:
        raise HTTPException(status_code=422, detail="Musisz zaakceptować regulamin i politykę prywatności")

    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=409, detail="Konto o tym adresie e-mail już istnieje")

    username = request.username.strip() if request.username and request.username.strip() else None
    if username and db.query(User).filter(User.username == username).first():
        raise HTTPException(status_code=409, detail="Nazwa użytkownika jest już zajęta")

    verification_token = secrets.token_urlsafe(32)
    user = User(
        username=username,
        email=email,
        password_hash=hash_password(request.password),
        is_verified=0,
        verification_token=verification_token,
        terms_accepted=1,
        marketing_consent=1 if request.marketing_consent else 0,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    verification_url = f"{frontend_url}/verify-email?token={verification_token}"
    try:
        send_verification_email(email, verification_url)
    except Exception:
        pass

    smtp_configured = all(os.getenv(name) for name in ("SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD"))
    return {
        "message": "Konto zostało utworzone. Sprawdź pocztę i potwierdź adres e-mail.",
        "verification_url": None if smtp_configured else verification_url,
    }


@router.post("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verification_token == token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Link potwierdzający jest niepoprawny lub wygasł")
    user.is_verified = 1
    user.verification_token = None
    db.commit()
    return {"ok": True, "message": "Adres e-mail został potwierdzony"}


@router.post("/login", response_model=AuthResponse)
def login(request: AuthRequest, db: Session = Depends(get_db)):
    email = request.email.strip().lower()
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Niepoprawny adres e-mail lub hasło")
    if not getattr(user, "is_verified", 0):
        raise HTTPException(status_code=403, detail="Najpierw potwierdź adres e-mail")

    token = secrets.token_urlsafe(32)
    db.add(UserSession(token=token, user_id=user.id))
    db.commit()
    return {"token": token, "user": UserResponse.model_validate(user)}


@router.post("/logout")
def logout(authorization: str | None = Header(default=None), db: Session = Depends(get_db)):
    if authorization and authorization.startswith("Bearer "):
        db.query(UserSession).filter(UserSession.token == authorization[7:].strip()).delete()
        db.commit()
    return {"ok": True}


@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)):
    return user


@router.get("/favorites", response_model=list[SongResponse])
def get_favorites(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    track_ids = [row.track_id for row in db.query(Favorite).filter(Favorite.user_id == user.id).all()]
    if not track_ids:
        return []
    songs = db.query(Song).filter(Song.track_id.in_(track_ids)).all()
    by_id = {song.track_id: song for song in songs}
    return [by_id[track_id] for track_id in track_ids if track_id in by_id]


@router.post("/favorites")
def add_favorite(request: FavoriteRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.track_id == request.track_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Piosenka nie istnieje")
    existing = db.query(Favorite).filter(Favorite.user_id == user.id, Favorite.track_id == request.track_id).first()
    if not existing:
        db.add(Favorite(user_id=user.id, track_id=request.track_id))
        db.commit()
    return {"ok": True}


@router.delete("/favorites/{track_id}")
def remove_favorite(track_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(Favorite).filter(Favorite.user_id == user.id, Favorite.track_id == track_id).delete()
    db.commit()
    return {"ok": True}
