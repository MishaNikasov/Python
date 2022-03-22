import pickle


def get_chat_list():
    try:
        with open('chat_list.pickle', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError as e:
        print(f'Ошибка считывания файла: {e}')
        return list()
    except EOFError as e:
        print(f'Ошибка считывания файла: {e}')
        return list()


def save_chat(chat_id):
    chat_list = get_chat_list()
    if chat_id in chat_list:
        return False
    else:
        chat_list.append(chat_id)
        __update_chat_list(chat_list)
        return True


def remove_chat(chat_id):
    chat_list = get_chat_list()
    if chat_id not in chat_list:
        return False
    else:
        chat_list.remove(chat_id)
        __update_chat_list(chat_list)
        return True


def __update_chat_list(chat_list):
    with open('chat_list.pickle', 'wb') as f:
        pickle.dump(chat_list, f)
