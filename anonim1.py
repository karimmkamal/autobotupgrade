from telethon import TelegramClient, events
import os
import json
import telethon

api_id = 3388504
api_hash = 'fcb26adccf95496b5b258a3f51f6ab59'
client = TelegramClient('unfban', api_id, api_hash)
                    # crypto winner - crypto auto signals
source_target = {                     # this is not your channel, right?yes
                 -1001316654669: [-1001474202691],   # source_target = {-1001408408426: [-1001285034799]} wait because it will be on the other anonim not this oneç yes
                 }

#AlphaTradeZone® Premium | 1316654669
#CryptoAutoZignals - Premium | 1376355233
#Crypto winner | 1285034799
#CryptoAlpha - Premium | 1474202691


with open('messages.json', encoding='UTF-8') as json_file:
    messages = json.load(json_file)


@client.on(events.NewMessage(chats=list(source_target.keys())))
async def incoming(event: telethon.events.newmessage.NewMessage.Event):
    global messages
    channel = event.chat_id
    print(event.message.id)

    if str(channel) not in messages:
        messages[str(channel)] = {}
        for i in source_target[channel]:
            messages[str(channel)][str(i)] = {}

    message_in = event.message
    if event.media:
        media_path = await message_in.download_media()
    else:
        media_path = ''
    text_of_post = message_in.text

    if len(media_path) > 0:
        try:
            for i in source_target[channel]:
                message_out = await client.send_file(entity=i, file=media_path, caption="{}".format(text_of_post))
                messages[str(channel)][str(i)][str(event.message.id)] = str(message_out.id)
            os.remove(media_path)
        except Exception as e:
            print(e)

    else:
        for i in source_target[channel]:
            message_out = await client.send_message(entity=i, message="{}".format(text_of_post))
            messages[str(channel)][str(i)][str(event.message.id)] = str(message_out.id)


    with open('messages.json', 'w', encoding='UTF-8') as file:
        json.dump(messages, file)


@client.on(events.MessageEdited(chats=list(source_target.keys())))
async def editing(event: telethon.events.messageedited.MessageEdited):
    global messages
    channel = event.chat_id

    for i in source_target[channel]:
        await client.edit_message(entity=i, message=int(messages[str(channel)][str(i)][str(event.message.id)]),
                              text=event.message.text)


@client.on(events.MessageDeleted(chats=list(source_target.keys())))
async def deleting(event: telethon.events.messagedeleted.MessageDeleted.Event):
    global messages
    channel = event.chat_id
    for i in source_target[channel]:
        ids_to_delete = []
        for j in event.deleted_ids:
            ids_to_delete.append(messages[str(channel)][str(i)][str(j)])
        await client.delete_messages(entity=i, message_ids=ids_to_delete)


client.start()
client.run_until_disconnected()






















