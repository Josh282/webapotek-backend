from app.database import engine
from app.models.user import User

print("⚠️  Dropping 'users' table...")
User.__table__.drop(engine)
print("✅  Table 'users' dropped.")
