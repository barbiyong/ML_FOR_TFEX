from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('UpXgIaRQWYXI36lC7IV4Uqwv2vD1zpA8VWHnXhgPZ/0cuI/qtnBvhB6j8G08+ooeBxGUm+S894UryM+Ana5nsf6SGq4HiiwT7qSvFxZk77XLpBXAvah0K+FsHTu0nlGweayyJ+NYCZXZVGQXKaqjVwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1e0c49ab1c5adafb8d7c5d0750e89071')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
