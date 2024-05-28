from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from colorama import Fore, Style, init

init(autoreset=True)

api_id = 'apiid'  # Your API ID
api_hash = 'apihash'  # Your API HASH
phone_number = 'number'  # YOUR PHONE NUMBER

app = Client(
    'teamtrickyabhi',
    api_id=api_id,
    api_hash=api_hash,
    phone_number=phone_number,
)

custom_caption = "Your Caption"  # Your Caption you can use "" for no caption
replace_text = "Replace Text"  # Enter the text you want to replace.
your_text = "Your Text"  # Enter your text that you want to replace other's text with your own.

# Enter Source Channel and Your Channel - Also support multiple source and destination.
channel_mapping = {
    'sourcechannel1': ['destinationchannel1', 'destinationchannel2'],
    'sourcechannel2': ['destinationchannel2'],
    'sourcechannel3': ['destinationchannel2']
}

def join_chat(chat):
    try:
        print(f"{Fore.GREEN}Joining chat: {chat}")
        app.join_chat(chat)
    except UserAlreadyParticipant:
        print(f"{Fore.YELLOW}Already a participant in chat: {chat}")
    except Exception as e:
        print(f"{Fore.RED}Error joining chat '{chat}': {e}")

try:
    for source_chat, dest_chats in channel_mapping.items():
        join_chat(source_chat)
        for dest_chat in dest_chats:
            join_chat(dest_chat)
except Exception as e:
    print(f"{Fore.RED}Error during chat joining: {e}")

try:
    sources = [app.get_chat(source_chat) for source_chat in channel_mapping.keys()]
    destinations = [
        [app.get_chat(dest_chat) for dest_chat in dest_chats]
        for dest_chats in channel_mapping.values()
    ]
except Exception as e:
    print(f"{Fore.RED}Error getting chat objects: {e}")
app.stop()

@app.on_message(filters.chat(list(channel_mapping.keys())))
async def my_handler(client, message):
    final_caption = custom_caption

    for source, dests in zip(sources, destinations):
        try:
            if message.chat.id == source.id:
                print(f"{Fore.YELLOW}{message}")
                if message.caption:
                    edited_caption = message.caption.replace(replace_text, your_text)
                    final_caption = f"{edited_caption}\n{custom_caption}"
                    for dest in dests:
                        try:
                            await message.copy(dest.id, caption=final_caption)
                            print(f"{Fore.BLUE}Message copied to {dest.id} with caption: {final_caption}")
                        except Exception as e:
                            print(f"{Fore.RED}Error copying message to {dest.id}: {e}")
                elif message.text:
                    edited_text = message.text.replace(replace_text, your_text)
                    final_text = f"{edited_text}\n{custom_caption}"
                    for dest in dests:
                        try:
                            await app.send_message(dest.id, text=final_text)
                            print(f"{Fore.BLUE}Message sent to {dest.id} with text: {final_text}")
                        except Exception as e:
                            print(f"{Fore.RED}Error sending message to {dest.id}: {e}")
                else:
                    for dest in dests:
                        try:
                            await message.copy(dest.id, caption=final_caption)
                            print(f"{Fore.BLUE}Message copied to {dest.id} with caption: {final_caption}")
                        except Exception as e:
                            print(f"{Fore.RED}Error copying message to {dest.id}: {e}")
        except Exception as e:
            print(f"{Fore.RED}Error in message handling: {e}")

if __name__ == "__main__":
    app.run()
