from fastapi import FastAPI
from pathlib import Path
import os
from dotenv import load_dotenv

from backend.routes import auth_routes, chat_routes
from backend.routes.user_routes import router as user_router

from backend.db.database import SessionLocal, engine, Base
from backend.db.models import UserDB
from backend.auth.password_utils import hash_password

load_dotenv()

app = FastAPI(
    title="Company Internal Chatbot Backend",
    version="1.0.0",
)

def ensure_default_admin():
    db = SessionLocal()
    try:
        username = os.getenv("DEFAULT_ADMIN_USERNAME")
        password = os.getenv("DEFAULT_ADMIN_PASSWORD")
        role = os.getenv("DEFAULT_ADMIN_ROLE")

        if not username or not password:
            print("⚠️ DEFAULT_ADMIN_USERNAME or DEFAULT_ADMIN_PASSWORD not set")
            return

        admin_user = (
            db.query(UserDB)
            .filter(UserDB.username == username)
            .first()
        )

        if not admin_user:
            print("👤 Creating default admin user...")

            new_admin = UserDB(
                username=username,
                role=role,
                hashed_password=hash_password(password),
            )

            db.add(new_admin)
            db.commit()

            print("✅ Default admin created.\n")
        else:
            print("👤 Admin already exists.\n")

    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    print("\n🚀 Backend starting...\n")

    Base.metadata.create_all(bind=engine)
    ensure_default_admin()

    print("📦 Loading existing vector store only (no rebuild)...\n")
    print("✅ Startup complete.\n")


app.include_router(auth_routes.router)
app.include_router(chat_routes.router)
app.include_router(user_router)


@app.get("/")
def health():
    return {"status": "Backend is running"}
