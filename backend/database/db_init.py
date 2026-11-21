from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'song_recommender.db')}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def ensure_user_columns():
    """Adds the authentication columns to databases created by earlier versions."""
    import sqlite3

    with sqlite3.connect(os.path.join(BASE_DIR, "song_recommender.db")) as connection:
        columns = {row[1] for row in connection.execute("PRAGMA table_info(users)").fetchall()}
        username_info = next((row for row in connection.execute("PRAGMA table_info(users)").fetchall()
                              if row[1] == "username"), None)
        if username_info and username_info[3]:
            connection.execute("PRAGMA foreign_keys=OFF")
            connection.execute("""
                CREATE TABLE users_new (
                    id INTEGER NOT NULL PRIMARY KEY,
                    username VARCHAR,
                    email VARCHAR,
                    password_hash VARCHAR NOT NULL,
                    is_verified INTEGER NOT NULL DEFAULT 0,
                    verification_token VARCHAR,
                    terms_accepted INTEGER NOT NULL DEFAULT 0,
                    marketing_consent INTEGER NOT NULL DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            existing_columns = {row[1] for row in connection.execute("PRAGMA table_info(users)").fetchall()}
            if "email" in existing_columns:
                email_expression = "email"
            else:
                email_expression = "NULL"
            has_terms = "terms_accepted" in existing_columns
            has_marketing = "marketing_consent" in existing_columns
            has_verified = "is_verified" in existing_columns
            has_verification = "verification_token" in existing_columns
            has_created = "created_at" in existing_columns
            connection.execute(f"""
                INSERT INTO users_new
                    (id, username, email, password_hash, is_verified, verification_token,
                     terms_accepted, marketing_consent, created_at)
                SELECT
                    id,
                    NULLIF(username, ''),
                    {email_expression},
                    password_hash,
                    {'is_verified' if has_verified else '0'},
                    {'verification_token' if has_verification else 'NULL'},
                    {'terms_accepted' if has_terms else '0'},
                    {'marketing_consent' if has_marketing else '0'},
                    {'created_at' if has_created else 'CURRENT_TIMESTAMP'}
                FROM users
            """)
            connection.execute("DROP TABLE users")
            connection.execute("ALTER TABLE users_new RENAME TO users")
            connection.execute("CREATE UNIQUE INDEX IF NOT EXISTS ix_users_username ON users(username)")
            connection.execute("CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email ON users(email)")
            connection.execute("CREATE INDEX IF NOT EXISTS ix_users_id ON users(id)")
            connection.commit()
            connection.execute("PRAGMA foreign_keys=ON")
            columns = {row[1] for row in connection.execute("PRAGMA table_info(users)").fetchall()}
        additions = [
            ("email", "TEXT"),
            ("is_verified", "INTEGER NOT NULL DEFAULT 0"),
            ("verification_token", "TEXT"),
            ("terms_accepted", "INTEGER NOT NULL DEFAULT 0"),
            ("marketing_consent", "INTEGER NOT NULL DEFAULT 0"),
        ]
        for name, definition in additions:
            if name not in columns:
                connection.execute(f"ALTER TABLE users ADD COLUMN {name} {definition}")