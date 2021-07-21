import time
import tweepy
from tweepy import OAuthHandler
from telethon import TelegramClient, events
from telethon.tl.custom import inlineresult, inlinebuilder
from telethon.tl.custom.button import Button
from telethon.tl.types import InputWebDocument,DocumentAttributeImageSize, DocumentAttributeFilename 
from telethon.client.dialogs import DialogMethods
import text
api_id = 936087
api_hash = '5f6f172f2107d79ed3e2929075a78058'
bot_token = '1945967714:AAFiB04cXAn4pnwaQzTc4q78YoNvDSvw2xQ'

client = TelegramClient('telethon_session', api_id, api_hash)
client.start(bot_token=bot_token)

consumer_key = 'BaD753vog7rygxpLtadm6bBpe'
consumer_secret = 'fR3IlwDumht4nV3HpBWQPxV1eTmyOXfA9NRSweuxBuHwAySgw7'
access_token = '2532009798-HdjyStZf5mY6VrQKiKkKA88INjghnGkHG2qovfU'
access_secret = 'ieu9aJcxwfP6w27Y5wU1xe8zuTi2G4kP6l9NKTtNe5FRS'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


# import  UserSetting
# print(f'init {time.strftime("%X")}')
# UserSetting.populate(li)
# print(f'populated {time.strftime("%X")}')
# print(li,end='\n')

# tr = api.trends_place(2282863) # mumbai 2295411)
# print(tr[0]['trends'][0])
# t = [[i['name'] for i in t['trends']] for t in tr]
# t = [i for i in tr[0]['trends']]
# print(tr[0]['as_of'])
# print(tr[0]['created_at'])
# print(tr[0]['locations'])
# print(tr[0]['locations'][0]["name"])
# print(tr[0]['locations'][0]["woeid"])

# ti = [[i for i in t['trends']] for t in tr][0]

# print(f'{ti[0]}')
# for i in ti:
#     name = t[i]
#     rank = i
#     print(f'#{rank}.{name}')


import twitter
import mongo
import re
pattern = re.compile(r'([aA-zZ]{2}).([aA-zZ]{3})')

@client.on(events.InlineQuery)
async def handler(event):
    #     print(f'event {time.strftime("%X")}')
    query, builder, sender = event.query.query, event.builder, event.sender 
    wid = 1
    if query.strip() == '':
        x = mongo.pref_exist(sender.id)
        # print(f'if {x=}')
    else:
        x = mongo.get_wid(query, sender.id)
        # print(f'else {x=}')
    location = ''
    if x is not None:
        wid = x['woeid']
        if x["name"] in x['country']:
            location = f'{x["country"]}'
        else:
            location = f'{x["name"]},{x["country"]}'
    else:
        wid = 1

    trends = twitter.get_trends(x['woeid'])
        # trends = twitter.trends(query_text, sender.id)
    results = [i async for i in build(builder,trends,location)]
    
    # results = [i async for i in fetch(builder,wid,country)]
    await event.answer(
        results=results,
        # cache_time = 10,
        # next_offset = '4',
        switch_pm=f"Trending in {location} | ⚙Settings",
        switch_pm_param='setting'
        )
    # print(f'answered on tele {time.strftime("%X")}')

@client.on(events.CallbackQuery)
async def handler(event):
    # print(event)
    pass

@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    # print(event)
    # if 'setting' in event.message.message:
        # await set_location(event)
    bot = "ttrend_bot"
    await event.reply(text.start)


@client.on(events.NewMessage(pattern="/set_location"))
async def set_location(event):
    # if '' in event.text:
    chat = event.message.peer_id.user_id
    async with client.conversation(chat) as conv:
        msg1 = await conv.send_message('Send Country Name \n You can also send your country code like US, IN ,BR ,JP etc. !')
        
        msg2 = await conv.get_response()
        
        if text := msg2.message:
            user_id=event.sender.id
            text = msg2.message
            s = Setting()
            status  = s.set(user_id, text)
            # print(status)
        # msg3 = await conv.get_reply()

        
    # await event.reply('send woeid or country name')
# @client.on(events.NewMessage)
# async def start(event):
    # print('change')
#     await event.reply('send woeid or country name')

# Defs
async def current_location(event):
    f'in setting: {time.strftime("%X")}'
    
    builder = event.builder
    tr = api.trends_place(2282863) # mumbai 2295411)

    text =  f'locations : {tr[0]["locations"][0]["name"]} \n'\
            f'woeid : {tr[0]["locations"][0]["woeid"]} \n'

    re = builder.article(
            title = f'Location: {tr[0]["locations"][0]["name"]}',
            description = "Go to ⚙settings to change location and more",
            text=text,
            thumb=InputWebDocument(
                url='http://assets.stickpng.com/images/580b57fcd9996e24bc43c53e.png',
                size=720,
                mime_type='image/png',
                attributes=[DocumentAttributeImageSize(w=100, h=100)]
                ),
            buttons=Button.url('Click here to visit new bot','example.com')
            )
    return re


async def build(builder,trends,location):
    
    rank = 0
    for t in trends[0]:
        rank += 1
        yield builder.article(
            title = f'{rank}: {t["name"]}',
            description = f"Trending in {location} \nClick to view ",
            text=f'{rank} : {t["name"]}  \n\n[View]({t["url"]})',
            url = t['url'],
            thumb=InputWebDocument(
                url='http://assets.stickpng.com/images/580b57fcd9996e24bc43c53e.png',
                size=720,
                mime_type='image/png',
                attributes=[DocumentAttributeImageSize(w=100, h=100)]
                ),
            buttons=Button.url('Click here to visit new bot','example.com')
            )
        if rank == 10:
            break


    # wid = wid
    # country = country
    # tr = api.trends_place(wid) # mumbai 2295411) #Nagpur- 2282863
    # t= [[i for i in t['trends']] for t in tr]

    # rank = 0
    # for i in t[0]:
    #     rank += 1
    #     yield builder.article(
    #         title = f'{rank} : {i["name"]}',
    #         description = f"Trending in {country} \nClick to view ",
    #         text=f'{rank} : {i["name"]}  \n\n[View]({i["url"]})',
    #         url = i['url'],
    #         thumb=InputWebDocument(
    #             url='http://assets.stickpng.com/images/580b57fcd9996e24bc43c53e.png',
    #             size=720,
    #             mime_type='image/png',
    #             attributes=[DocumentAttributeImageSize(w=100, h=100)]
    #             ),
    #         buttons=Button.url('Click here to visit new bot','example.com')
    #         )
    #     if rank == 10:
    #         break

    # print(f'end loop {time.strftime("%X")}')

    
client.run_until_disconnected()
