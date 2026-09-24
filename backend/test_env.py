import os

from dotenv import load_dotenv


load_dotenv()

app_id = os.getenv("ADZUNA_APP_ID")
app_key = os.getenv("ADZUNA_APP_KEY")

print(
    "App ID loaded:",
    bool(app_id)
)

print(
    "App Key loaded:",
    bool(app_key)
)