import os
import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://mukundlanetteam_db_user:SMiBXvFG3ROkgB52@mukund-crm.dnnqqi8.mongodb.net/")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
# Using 'pdf-editor' as default db name from the commented out line in ts file, 
# or letting the connection string decide if it has a db name. 
# The connection string in db.ts doesn't specify a db name at the end (just slash).
# Mongoose default might handle it, but Motor needs a db name usually if not in URI.
# I will use 'test' or 'pdf-editor' ?
# Looking at the original: mongodb+srv://.../  (no db name)
# But commented line had /pdf-editor
# I'll check if I can List Database names or just pick one.
# For now, I'll assume 'test' is default for Atlas if not specified, OR I should use a specific one.
# Re-reading db.ts: const conn = await mongoose.connect('.../');
# It might be writing to 'test' database or 'admin'. 
# I'll default to 'test' for now, but allow env var override.

DB_NAME = os.getenv("DB_NAME", "test") 
db = client[DB_NAME]
