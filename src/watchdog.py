import os
import telebot
from telebot import types
from dotenv import load_dotenv
import time
import sys

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
LOG_PATH = os.getenv('LOG_PATH', "/tmp")
bot = telebot.TeleBot(TOKEN)

# логика обработки сообщений в телеге
# 5 секунд на то чтобы ответить - ты ли подрубился по ssh или нет
# если ответа нет, значит по умолчанию считается что не ты
def check_access():
    remote_addr = os.getenv("PAM_RHOST", "unknown_rhost")

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Мужик", callback_data='yes'))
    markup.add(telebot.types.InlineKeyboardButton("Сука", callback_data='no'))
    
    sent_msg = bot.send_message(CHAT_ID, "Братишка, тут новенький заехал: " + remote_addr, reply_markup=markup)

    start_time = time.time()
    choice = None

    while time.time() - start_time < 5:
        updates = bot.get_updates(offset=-10) 
        for update in updates:
            if update.callback_query and update.callback_query.message.message_id == sent_msg.message_id:
                choice = update.callback_query.data
                bot.answer_callback_query(update.callback_query.id)
                break
        
        if choice:
            break
        time.sleep(1)

    if choice == 'yes':
        bot.edit_message_text("Заходи братан, кидай вещи", CHAT_ID, sent_msg.message_id)
        return True
    elif choice == 'no':
        bot.edit_message_text("Понял тебя. Сейчас обработаем перца", CHAT_ID, sent_msg.message_id)
        return False
    else:
        bot.edit_message_text("Ты хули молчишь", CHAT_ID, sent_msg.message_id)
        return False

# короче заменяем дефолтный /bin/bash или че у вас там
# на пиздатенький терминал внутри докера
# и пишем в лог файл все че делал пацанчик у нас в контейнере
def move_user_to_docker():
    log_filename = f"/suspicious_access_{int(time.time())}.log"
    log_path = LOG_PATH + log_filename

    docker_cmd = ["script", "-q", "-c", "docker run --hostname bebrian --rm -it debian /bin/bash", log_path]
    os.execvp("script", docker_cmd)

if __name__ == "__main__":
    allowed = check_access()
    if allowed:
        # если подтвердили в телеге
        os.execvp("/bin/bash", ["/bin/bash"])
    else:
        # если не ответили / нажали disallow
        move_user_to_docker()