from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from chatbot.router import handle_message

app = FastAPI()

# Serve web UI (static/index.html)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/')
def home():
    # Trả về web UI thay vì chuỗi JSON
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    except FileNotFoundError:
        return {
            'message': 'AI Banking Chatbot Running',
            'note': 'Web UI not found. Please ensure static/index.html exists.'
        }


@app.post('/chat')
def chat(body: dict):
    # UI gửi JSON dạng: {"message": "...", "account_id": "ACC..."}
    # (Giữ validate cơ bản để tránh lỗi 422 do body không đúng schema)
    try:
        message = body.get('message')
        account_id = body.get('account_id')
    except Exception:
        return {
            'response': 'Body không đúng định dạng JSON.'
        }

    if not message or not account_id:
        return {
            'response': 'Thiếu message hoặc account_id. Vui lòng gửi đúng JSON: {"message": "...", "account_id": "..."}'
        }

    response = handle_message(
        message,
        account_id
    )

    return {
        'response': response
    }
