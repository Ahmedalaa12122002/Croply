
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="ar">
    <head>
        <meta charset="UTF-8">
        <title>Telegram Web App</title>
    </head>
    <body style="text-align:center;font-family:Arial">
        <h1>✅ الويب شغال بنجاح</h1>
        <p>تم فتح التطبيق من داخل تلجرام 🚀</p>
    </body>
    </html>
    """
