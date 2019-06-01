from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('/db2rSDRM9HcQJweTZ1fMt6dy9IwyiHl6py93VaX7b7nb4rUKqJ6Nk9NcPUQlmKgdwI1JIv/CgaNh0IvTvQU1SVccS38Cv/qPEWJ8hLt4QlC+HnrUqhsOjniisWzrrwBTh1fmA4YEUkoU4nGwthbigdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('48ea983497d411af94e8083c39b8c5dc')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TemplateSendMessage(
    alt_text='Buttons template',
    template=ButtonsTemplate(
        thumbnail_image_url='https://example.com/image.jpg',
        title='Menu',
        text='Please select',
        actions=[
            PostbackAction(
                label='postback',
                text='postback text',
                data='action=buy&itemid=1'
            ),
            MessageAction(
                label='message',
                text='message text'
            ),
            URIAction(
                label='uri',
                uri='http://oinzen.com/'
            )
        ]
    )
)


if __name__ == "__main__":
    app.run()