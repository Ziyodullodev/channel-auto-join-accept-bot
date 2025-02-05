import json, os
from datetime import datetime

if not os.path.exists('users.json'):
    with open('users.json', 'w') as f:
        json.dump({}, f)

async def check_user(chat_id):
    with open('users.json', 'r') as f:
        users = json.load(f)
        
    if str(chat_id) in users:
        return True 
    return False

async def add_user(message):
    check = await check_user(message.from_user.id)
    if not check:
        with open('users.json', 'r') as f:
            users = json.load(f)
        users[message.from_user.id] = {
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
            'username': message.from_user.username,
            'chat_id': message.from_user.id,
            'language_code': message.from_user.language_code,
            "from_chat_id": message.chat.id,
            "from_group": message.chat.title,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        with open('users.json', 'w') as f:
            json.dump(users, f)    
        
        
async def users_stat():
    with open('users.json', 'r') as f:
        users = json.load(f)
    return len(users)
