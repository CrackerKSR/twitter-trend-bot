import time
import tweepy
from tweepy import OAuthHandler
from telethon import TelegramClient, events
from telethon.tl.custom import inlineresult, inlinebuilder
from telethon.tl.custom.button import Button
from telethon.tl.types import InputWebDocument,DocumentAttributeImageSize, DocumentAttributeFilename 
from telethon.client.dialogs import DialogMethods

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


from UserSetting import Setting
sett = Setting()

@client.on(events.InlineQuery)
async def handler(event):
#     print(f'event {time.strftime("%X")}')
    query_text = event.query.query
    builder = event.builder
    sender = event.sender
    
    Pref = Setting()
    Pref.fetch(sender.id)
    wid = Pref.woeid
    country = Pref.country
    # lat = 19.075983
    # lon = 72.877655
    # location = api.trends_closest(lat,lon)
    # print(location)


    # print(f'event.answer {time.strftime("%X")}')
    
    if '-loc' in query_text:
        results = [await current_location(event)]
    elif '1' in query_text:
        results = [i async for i in fetch(builder,1,"WORLD")]
        country = 'World' 
    elif 'in' in query_text:
        results = [i async for i in fetch(builder,23424848,"India")]
        country = 'India' 
    elif 'mum' in query_text:
        results = [i async for i in fetch(builder,2295411,"Mumbai")]    
        country = 'Mumbai' 
    elif 'nag' in query_text:
        results = [i async for i in fetch(builder,2282863,"Nagpur")]
        country = 'Nagpur' 
    elif 'del' in query_text:
        results = [i async for i in fetch(builder,20070458,"Delhi9")]
        country = 'Delhi9' 
    elif 'sur' in query_text:
        results = [i async for i in fetch(builder,2295405,"Surat")]
        country = 'Surat' 
    elif 'hyd' in query_text:
        results = [i async for i in fetch(builder,2295414,"Hyderabad")]
        country = 'Hyderabad' 
    else:
        results = [i async for i in fetch(builder,wid,country)]

    await event.answer(
        results=results,
        # cache_time = 10,
        # next_offset = '4',
        switch_pm=f"Trending in {country} | ⚙Settings",
        switch_pm_param='setting'
        )
    # print(f'answered on tele {time.strftime("%X")}')

@client.on(events.CallbackQuery)
async def handler(event):
    # print(event)
    pass

@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    # if 'setting' in event.message.message:
        # await set_location(event)
    await event.reply('type bot username to see current trends on twitter, also you can type commands to change the location on the go. \n currently supported commands are'\
        f'world: {bot} 1 '\
        f'india: {bot} in'\
        f'mumbai: {bot} mum'\
        f'hyderabad: {bot} hyd'\
        f'similary type first 3 letters for (nag)pur, (sur)at, (del)hi \n\n'\
        f'\n Check the top 10 trends anywhere on telegram*')


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
    print('change')
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


async def fetch(builder,wid,country):
    # print(f'in fetch {time.strftime("%X")}')
    # check user id and its preferences
    # pref = setting.get(id)
    # woeid = pref.User.woeid
    # top = pref.User.top
    # woeid = pre.manual.woeid
    # top = pref.manual.top
    wid = wid
    country = country
    # print(f'{wid=} {country=}')
    tr = api.trends_place(wid) # mumbai 2295411) #Nagpur- 2282863
    # print(tr[0]['locations'][0])
    t= [[i for i in t['trends']] for t in tr]

    # for i in t:
    #     i['url']
    # print(f'💙 {type(t)} - {t}')

    # print(f'after fetch {time.strftime("%X")}')
    rank = 0
    for i in t[0]:
        rank += 1
        yield builder.article(
            title = f'{rank} : {i["name"]}',
            description = f"Trending in {country} \nClick to view ",
            text=f'{rank} : {i["name"]}  \n\n[View]({i["url"]})',
            url = i['url'],
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

    # print(f'end loop {time.strftime("%X")}')

    
client.run_until_disconnected()
