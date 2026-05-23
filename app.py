from fastapi import FastAPI

from chatbot.router import handle_message

app = FastAPI()


@app.get('/')
def home():

    return {
        'message': 'AI Banking Chatbot Running'
    }


@app.post('/chat')
def chat(
    message: str,
    account_id: str
):

    response = handle_message(
        message,
        account_id
    )

    return {
        'response': response
    }