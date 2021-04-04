from telethon import TelegramClient, events
import os
import json
import telethon

api_id = 3031240
api_hash = 'e8f49a2be88f834035d4124b8cb97d26'
client = TelegramClient('unfban2', api_id, api_hash)

source_target = {1408408426: [-1001285034799]}


with open('messages2.json', encoding='UTF-8') as json_file:
    messages = json.load(json_file)


@client.on(events.NewMessage(chats=list(source_target.keys())))
async def incoming(event: telethon.events.newmessage.NewMessage.Event):
    global messages
    channel = event.chat_id

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


    with open('messages2.json', 'w', encoding='UTF-8') as file:
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






















