from hydrogram import Client , filters, idle
from hydrogram.handlers import MessageHandler
from config import api_id, api_hash, bot_token, Channel_chat_id, admins
from handlers import giveaway_handler,listen_handler
from handlers import admin_start_handler , clear_all_handler,clear_redeemed_handler,clear_unredeemed_handler
from db import create_db_if_not_exists

bot_client = Client("giveaway_bot",api_id=api_id,api_hash=api_hash,bot_token=bot_token)

async def main():
    await create_db_if_not_exists()
    print("Starting up............")
    
    bot_client.add_handler(MessageHandler(listen_handler,filters.chat(Channel_chat_id)))

    
    ## admin only
    bot_client.add_handler(MessageHandler(admin_start_handler,filters.command("start") & filters.user(admins) ))
    bot_client.add_handler(MessageHandler(clear_redeemed_handler,filters.command("clear_redeemed") & filters.user(admins) ))
    bot_client.add_handler(MessageHandler(clear_unredeemed_handler, filters.command("clear_unredeemed") & filters.user(admins) ))
    bot_client.add_handler(MessageHandler(clear_all_handler, filters.command("clear_all") & filters.user(admins)))

    
    ## Non admin commands
    bot_client.add_handler(MessageHandler(giveaway_handler,filters.command("start") & ~filters.user(admins)))


    await bot_client.start()
    await idle()
    await bot_client.stop()

if __name__ == "__main__":
    bot_client.run(main())