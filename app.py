from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

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
    msg = event.message.text
    r = '我看不懂你說什麼'

    if msg in ['位置', '地點', '店的地址']:
        location_message = LocationSendMessage(
            title='my location',
            address='Tokyo',
            latitude=35.65910807942215,
            longitude=139.70372892916203
        )
        
        line_bot_api.reply_message(
            event.reply_token,
            location_message
        )

    

    elif msg == '確認':
        Confirm_template = TemplateSendMessage(
        alt_text='目錄 template',
        template=ConfirmTemplate(
            title='這是ConfirmTemplate',
            text='這就是ConfirmTemplate,用於兩種按鈕選擇',
            actions=[                              
                PostbackTemplateAction(
                    label='Y',
                    text='Y',
                    data='action=buy&itemid=1'
                ),
                MessageTemplateAction(
                    label='N',
                    text='N'
                )
            ]
        )
    )

        line_bot_api.reply_message(
            event.reply_token,
            Confirm_template
        )

    elif msg == '商品目錄':
        image_carousel_template_message = TemplateSendMessage(
        alt_text='ImageCarousel template',
        template=ImageCarouselTemplate(
            columns=[
                ImageCarouselColumn(
                    image_url='https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png',
                    action=PostbackAction(
                        label='postback1',
                        display_text='postback text1',
                        data='action=buy&itemid=1'
                    )
                ),
                ImageCarouselColumn(
                    image_url='https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png',
                    action=PostbackAction(
                        label='postback2',
                        display_text='postback text2',
                        data='action=buy&itemid=2'
                    )
                )
            ]
        )
        )

        line_bot_api.reply_message(
            event.reply_token,
            image_carousel_template_message
        )

    else:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message
        )



    


if __name__ == "__main__":
    app.run()