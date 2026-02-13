import logging
from typing import Dict, List
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import json
import os
from datetime import datetime, timedelta
import random
import hashlib
import string
import asyncio

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = "8309717291:AAGJKse9kJPAAoOdr_a7Bk6AzN3Ettqyo_I"
ADMIN_ID = 7090250668
CHANNEL_USERNAME = "@CEBA_CLICER"

# Ранги пользователей
RANKS = {
    "user": "👤 Обычный пользователь",
    "vip": "⭐ VIP",
    "vip+": "✨ VIP+", 
    "vip++": "🌟 VIP++",
    "admin": "👑 Администратор",
    "admin+": "👑👑 Администратор+"
}

# NFT категории
NFT_CATEGORIES = {
    "common": {"name": "📦 Обычный NFT", "emoji": "📦", "price": 1000},
    "rare": {"name": "🎁 Редкий NFT", "emoji": "🎁", "price": 5000},
    "epic": {"name": "💎 Эпический NFT", "emoji": "💎", "price": 10000},
    "legendary": {"name": "🏆 Легендарный NFT", "emoji": "🏆", "price": 50000},
    "mythic": {"name": "🌌 Мифический NFT", "emoji": "🌌", "price": 100000}
}

# Множители для кейсов
CASE_MULTIPLIERS = {
    "common": {"name": "📦 Обычный кейс", "multipliers": [2, 3, 4], "chances": [50, 30, 20]},
    "rare": {"name": "🎁 Редкий кейс", "multipliers": [5, 6, 7], "chances": [40, 35, 25]},
    "epic": {"name": "💎 Эпический кейс", "multipliers": [8, 9, 10], "chances": [30, 40, 30]}
}

# ========== ХРАНИЛИЩЕ ДАННЫХ ==========

class UserData:
    def __init__(self):
        self.data_file = "users_data.json"
        self.accounts_file = "accounts.json"
        self.multipliers_file = "multipliers.json"
        self.sessions_file = "sessions.json"
        self.promocodes_file = "promocodes.json"
        self.used_promocodes_file = "used_promocodes.json"
        self.nft_file = "nft_collection.json"
        self.verification_file = "verification.json"
        self.channel_stats_file = "channel_stats.json"
        self.friends_file = "friends.json"
        self.duels_file = "duels.json"
        self.data = self.load_data()
        self.accounts = self.load_accounts()
        self.multipliers = self.load_multipliers()
        self.sessions = self.load_sessions()
        self.promocodes = self.load_promocodes()
        self.used_promocodes = self.load_used_promocodes()
        self.nft_collection = self.load_nft_collection()
        self.verification = self.load_verification()
        self.channel_stats = self.load_channel_stats()
        self.friends = self.load_friends()
        self.duels = self.load_duels()
    
    def load_data(self) -> Dict:
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def load_accounts(self) -> Dict:
        if os.path.exists(self.accounts_file):
            with open(self.accounts_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def load_multipliers(self) -> Dict:
        if os.path.exists(self.multipliers_file):
            with open(self.multipliers_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def load_sessions(self) -> Dict:
        if os.path.exists(self.sessions_file):
            with open(self.sessions_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def load_promocodes(self) -> Dict:
        if os.path.exists(self.promocodes_file):
            with open(self.promocodes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def load_used_promocodes(self) -> Dict:
        if os.path.exists(self.used_promocodes_file):
            with open(self.used_promocodes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def load_nft_collection(self) -> Dict:
        if os.path.exists(self.nft_file):
            with open(self.nft_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def load_verification(self) -> Dict:
        if os.path.exists(self.verification_file):
            with open(self.verification_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def load_channel_stats(self) -> Dict:
        if os.path.exists(self.channel_stats_file):
            with open(self.channel_stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "last_hourly_promo": None,
            "last_daily_promo": None,
            "last_weekly_promo": None,
            "total_promos_sent": 0,
            "hourly_promo_count": 0,
            "daily_promo_count": 0,
            "weekly_promo_count": 0
        }
    
    def load_friends(self) -> Dict:
        if os.path.exists(self.friends_file):
            with open(self.friends_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def load_duels(self) -> Dict:
        if os.path.exists(self.duels_file):
            with open(self.duels_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def save_accounts(self):
        with open(self.accounts_file, 'w', encoding='utf-8') as f:
            json.dump(self.accounts, f, ensure_ascii=False, indent=2)
    
    def save_multipliers(self):
        with open(self.multipliers_file, 'w', encoding='utf-8') as f:
            json.dump(self.multipliers, f, ensure_ascii=False, indent=2)
    
    def save_sessions(self):
        with open(self.sessions_file, 'w', encoding='utf-8') as f:
            json.dump(self.sessions, f, ensure_ascii=False, indent=2)
    
    def save_promocodes(self):
        with open(self.promocodes_file, 'w', encoding='utf-8') as f:
            json.dump(self.promocodes, f, ensure_ascii=False, indent=2)
    
    def save_used_promocodes(self):
        with open(self.used_promocodes_file, 'w', encoding='utf-8') as f:
            json.dump(self.used_promocodes, f, ensure_ascii=False, indent=2)
    
    def save_nft_collection(self):
        with open(self.nft_file, 'w', encoding='utf-8') as f:
            json.dump(self.nft_collection, f, ensure_ascii=False, indent=2)
    
    def save_verification(self):
        with open(self.verification_file, 'w', encoding='utf-8') as f:
            json.dump(self.verification, f, ensure_ascii=False, indent=2)
    
    def save_channel_stats(self):
        with open(self.channel_stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.channel_stats, f, ensure_ascii=False, indent=2)
    
    def save_friends(self):
        with open(self.friends_file, 'w', encoding='utf-8') as f:
            json.dump(self.friends, f, ensure_ascii=False, indent=2)
    
    def save_duels(self):
        with open(self.duels_file, 'w', encoding='utf-8') as f:
            json.dump(self.duels, f, ensure_ascii=False, indent=2)
    
    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    # ========== АККАУНТЫ И СЕССИИ ==========
    
    def create_account(self, username: str, password: str, telegram_id: int, telegram_username: str = "") -> bool:
        if username in self.accounts:
            return False
        
        self.accounts[username] = {
            "password_hash": self.hash_password(password),
            "telegram_id": telegram_id,
            "telegram_username": telegram_username,
            "created_at": datetime.now().isoformat(),
            "is_active": True,
            "verified": False,
            "verified_by": None,
            "verified_at": None
        }
        self.save_accounts()
        self.get_user(telegram_id)
        return True
    
    def authenticate(self, username: str, password: str) -> bool:
        if username not in self.accounts:
            return False
        
        account = self.accounts[username]
        if not account.get("is_active", True):
            return False
        
        return account["password_hash"] == self.hash_password(password)
    
    def get_account_by_telegram_id(self, telegram_id: int) -> Dict:
        for username, account in self.accounts.items():
            if account.get("telegram_id") == telegram_id:
                return {"username": username, **account}
        return {}
    
    def get_account_by_username(self, username: str) -> Dict:
        if username in self.accounts:
            return {"username": username, **self.accounts[username]}
        return {}
    
    def create_session(self, telegram_id: int, username: str):
        self.sessions[str(telegram_id)] = {
            "username": username,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=30)).isoformat()
        }
        self.save_sessions()
    
    def get_session(self, telegram_id: int) -> Dict:
        return self.sessions.get(str(telegram_id), {})
    
    def logout(self, telegram_id: int):
        if str(telegram_id) in self.sessions:
            del self.sessions[str(telegram_id)]
            self.save_sessions()
    
    # ========== ВЕРИФИКАЦИЯ ==========
    
    def verify_user(self, username: str, admin_username: str) -> bool:
        if username not in self.accounts:
            return False
        
        self.accounts[username]["verified"] = True
        self.accounts[username]["verified_by"] = admin_username
        self.accounts[username]["verified_at"] = datetime.now().isoformat()
        self.save_accounts()
        return True
    
    def unverify_user(self, username: str) -> bool:
        if username not in self.accounts:
            return False
        
        self.accounts[username]["verified"] = False
        self.accounts[username]["verified_by"] = None
        self.accounts[username]["verified_at"] = None
        self.save_accounts()
        return True
    
    def is_verified(self, username: str) -> bool:
        if username not in self.accounts:
            return False
        return self.accounts[username].get("verified", False)
    
    def get_formatted_username(self, username: str) -> str:
        if self.is_verified(username):
            return f"@{username} ☑️"
        return f"@{username}"
    
    # ========== СИСТЕМА ДРУЗЕЙ ==========
    
    def add_friend(self, user_id: int, friend_username: str) -> Dict:
        user_str = str(user_id)
        
        if user_str not in self.friends:
            self.friends[user_str] = {"friends": [], "pending": [], "sent": []}
        
        if friend_username not in self.accounts:
            return {"success": False, "message": "❌ Пользователь не найден"}
        
        account = self.get_account_by_telegram_id(user_id)
        if account.get("username") == friend_username:
            return {"success": False, "message": "❌ Нельзя добавить себя в друзья"}
        
        if friend_username in self.friends[user_str]["friends"]:
            return {"success": False, "message": "❌ Этот пользователь уже у вас в друзьях"}
        
        if friend_username in self.friends[user_str]["sent"]:
            return {"success": False, "message": "❌ Заявка уже отправлена"}
        
        self.friends[user_str]["sent"].append(friend_username)
        
        friend_str = str(self.accounts[friend_username]["telegram_id"])
        if friend_str not in self.friends:
            self.friends[friend_str] = {"friends": [], "pending": [], "sent": []}
        
        if friend_username not in self.friends[friend_str]["pending"]:
            self.friends[friend_str]["pending"].append(account.get("username"))
        
        self.save_friends()
        return {"success": True, "message": f"✅ Заявка в друзья отправлена @{friend_username}"}
    
    def accept_friend(self, user_id: int, friend_username: str) -> Dict:
        user_str = str(user_id)
        account = self.get_account_by_telegram_id(user_id)
        my_username = account.get("username")
        
        if user_str not in self.friends:
            return {"success": False, "message": "❌ Нет заявок"}
        
        if friend_username not in self.friends[user_str]["pending"]:
            return {"success": False, "message": "❌ Заявка не найдена"}
        
        self.friends[user_str]["pending"].remove(friend_username)
        
        if friend_username not in self.friends[user_str]["friends"]:
            self.friends[user_str]["friends"].append(friend_username)
        
        friend_account = self.accounts[friend_username]
        friend_str = str(friend_account["telegram_id"])
        
        if friend_str not in self.friends:
            self.friends[friend_str] = {"friends": [], "pending": [], "sent": []}
        
        if my_username in self.friends[friend_str]["sent"]:
            self.friends[friend_str]["sent"].remove(my_username)
        
        if my_username not in self.friends[friend_str]["friends"]:
            self.friends[friend_str]["friends"].append(my_username)
        
        self.save_friends()
        return {"success": True, "message": f"✅ Вы и @{friend_username} теперь друзья!"}
    
    def decline_friend(self, user_id: int, friend_username: str) -> Dict:
        user_str = str(user_id)
        account = self.get_account_by_telegram_id(user_id)
        my_username = account.get("username")
        
        if user_str not in self.friends:
            return {"success": False, "message": "❌ Нет заявок"}
        
        if friend_username not in self.friends[user_str]["pending"]:
            return {"success": False, "message": "❌ Заявка не найдена"}
        
        self.friends[user_str]["pending"].remove(friend_username)
        
        friend_account = self.accounts[friend_username]
        friend_str = str(friend_account["telegram_id"])
        
        if friend_str in self.friends and my_username in self.friends[friend_str]["sent"]:
            self.friends[friend_str]["sent"].remove(my_username)
        
        self.save_friends()
        return {"success": True, "message": f"❌ Заявка от @{friend_username} отклонена"}
    
    def remove_friend(self, user_id: int, friend_username: str) -> Dict:
        user_str = str(user_id)
        account = self.get_account_by_telegram_id(user_id)
        my_username = account.get("username")
        
        if user_str not in self.friends:
            return {"success": False, "message": "❌ У вас нет друзей"}
        
        if friend_username not in self.friends[user_str]["friends"]:
            return {"success": False, "message": "❌ Этот пользователь не у вас в друзьях"}
        
        self.friends[user_str]["friends"].remove(friend_username)
        
        friend_account = self.accounts[friend_username]
        friend_str = str(friend_account["telegram_id"])
        
        if friend_str in self.friends and my_username in self.friends[friend_str]["friends"]:
            self.friends[friend_str]["friends"].remove(my_username)
        
        self.save_friends()
        return {"success": True, "message": f"❌ @{friend_username} удален из друзей"}
    
    def get_friends(self, user_id: int) -> List[str]:
        user_str = str(user_id)
        if user_str not in self.friends:
            return []
        return self.friends[user_str].get("friends", [])
    
    def get_pending_requests(self, user_id: int) -> List[str]:
        user_str = str(user_id)
        if user_str not in self.friends:
            return []
        return self.friends[user_str].get("pending", [])
    
    def get_sent_requests(self, user_id: int) -> List[str]:
        user_str = str(user_id)
        if user_str not in self.friends:
            return []
        return self.friends[user_str].get("sent", [])
    
    # ========== СИСТЕМА ДУЭЛЕЙ ==========
    
    def create_duel(self, creator_id: int, opponent_username: str, duration: int, bet: int = 0) -> Dict:
        creator_account = self.get_account_by_telegram_id(creator_id)
        creator_username = creator_account.get("username")
        
        if opponent_username not in self.accounts:
            return {"success": False, "message": "❌ Противник не найден"}
        
        if creator_username == opponent_username:
            return {"success": False, "message": "❌ Нельзя вызвать на дуэль самого себя"}
        
        opponent_id = self.accounts[opponent_username]["telegram_id"]
        duel_id = f"{creator_id}_{opponent_id}_{datetime.now().timestamp()}"
        
        creator_data = self.get_user(creator_id)
        if creator_data.get("clicks", 0) < bet:
            return {"success": False, "message": f"❌ У вас недостаточно кликов для ставки {bet:,}"}
        
        self.duels[duel_id] = {
            "id": duel_id,
            "creator_id": creator_id,
            "creator_username": creator_username,
            "opponent_id": opponent_id,
            "opponent_username": opponent_username,
            "status": "waiting",
            "duration": duration,
            "bet": bet,
            "created_at": datetime.now().isoformat(),
            "started_at": None,
            "finished_at": None,
            "creator_clicks": 0,
            "opponent_clicks": 0,
            "winner": None,
            "creator_accepted": False,
            "opponent_accepted": False
        }
        
        self.save_duels()
        return {"success": True, "message": f"✅ Дуэль создана! Ожидание ответа от @{opponent_username}", "duel_id": duel_id}
    
    def accept_duel(self, user_id: int, duel_id: str) -> Dict:
        if duel_id not in self.duels:
            return {"success": False, "message": "❌ Дуэль не найдена"}
        
        duel = self.duels[duel_id]
        
        if duel["status"] != "waiting":
            return {"success": False, "message": "❌ Эта дуэль уже началась или завершена"}
        
        if user_id != duel["opponent_id"]:
            return {"success": False, "message": "❌ Это не ваша дуэль"}
        
        opponent_data = self.get_user(user_id)
        if opponent_data.get("clicks", 0) < duel["bet"]:
            return {"success": False, "message": f"❌ У вас недостаточно кликов для ставки {duel['bet']:,}"}
        
        creator_data = self.get_user(duel["creator_id"])
        creator_data["clicks"] = creator_data.get("clicks", 0) - duel["bet"]
        self.update_user(duel["creator_id"], creator_data)
        
        opponent_data["clicks"] = opponent_data.get("clicks", 0) - duel["bet"]
        self.update_user(user_id, opponent_data)
        
        duel["status"] = "active"
        duel["started_at"] = datetime.now().isoformat()
        duel["opponent_accepted"] = True
        duel["creator_accepted"] = True
        
        self.save_duels()
        return {"success": True, "message": f"✅ Дуэль принята! Бой начнется через 5 секунд!", "duel_id": duel_id}
    
    def decline_duel(self, user_id: int, duel_id: str) -> Dict:
        if duel_id not in self.duels:
            return {"success": False, "message": "❌ Дуэль не найдена"}
        
        duel = self.duels[duel_id]
        
        if duel["status"] != "waiting":
            return {"success": False, "message": "❌ Эта дуэль уже началась или завершена"}
        
        if user_id != duel["opponent_id"]:
            return {"success": False, "message": "❌ Это не ваша дуэль"}
        
        duel["status"] = "finished"
        duel["finished_at"] = datetime.now().isoformat()
        duel["winner"] = "declined"
        
        self.save_duels()
        return {"success": True, "message": f"❌ Дуэль отклонена"}
    
    def add_duel_click(self, user_id: int, duel_id: str) -> Dict:
        if duel_id not in self.duels:
            return {"success": False, "message": "❌ Дуэль не найдена"}
        
        duel = self.duels[duel_id]
        
        if duel["status"] != "active":
            return {"success": False, "message": "❌ Дуэль не активна"}
        
        start_time = datetime.fromisoformat(duel["started_at"])
        if datetime.now() > start_time + timedelta(seconds=duel["duration"]):
            return self.finish_duel(duel_id)
        
        if user_id == duel["creator_id"]:
            duel["creator_clicks"] += 1
        elif user_id == duel["opponent_id"]:
            duel["opponent_clicks"] += 1
        else:
            return {"success": False, "message": "❌ Вы не участвуете в этой дуэли"}
        
        self.save_duels()
        return {"success": True, "message": "Клик засчитан!", "duel_id": duel_id}
    
    def finish_duel(self, duel_id: str) -> Dict:
        if duel_id not in self.duels:
            return {"success": False, "message": "❌ Дуэль не найдена"}
        
        duel = self.duels[duel_id]
        
        if duel["status"] != "active":
            return {"success": False, "message": "❌ Дуэль уже завершена"}
        
        duel["status"] = "finished"
        duel["finished_at"] = datetime.now().isoformat()
        
        if duel["creator_clicks"] > duel["opponent_clicks"]:
            duel["winner"] = duel["creator_username"]
            winner_id = duel["creator_id"]
            
            winner_data = self.get_user(winner_id)
            winner_data["clicks"] = winner_data.get("clicks", 0) + duel["bet"] * 2
            winner_data["duels_won"] = winner_data.get("duels_won", 0) + 1
            self.update_user(winner_id, winner_data)
            
            loser_data = self.get_user(duel["opponent_id"])
            loser_data["duels_lost"] = loser_data.get("duels_lost", 0) + 1
            self.update_user(duel["opponent_id"], loser_data)
            
        elif duel["opponent_clicks"] > duel["creator_clicks"]:
            duel["winner"] = duel["opponent_username"]
            winner_id = duel["opponent_id"]
            
            winner_data = self.get_user(winner_id)
            winner_data["clicks"] = winner_data.get("clicks", 0) + duel["bet"] * 2
            winner_data["duels_won"] = winner_data.get("duels_won", 0) + 1
            self.update_user(winner_id, winner_data)
            
            loser_data = self.get_user(duel["creator_id"])
            loser_data["duels_lost"] = loser_data.get("duels_lost", 0) + 1
            self.update_user(duel["creator_id"], loser_data)
            
        else:
            duel["winner"] = "draw"
            
            creator_data = self.get_user(duel["creator_id"])
            creator_data["clicks"] = creator_data.get("clicks", 0) + duel["bet"]
            creator_data["duels_draw"] = creator_data.get("duels_draw", 0) + 1
            self.update_user(duel["creator_id"], creator_data)
            
            opponent_data = self.get_user(duel["opponent_id"])
            opponent_data["clicks"] = opponent_data.get("clicks", 0) + duel["bet"]
            opponent_data["duels_draw"] = opponent_data.get("duels_draw", 0) + 1
            self.update_user(duel["opponent_id"], opponent_data)
        
        self.save_duels()
        return {"success": True, "message": "Дуэль завершена!", "duel": duel}
    
    def get_active_duel(self, user_id: int) -> Dict:
        for duel_id, duel in self.duels.items():
            if duel["status"] == "active":
                if user_id == duel["creator_id"] or user_id == duel["opponent_id"]:
                    duel["id"] = duel_id
                    return duel
        return None
    
    def get_user_duels(self, user_id: int) -> List[Dict]:
        user_duels = []
        for duel_id, duel in self.duels.items():
            if user_id == duel["creator_id"] or user_id == duel["opponent_id"]:
                duel["id"] = duel_id
                user_duels.append(duel)
        return user_duels
    
    # ========== ИГРОВЫЕ ДАННЫЕ ==========
    
    def get_user(self, user_id: int) -> Dict:
        user_id_str = str(user_id)
        
        if user_id_str not in self.data:
            self.data[user_id_str] = {
                "clicks": 0,
                "rank": "user",
                "username": "",
                "total_clicks": 0,
                "cases_opened": 0,
                "duels_won": 0,
                "duels_lost": 0,
                "duels_draw": 0,
                "registered_at": datetime.now().isoformat(),
                "last_login": datetime.now().isoformat(),
                "promocodes_used": [],
                "nft_collection": []
            }
            self.save_data()
        else:
            user_data = self.data[user_id_str]
            defaults = {
                "total_clicks": user_data.get("clicks", 0),
                "cases_opened": 0,
                "duels_won": 0,
                "duels_lost": 0,
                "duels_draw": 0,
                "username": user_data.get("username", ""),
                "registered_at": user_data.get("registered_at", datetime.now().isoformat()),
                "last_login": datetime.now().isoformat(),
                "promocodes_used": user_data.get("promocodes_used", []),
                "nft_collection": user_data.get("nft_collection", [])
            }
            
            for key, default_value in defaults.items():
                if key not in user_data:
                    user_data[key] = default_value
            
            self.data[user_id_str] = user_data
        
        return self.data[user_id_str]
    
    def update_user(self, user_id: int, data: Dict):
        self.data[str(user_id)] = data
        self.save_data()
    
    def get_top_users(self, limit: int = 15) -> List[tuple]:
        users = []
        for user_id_str, user_data in self.data.items():
            username = user_data.get("username", "Без имени")
            clicks = user_data.get("clicks", 0)
            total_clicks = user_data.get("total_clicks", clicks)
            rank = user_data.get("rank", "user")
            
            users.append((int(user_id_str), username, clicks, total_clicks, rank))
        
        users.sort(key=lambda x: x[2], reverse=True)
        return users[:limit]
    
    def get_top_duelists(self, limit: int = 10) -> List[tuple]:
        duelists = []
        for user_id_str, user_data in self.data.items():
            username = user_data.get("username", "Без имени")
            wins = user_data.get("duels_won", 0)
            losses = user_data.get("duels_lost", 0)
            draws = user_data.get("duels_draw", 0)
            total = wins + losses + draws
            
            duelists.append((int(user_id_str), username, wins, losses, draws, total))
        
        duelists.sort(key=lambda x: x[2], reverse=True)
        return duelists[:limit]
    
    def get_all_accounts(self) -> List[Dict]:
        accounts_list = []
        for username, account_data in self.accounts.items():
            telegram_id = account_data.get("telegram_id")
            user_data = self.get_user(telegram_id) if telegram_id else {}
            
            accounts_list.append({
                "username": username,
                "telegram_id": telegram_id,
                "telegram_username": account_data.get("telegram_username", ""),
                "clicks": user_data.get("clicks", 0),
                "rank": user_data.get("rank", "user"),
                "created_at": account_data.get("created_at", ""),
                "is_active": account_data.get("is_active", True),
                "verified": account_data.get("verified", False)
            })
        return accounts_list
    
    # ========== МНОЖИТЕЛИ ==========
    
    def set_multiplier(self, user_id: int, multiplier: int, duration_minutes: int = 10):
        expires = datetime.now() + timedelta(minutes=duration_minutes)
        self.multipliers[str(user_id)] = {
            "multiplier": multiplier,
            "expires": expires.timestamp()
        }
        self.save_multipliers()
    
    def get_multiplier(self, user_id: int) -> int:
        user_str = str(user_id)
        if user_str in self.multipliers:
            multiplier_data = self.multipliers[user_str]
            if datetime.now().timestamp() < multiplier_data["expires"]:
                return multiplier_data["multiplier"]
            else:
                del self.multipliers[user_str]
                self.save_multipliers()
        return 1
    
    # ========== КЛИКИ ==========
    
    def add_clicks(self, user_id: int, amount: int):
        user_data = self.get_user(user_id)
        user_data["clicks"] = user_data.get("clicks", 0) + amount
        if amount > 0:
            user_data["total_clicks"] = user_data.get("total_clicks", 0) + amount
        self.update_user(user_id, user_data)
    
    def remove_clicks(self, user_id: int, amount: int):
        user_data = self.get_user(user_id)
        current_clicks = user_data.get("clicks", 0)
        if amount > current_clicks:
            user_data["clicks"] = 0
        else:
            user_data["clicks"] = current_clicks - amount
        self.update_user(user_id, user_data)
    
    # ========== ПРОМОКОДЫ ==========
    
    def generate_promocode(self, length: int = 8) -> str:
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    def create_promocode(self, code: str, reward_type: str, reward_value: int, 
                         uses_limit: int = 100, expires_days: int = 30) -> bool:
        if code in self.promocodes:
            return False
        
        expires_at = datetime.now() + timedelta(days=expires_days)
        
        self.promocodes[code] = {
            "code": code,
            "reward_type": reward_type,
            "reward_value": reward_value,
            "uses_limit": uses_limit,
            "uses_count": 0,
            "created_at": datetime.now().isoformat(),
            "expires_at": expires_at.isoformat(),
            "is_active": True,
            "created_by": "admin",
            "channel_promo": False
        }
        self.save_promocodes()
        return True
    
    def create_channel_promocode(self, reward_type: str, reward_value: int, 
                                 uses_limit: int = 1000, expires_days: int = 1) -> str:
        code = self.generate_promocode(10)
        expires_at = datetime.now() + timedelta(days=expires_days)
        
        self.promocodes[code] = {
            "code": code,
            "reward_type": reward_type,
            "reward_value": reward_value,
            "uses_limit": uses_limit,
            "uses_count": 0,
            "created_at": datetime.now().isoformat(),
            "expires_at": expires_at.isoformat(),
            "is_active": True,
            "created_by": "channel",
            "channel_promo": True
        }
        self.save_promocodes()
        return code
    
    def use_promocode(self, user_id: int, code: str) -> Dict:
        if code not in self.promocodes:
            return {"success": False, "message": "❌ Промокод не найден"}
        
        promocode = self.promocodes[code]
        
        if not promocode.get("is_active", True):
            return {"success": False, "message": "❌ Промокод не активен"}
        
        expires_at = datetime.fromisoformat(promocode.get("expires_at", datetime.now().isoformat()))
        if datetime.now() > expires_at:
            return {"success": False, "message": "❌ Промокод просрочен"}
        
        uses_count = promocode.get("uses_count", 0)
        uses_limit = promocode.get("uses_limit", 1)
        if uses_count >= uses_limit:
            return {"success": False, "message": "❌ Лимит использований промокода исчерпан"}
        
        user_data = self.get_user(user_id)
        used_promocodes = user_data.get("promocodes_used", [])
        if code in used_promocodes:
            return {"success": False, "message": "❌ Вы уже использовали этот промокод"}
        
        reward_type = promocode.get("reward_type", "clicks")
        reward_value = promocode.get("reward_value", 0)
        
        if reward_type == "clicks":
            self.add_clicks(user_id, reward_value)
            reward_text = f"🎁 {reward_value:,} кликов"
        elif reward_type == "multiplier":
            self.set_multiplier(user_id, reward_value, duration_minutes=60)
            reward_text = f"⚡ Множитель x{reward_value} на 1 час"
        elif reward_type == "rank":
            user_data = self.get_user(user_id)
            user_data["rank"] = str(reward_value)
            self.update_user(user_id, user_data)
            reward_text = f"⭐ Ранг {RANKS.get(str(reward_value), 'User')}"
        elif reward_type == "nft":
            result = self.add_nft_to_user(user_id, reward_value)
            if result["success"]:
                reward_text = f"🎨 NFT: {result['nft_name']}"
            else:
                return {"success": False, "message": "❌ Ошибка при выдаче NFT"}
        else:
            return {"success": False, "message": "❌ Неизвестный тип награды"}
        
        promocode["uses_count"] = uses_count + 1
        self.promocodes[code] = promocode
        self.save_promocodes()
        
        used_promocodes.append(code)
        user_data["promocodes_used"] = used_promocodes
        self.update_user(user_id, user_data)
        
        user_str = str(user_id)
        if user_str not in self.used_promocodes:
            self.used_promocodes[user_str] = []
        
        self.used_promocodes[user_str].append({
            "code": code,
            "used_at": datetime.now().isoformat(),
            "reward_type": reward_type,
            "reward_value": reward_value
        })
        self.save_used_promocodes()
        
        return {"success": True, "message": f"✅ Промокод активирован!\n\n🎁 Награда: {reward_text}"}
    
    def get_all_promocodes(self) -> List[Dict]:
        return list(self.promocodes.values())
    
    # ========== NFT СИСТЕМА ==========
    
    def generate_nft_id(self) -> str:
        return f"NFT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"
    
    def create_nft(self, category: str, name: str = None) -> Dict:
        nft_id = self.generate_nft_id()
        category_info = NFT_CATEGORIES.get(category, NFT_CATEGORIES["common"])
        
        if not name:
            name = f"{category_info['name']} #{random.randint(1000, 9999)}"
        
        nft = {
            "id": nft_id,
            "category": category,
            "name": name,
            "emoji": category_info["emoji"],
            "price": category_info["price"],
            "created_at": datetime.now().isoformat(),
            "owner": None
        }
        return nft
    
    def add_nft_to_user(self, user_id: int, category: str) -> Dict:
        try:
            user_data = self.get_user(user_id)
            
            if "nft_collection" not in user_data:
                user_data["nft_collection"] = []
            
            if category not in NFT_CATEGORIES:
                category = "common"
            
            nft = self.create_nft(category)
            nft["owner"] = user_id
            
            if "nft_collection" not in self.nft_collection:
                self.nft_collection = {}
            
            self.nft_collection[nft["id"]] = nft
            user_data["nft_collection"].append(nft["id"])
            
            self.update_user(user_id, user_data)
            self.save_nft_collection()
            
            return {"success": True, "nft_id": nft["id"], "nft_name": nft["name"], "nft_category": category}
        except Exception as e:
            logger.error(f"Ошибка при добавлении NFT пользователю {user_id}: {e}")
            return {"success": False, "message": f"Ошибка: {str(e)}"}
    
    def get_user_nft_collection(self, user_id: int) -> List[Dict]:
        user_data = self.get_user(user_id)
        nft_ids = user_data.get("nft_collection", [])
        
        collection = []
        for nft_id in nft_ids:
            if nft_id in self.nft_collection:
                collection.append(self.nft_collection[nft_id])
        
        return collection
    
    def get_all_nft_categories(self) -> Dict:
        return NFT_CATEGORIES
    
    # ========== СТАТИСТИКА КАНАЛА ==========
    
    def update_channel_stats(self, promo_type: str, code: str):
        now = datetime.now().isoformat()
        
        if promo_type == "hourly":
            self.channel_stats["last_hourly_promo"] = now
            self.channel_stats["hourly_promo_count"] += 1
        elif promo_type == "daily":
            self.channel_stats["last_daily_promo"] = now
            self.channel_stats["daily_promo_count"] += 1
        elif promo_type == "weekly":
            self.channel_stats["last_weekly_promo"] = now
            self.channel_stats["weekly_promo_count"] += 1
        
        self.channel_stats["total_promos_sent"] += 1
        self.save_channel_stats()
    
    def should_send_hourly_promo(self) -> bool:
        last = self.channel_stats.get("last_hourly_promo")
        if not last:
            return True
        last_time = datetime.fromisoformat(last)
        return datetime.now() - last_time > timedelta(hours=1)
    
    def should_send_daily_promo(self) -> bool:
        last = self.channel_stats.get("last_daily_promo")
        if not last:
            return True
        last_time = datetime.fromisoformat(last)
        return datetime.now() - last_time > timedelta(days=1)
    
    def should_send_weekly_promo(self) -> bool:
        last = self.channel_stats.get("last_weekly_promo")
        if not last:
            return True
        last_time = datetime.fromisoformat(last)
        return datetime.now() - last_time > timedelta(days=7)

# Создаем экземпляр хранилища
user_storage = UserData()

# Словарь для хранения состояний
user_states = {}

# ========== ФУНКЦИИ ДЛЯ КАНАЛА ==========

async def check_and_send_channel_promos(application: Application):
    while True:
        try:
            await send_channel_promocodes(application)
        except Exception as e:
            logger.error(f"Ошибка в цикле отправки промокодов: {e}")
        await asyncio.sleep(3600)

async def send_channel_promocodes(context):
    try:
        bot = context.bot
        
        if user_storage.should_send_hourly_promo():
            code = user_storage.create_channel_promocode("clicks", 100, uses_limit=1000, expires_days=1)
            message = (
                "🎁 <b>ЕЖЕЧАСНЫЙ ПРОМОКОД!</b>\n\n"
                f"🔥 Ваш промокод на <b>100 кликов</b>!\n\n"
                f"<code>{code}</code>\n\n"
                "📋 Просто скопируйте и отправьте его боту!\n"
                "⏳ Промокод действует 24 часа!"
            )
            await bot.send_message(chat_id=CHANNEL_USERNAME, text=message, parse_mode='HTML')
            user_storage.update_channel_stats("hourly", code)
            logger.info(f"Отправлен часовой промокод {code} в канал")
        
        if user_storage.should_send_daily_promo():
            code = user_storage.create_channel_promocode("clicks", 2000, uses_limit=500, expires_days=2)
            message = (
                "🎉 <b>ЕЖЕДНЕВНЫЙ ПРОМОКОД!</b>\n\n"
                f"🔥 Сегодня выпал промокод на <b>2,000 кликов</b>!\n\n"
                f"<code>{code}</code>\n\n"
                "📋 Скопируйте и активируйте у бота!\n"
                "⏳ Промокод действует 48 часов!"
            )
            await bot.send_message(chat_id=CHANNEL_USERNAME, text=message, parse_mode='HTML')
            user_storage.update_channel_stats("daily", code)
            logger.info(f"Отправлен дневной промокод {code} в канал")
        
        if user_storage.should_send_weekly_promo():
            code = user_storage.create_channel_promocode("nft", "mythic", uses_limit=100, expires_days=7)
            message = (
                "🏆 <b>НЕДЕЛЬНЫЙ ПРОМОКОД!</b>\n\n"
                "🌌 Выпал <b>МИФИЧЕСКИЙ NFT</b>!\n\n"
                f"<code>{code}</code>\n\n"
                "⚡ Успейте активировать!\n"
                "⏳ Промокод действует 7 дней!\n"
                "🎨 Уникальный NFT с самой высокой редкостью!"
            )
            await bot.send_message(chat_id=CHANNEL_USERNAME, text=message, parse_mode='HTML')
            user_storage.update_channel_stats("weekly", code)
            logger.info(f"Отправлен недельный промокод {code} (NFT) в канал")
            
    except Exception as e:
        logger.error(f"Ошибка при отправке промокода в канал: {e}")

# ========== КОМАНДА /start ==========

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    session = user_storage.get_session(user.id)
    
    if session:
        username = session.get("username", "")
        account_info = user_storage.get_account_by_telegram_id(user.id)
        
        if account_info:
            user_data = user_storage.get_user(user.id)
            user_data["username"] = account_info.get("username", user.username or user.first_name)
            user_data["last_login"] = datetime.now().isoformat()
            user_storage.update_user(user.id, user_data)
            
            await show_main_menu(update, context, user.id, username)
            return
    
    await show_auth_menu(update, context)

async def show_auth_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    auth_text = (
        "🔐 <b>Добро пожаловать в кликер-бот!</b>\n\n"
        "Для начала игры необходимо войти в свой аккаунт.\n"
        "Если у вас ещё нет аккаунта - зарегистрируйтесь.\n\n"
        "📢 <b>Наш канал:</b> {}\n"
        "🎁 В канале каждый час выходят промокоды!\n\n"
        "<b>Формат входа:</b>\n"
        "Логин: @username\n"
        "Пароль: ваш пароль\n\n"
        "<b>Формат регистрации:</b>\n"
        "Логин: @username\n"
        "Пароль: ваш пароль"
    ).format(CHANNEL_USERNAME)
    
    keyboard = [
        [InlineKeyboardButton("🔐 Войти в аккаунт", callback_data="login")],
        [InlineKeyboardButton("📝 Зарегистрироваться", callback_data="register")],
        [InlineKeyboardButton("📢 Наш канал", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.message.edit_text(auth_text, reply_markup=reply_markup, parse_mode='HTML')
    else:
        await update.message.reply_text(auth_text, reply_markup=reply_markup, parse_mode='HTML')

async def handle_login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    user_states[user.id] = {"action": "login", "step": "username"}
    
    login_text = (
        "🔐 <b>Вход в аккаунт</b>\n\n"
        "Введите ваш логин в формате:\n"
        "<code>@username</code>\n\n"
        "Например: <code>@player123</code>"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="auth_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(login_text, reply_markup=reply_markup, parse_mode='HTML')

async def handle_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    user_states[user.id] = {"action": "register", "step": "username"}
    
    register_text = (
        "📝 <b>Регистрация нового аккаунта</b>\n\n"
        "Придумайте и введите логин в формате:\n"
        "<code>@username</code>\n\n"
        "Правила:\n"
        "• Логин должен начинаться с @\n"
        "• Можно использовать буквы, цифры и нижнее подчеркивание\n"
        "• Минимум 3 символа, максимум 20\n\n"
        "Например: <code>@player123</code>"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="auth_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(register_text, reply_markup=reply_markup, parse_mode='HTML')

# ========== ИСПРАВЛЕННЫЙ ОБРАБОТЧИК СООБЩЕНИЙ ==========

async def handle_friend_add_message(update: Update, context: ContextTypes.DEFAULT_TYPE, message_text: str):
    """Обработка ввода логина для добавления в друзья"""
    user = update.effective_user
    user_id = user.id
    
    if not message_text.startswith("@"):
        await update.message.reply_text("❌ Логин должен начинаться с @\nПопробуйте снова:")
        return
    
    friend_username = message_text[1:]
    
    account = user_storage.get_account_by_username(friend_username)
    if not account:
        await update.message.reply_text("❌ Пользователь не найден")
        if user_id in user_states:
            del user_states[user_id]
        return
    
    result = user_storage.add_friend(user_id, friend_username)
    await update.message.reply_text(result["message"])
    
    if result["success"] and account.get("telegram_id"):
        my_account = user_storage.get_account_by_telegram_id(user_id)
        my_username = my_account.get("username")
        
        try:
            await context.bot.send_message(
                chat_id=account["telegram_id"],
                text=(
                    f"📨 <b>Новая заявка в друзья!</b>\n\n"
                    f"👤 Пользователь @{my_username} хочет добавить вас в друзья!\n\n"
                    f"Перейдите в раздел 👥 Друзья → 📨 Входящие заявки"
                ),
                parse_mode='HTML'
            )
        except:
            pass
    
    if user_id in user_states:
        del user_states[user_id]
    
    keyboard = [[InlineKeyboardButton("👥 Друзья", callback_data="friends_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Вернуться в меню друзей:", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message_text = update.message.text.strip()
    
    if user.id in user_states:
        state = user_states[user.id]
        action = state.get("action")
        
        if action == "add_friend":
            await handle_friend_add_message(update, context, message_text)
            return
        
        await handle_auth_message(update, context, message_text)
        return
    
    if message_text.upper() in user_storage.promocodes:
        await use_promocode_command(update, context, message_text.upper())
        return
    
    await update.message.reply_text(
        "❓ Неизвестная команда.\n"
        "Используйте /start для входа в меню.\n"
        "Или введите промокод для активации!"
    )

async def handle_auth_message(update: Update, context: ContextTypes.DEFAULT_TYPE, message_text: str):
    user = update.effective_user
    state = user_states[user.id]
    action = state.get("action")
    step = state.get("step")
    
    if action == "login":
        if step == "username":
            if not message_text.startswith("@"):
                await update.message.reply_text("❌ Логин должен начинаться с @\nПопробуйте снова:")
                return
            
            username = message_text[1:]
            if not username.isalnum() and "_" not in username:
                await update.message.reply_text("❌ Логин может содержать только буквы, цифры и нижнее подчеркивание\nПопробуйте снова:")
                return
            
            state["username"] = username
            state["step"] = "password"
            await update.message.reply_text("🔐 Теперь введите ваш пароль:")
        
        elif step == "password":
            username = state.get("username", "")
            password = message_text
            
            if user_storage.authenticate(username, password):
                user_storage.create_session(user.id, username)
                
                user_data = user_storage.get_user(user.id)
                user_data["username"] = username
                user_data["last_login"] = datetime.now().isoformat()
                user_storage.update_user(user.id, user_data)
                
                if username in user_storage.accounts:
                    user_storage.accounts[username]["telegram_id"] = user.id
                    user_storage.accounts[username]["telegram_username"] = user.username or ""
                    user_storage.save_accounts()
                
                del user_states[user.id]
                
                await update.message.reply_text(f"✅ <b>Успешный вход!</b>\nДобро пожаловать, @{username}!", parse_mode='HTML')
                await show_main_menu(update, context, user.id, username)
            else:
                await update.message.reply_text("❌ Неверный логин или пароль.\nПопробуйте снова или зарегистрируйтесь.")
                del user_states[user.id]
                await show_auth_menu(update, context)
    
    elif action == "register":
        if step == "username":
            if not message_text.startswith("@"):
                await update.message.reply_text("❌ Логин должен начинаться с @\nПопробуйте снова:")
                return
            
            username = message_text[1:]
            
            if len(username) < 3:
                await update.message.reply_text("❌ Логин слишком короткий (минимум 3 символа)\nПопробуйте снова:")
                return
            if len(username) > 20:
                await update.message.reply_text("❌ Логин слишком длинный (максимум 20 символов)\nПопробуйте снова:")
                return
            
            allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
            if not all(char in allowed_chars for char in username):
                await update.message.reply_text("❌ Логин может содержать только буквы, цифры и нижнее подчеркивание\nПопробуйте снова:")
                return
            
            if username in user_storage.accounts:
                await update.message.reply_text("❌ Этот логин уже занят.\nПопробуйте другой:")
                return
            
            state["username"] = username
            state["step"] = "password"
            await update.message.reply_text("🔐 Отлично! Теперь придумайте пароль:\n\n• Минимум 6 символов")
        
        elif step == "password":
            username = state.get("username", "")
            password = message_text
            
            if len(password) < 6:
                await update.message.reply_text("❌ Пароль слишком короткий (минимум 6 символов)\nПопробуйте снова:")
                return
            
            if user_storage.create_account(username, password, user.id, user.username or ""):
                user_storage.create_session(user.id, username)
                
                user_data = user_storage.get_user(user.id)
                user_data["username"] = username
                user_data["registered_at"] = datetime.now().isoformat()
                user_data["last_login"] = datetime.now().isoformat()
                user_storage.update_user(user.id, user_data)
                
                del user_states[user.id]
                
                await update.message.reply_text(
                    f"🎉 <b>Аккаунт успешно создан!</b>\n\n"
                    f"👤 Логин: @{username}\n"
                    f"🔐 Пароль: {password}\n\n"
                    f"⚠️ <b>Сохраните ваш пароль!</b>\n\n"
                    f"Добро пожаловать в игру!",
                    parse_mode='HTML'
                )
                
                await show_main_menu(update, context, user.id, username)
            else:
                await update.message.reply_text("❌ Ошибка при создании аккаунта.\nПопробуйте снова.")
                del user_states[user.id]
                await show_auth_menu(update, context)

# ========== ГЛАВНОЕ МЕНЮ ==========

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, username: str):
    user_data = user_storage.get_user(user_id)
    multiplier = user_storage.get_multiplier(user_id)
    rank = user_data.get("rank", "user")
    formatted_username = user_storage.get_formatted_username(username)
    
    multiplier_text = f" (x{multiplier})" if multiplier > 1 else ""
    
    pending_requests = user_storage.get_pending_requests(user_id)
    pending_text = f" [{len(pending_requests)}]" if pending_requests else ""
    
    welcome_text = (
        f"👋 <b>Добро пожаловать, {formatted_username}!</b>\n\n"
        f"📊 Ваша статистика:\n"
        f"├ 🎯 Кликов: {user_data.get('clicks', 0):,}\n"
        f"├ 📈 Всего кликов: {user_data.get('total_clicks', user_data.get('clicks', 0)):,}\n"
        f"├ 🎁 Открыто кейсов: {user_data.get('cases_opened', 0)}\n"
        f"├ 🎨 NFT: {len(user_data.get('nft_collection', []))}\n"
        f"├ ⚔️ Дуэлей: {user_data.get('duels_won', 0)} побед / {user_data.get('duels_lost', 0)} поражений\n"
        f"└ ⚡ Множитель: x{multiplier}{multiplier_text}\n\n"
        f"Выберите действие:"
    )
    
    keyboard = [
        [InlineKeyboardButton(f"🎯 Кликать{multiplier_text}", callback_data="click_page")],
        [InlineKeyboardButton("📊 Профиль", callback_data="profile"),
         InlineKeyboardButton("🏆 Топ", callback_data="top")],
        [InlineKeyboardButton("🎁 Кейсы", callback_data="cases"),
         InlineKeyboardButton("🎨 NFT", callback_data="nft_menu")],
        [InlineKeyboardButton("👥 Друзья" + pending_text, callback_data="friends_menu"),
         InlineKeyboardButton("⚔️ Дуэли", callback_data="duels_menu")],
        [InlineKeyboardButton("⚙️ Аккаунт", callback_data="account_settings")]
    ]
    
    if user_id == ADMIN_ID or rank in ["admin", "admin+"]:
        keyboard.append([InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.message.edit_text(welcome_text, reply_markup=reply_markup, parse_mode='HTML')
    else:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='HTML')

# ========== СИСТЕМА ДРУЗЕЙ ==========

async def friends_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    friends = user_storage.get_friends(user_id)
    pending = user_storage.get_pending_requests(user_id)
    sent = user_storage.get_sent_requests(user_id)
    
    friends_text = (
        f"👥 <b>Мои друзья</b>\n\n"
        f"👤 Друзей: {len(friends)}\n"
        f"📨 Входящие заявки: {len(pending)}\n"
        f"📤 Исходящие заявки: {len(sent)}\n\n"
    )
    
    if friends:
        friends_text += "<b>Список друзей:</b>\n"
        for i, friend in enumerate(friends[:10], 1):
            formatted_friend = user_storage.get_formatted_username(friend)
            friends_text += f"{i}. {formatted_friend}\n"
        if len(friends) > 10:
            friends_text += f"... и ещё {len(friends) - 10}\n"
    else:
        friends_text += "У вас пока нет друзей. Добавьте друзей, чтобы сражаться в дуэлях!\n"
    
    keyboard = [
        [InlineKeyboardButton("➕ Добавить в друзья", callback_data="friend_add")],
        [InlineKeyboardButton("📨 Входящие заявки" + (f" ({len(pending)})" if pending else ""), callback_data="friend_pending")],
        [InlineKeyboardButton("📤 Исходящие заявки" + (f" ({len(sent)})" if sent else ""), callback_data="friend_sent")],
        [InlineKeyboardButton("❌ Удалить из друзей", callback_data="friend_remove")],
        [InlineKeyboardButton("🔙 В меню", callback_data="main_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(friends_text, reply_markup=reply_markup, parse_mode='HTML')

async def friend_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_states[user_id] = {"action": "add_friend", "step": "username"}
    
    add_text = (
        "➕ <b>Добавление в друзья</b>\n\n"
        "Введите логин пользователя в формате:\n"
        "<code>@username</code>\n\n"
        "Например: <code>@player123</code>"
    )
    
    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="friends_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(add_text, reply_markup=reply_markup, parse_mode='HTML')

async def friend_pending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    pending = user_storage.get_pending_requests(user_id)
    
    if not pending:
        pending_text = "📨 <b>Входящие заявки</b>\n\nУ вас нет входящих заявок в друзья."
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="friends_menu")]]
    else:
        pending_text = "📨 <b>Входящие заявки</b>\n\n"
        for i, friend in enumerate(pending, 1):
            formatted_friend = user_storage.get_formatted_username(friend)
            pending_text += f"{i}. {formatted_friend}\n"
        
        keyboard = []
        for friend in pending[:5]:
            keyboard.append([
                InlineKeyboardButton(f"✅ Принять @{friend}", callback_data=f"friend_accept_{friend}"),
                InlineKeyboardButton(f"❌ Отклонить @{friend}", callback_data=f"friend_decline_{friend}")
            ])
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="friends_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(pending_text, reply_markup=reply_markup, parse_mode='HTML')

async def friend_sent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    sent = user_storage.get_sent_requests(user_id)
    
    if not sent:
        sent_text = "📤 <b>Исходящие заявки</b>\n\nУ вас нет исходящих заявок в друзья."
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="friends_menu")]]
    else:
        sent_text = "📤 <b>Исходящие заявки</b>\n\n"
        for i, friend in enumerate(sent, 1):
            formatted_friend = user_storage.get_formatted_username(friend)
            sent_text += f"{i}. {formatted_friend}\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="friends_menu")]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(sent_text, reply_markup=reply_markup, parse_mode='HTML')

async def friend_accept(update: Update, context: ContextTypes.DEFAULT_TYPE, friend_username: str):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    result = user_storage.accept_friend(user_id, friend_username)
    
    await query.edit_message_text(result["message"], parse_mode='HTML')
    
    if result["success"]:
        friend_account = user_storage.get_account_by_username(friend_username)
        if friend_account and friend_account.get("telegram_id"):
            account = user_storage.get_account_by_telegram_id(user_id)
            my_username = account.get("username")
            
            try:
                await context.bot.send_message(
                    chat_id=friend_account["telegram_id"],
                    text=(
                        f"✅ <b>Заявка в друзья принята!</b>\n\n"
                        f"👤 Пользователь @{my_username} принял вашу заявку в друзья!\n\n"
                        f"Теперь вы можете сражаться в дуэлях!"
                    ),
                    parse_mode='HTML'
                )
            except:
                pass

async def friend_decline(update: Update, context: ContextTypes.DEFAULT_TYPE, friend_username: str):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    result = user_storage.decline_friend(user_id, friend_username)
    
    await query.edit_message_text(result["message"], parse_mode='HTML')

async def friend_remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    friends = user_storage.get_friends(user_id)
    
    if not friends:
        remove_text = "❌ <b>Удаление из друзей</b>\n\nУ вас нет друзей."
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="friends_menu")]]
    else:
        remove_text = "❌ <b>Удаление из друзей</b>\n\nВыберите друга для удаления:"
        
        keyboard = []
        for friend in friends[:10]:
            formatted_friend = user_storage.get_formatted_username(friend)
            keyboard.append([
                InlineKeyboardButton(f"❌ {formatted_friend}", callback_data=f"friend_remove_{friend}")
            ])
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="friends_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(remove_text, reply_markup=reply_markup, parse_mode='HTML')

async def friend_remove_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE, friend_username: str):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    result = user_storage.remove_friend(user_id, friend_username)
    
    await query.edit_message_text(result["message"], parse_mode='HTML')

# ========== СИСТЕМА ДУЭЛЕЙ ==========

async def duels_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_data = user_storage.get_user(user_id)
    active_duel = user_storage.get_active_duel(user_id)
    
    duels_text = (
        f"⚔️ <b>Дуэли</b>\n\n"
        f"📊 Ваша статистика:\n"
        f"├ 🏆 Побед: {user_data.get('duels_won', 0)}\n"
        f"├ 💔 Поражений: {user_data.get('duels_lost', 0)}\n"
        f"└ 🤝 Ничьих: {user_data.get('duels_draw', 0)}\n\n"
    )
    
    if active_duel:
        duels_text += f"⚠️ <b>У вас активная дуэль!</b>\n"
        duels_text += f"Противник: @{active_duel['opponent_username'] if active_duel['creator_id'] == user_id else active_duel['creator_username']}\n"
        duels_text += f"⏳ Осталось: {active_duel['duration']} сек\n\n"
    
    keyboard = [
        [InlineKeyboardButton("⚔️ Создать дуэль", callback_data="duel_create")],
        [InlineKeyboardButton("📋 Мои дуэли", callback_data="duel_history")],
        [InlineKeyboardButton("🏆 Топ дуэлянтов", callback_data="duel_top")],
        [InlineKeyboardButton("🔙 В меню", callback_data="main_menu")]
    ]
    
    if active_duel:
        keyboard.insert(0, [InlineKeyboardButton("⚔️ Перейти к дуэли", callback_data=f"duel_enter_{active_duel['id']}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(duels_text, reply_markup=reply_markup, parse_mode='HTML')

async def duel_create(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    friends = user_storage.get_friends(user_id)
    
    if not friends:
        create_text = (
            "⚔️ <b>Создание дуэли</b>\n\n"
            "❌ У вас нет друзей для дуэли!\n\n"
            "Сначала добавьте друзей в разделе 👥 Друзья."
        )
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="duels_menu")]]
    else:
        create_text = (
            "⚔️ <b>Создание дуэли</b>\n\n"
            "Выберите противника из списка друзей:"
        )
        
        keyboard = []
        for friend in friends[:10]:
            formatted_friend = user_storage.get_formatted_username(friend)
            keyboard.append([
                InlineKeyboardButton(f"👤 {formatted_friend}", callback_data=f"duel_opponent_{friend}")
            ])
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="duels_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(create_text, reply_markup=reply_markup, parse_mode='HTML')

async def duel_opponent(update: Update, context: ContextTypes.DEFAULT_TYPE, opponent_username: str):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    user_states[user_id] = {"action": "duel_create", "opponent": opponent_username}
    
    duel_text = (
        f"⚔️ <b>Создание дуэли</b>\n\n"
        f"👤 Противник: @{opponent_username}\n\n"
        f"Выберите длительность дуэли:"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("🕐 1 минута", callback_data="duel_duration_60"),
            InlineKeyboardButton("🕒 3 минуты", callback_data="duel_duration_180")
        ],
        [
            InlineKeyboardButton("🕔 5 минут", callback_data="duel_duration_300"),
            InlineKeyboardButton("🕙 10 минут", callback_data="duel_duration_600")
        ],
        [InlineKeyboardButton("🔙 Назад", callback_data="duel_create")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(duel_text, reply_markup=reply_markup, parse_mode='HTML')

async def duel_duration(update: Update, context: ContextTypes.DEFAULT_TYPE, duration: int):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    opponent = user_states[user_id].get("opponent")
    
    duel_text = (
        f"⚔️ <b>Создание дуэли</b>\n\n"
        f"👤 Противник: @{opponent}\n"
        f"⏳ Длительность: {duration // 60} минут\n\n"
        f"Выберите ставку в кликах:"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("💰 0", callback_data=f"duel_bet_{opponent}_{duration}_0"),
            InlineKeyboardButton("💰 100", callback_data=f"duel_bet_{opponent}_{duration}_100"),
            InlineKeyboardButton("💰 500", callback_data=f"duel_bet_{opponent}_{duration}_500")
        ],
        [
            InlineKeyboardButton("💰 1,000", callback_data=f"duel_bet_{opponent}_{duration}_1000"),
            InlineKeyboardButton("💰 5,000", callback_data=f"duel_bet_{opponent}_{duration}_5000"),
            InlineKeyboardButton("💰 10,000", callback_data=f"duel_bet_{opponent}_{duration}_10000")
        ],
        [InlineKeyboardButton("🔙 Назад", callback_data=f"duel_opponent_{opponent}")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(duel_text, reply_markup=reply_markup, parse_mode='HTML')

async def duel_create_final(update: Update, context: ContextTypes.DEFAULT_TYPE, 
                           opponent_username: str, duration: int, bet: int):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    result = user_storage.create_duel(user_id, opponent_username, duration, bet)
    
    if result["success"]:
        opponent_account = user_storage.get_account_by_username(opponent_username)
        account = user_storage.get_account_by_telegram_id(user_id)
        my_username = account.get("username")
        
        if opponent_account and opponent_account.get("telegram_id"):
            bet_text = f"{bet:,} кликов" if bet > 0 else "без ставки"
            duration_text = f"{duration // 60} минут"
            
            try:
                await context.bot.send_message(
                    chat_id=opponent_account["telegram_id"],
                    text=(
                        f"⚔️ <b>Вас вызвали на дуэль!</b>\n\n"
                        f"👤 Противник: @{my_username}\n"
                        f"⏳ Длительность: {duration_text}\n"
                        f"💰 Ставка: {bet_text}\n\n"
                        f"Перейдите в раздел ⚔️ Дуэли, чтобы принять или отклонить вызов!"
                    ),
                    parse_mode='HTML'
                )
            except:
                pass
        
        await query.edit_message_text(result["message"], parse_mode='HTML')
    else:
        await query.edit_message_text(result["message"], parse_mode='HTML')
    
    if user_id in user_states:
        del user_states[user_id]

async def duel_enter(update: Update, context: ContextTypes.DEFAULT_TYPE, duel_id: str):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    duel = user_storage.duels.get(duel_id)
    
    if not duel or duel["status"] != "active":
        await query.edit_message_text("❌ Эта дуэль уже завершена!", parse_mode='HTML')
        return
    
    if user_id == duel["creator_id"]:
        opponent = duel["opponent_username"]
        my_clicks = duel["creator_clicks"]
        opp_clicks = duel["opponent_clicks"]
    else:
        opponent = duel["creator_username"]
        my_clicks = duel["opponent_clicks"]
        opp_clicks = duel["creator_clicks"]
    
    start_time = datetime.fromisoformat(duel["started_at"])
    time_passed = (datetime.now() - start_time).seconds
    time_left = max(0, duel["duration"] - time_passed)
    
    duel_text = (
        f"⚔️ <b>АКТИВНАЯ ДУЭЛЬ!</b>\n\n"
        f"👤 Противник: @{opponent}\n"
        f"💰 Ставка: {duel['bet']:,} кликов\n"
        f"⏳ Осталось: {time_left} сек\n\n"
        f"📊 <b>Счет:</b>\n"
        f"├ Вы: {my_clicks} кликов\n"
        f"└ Противник: {opp_clicks} кликов\n\n"
        f"⚡ Нажимай кнопку, чтобы кликать!"
    )
    
    keyboard = [
        [InlineKeyboardButton("🎯 КЛИК!", callback_data=f"duel_click_{duel_id}")],
        [InlineKeyboardButton("🔙 В меню", callback_data="main_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(duel_text, reply_markup=reply_markup, parse_mode='HTML')

async def duel_click(update: Update, context: ContextTypes.DEFAULT_TYPE, duel_id: str):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    result = user_storage.add_duel_click(user_id, duel_id)
    
    if result["success"]:
        duel = user_storage.duels.get(duel_id)
        
        if duel["status"] == "finished":
            if duel["winner"] == "draw":
                winner_text = "🤝 Ничья!"
            else:
                winner_text = f"🏆 Победитель: @{duel['winner']}!"
            
            result_text = (
                f"⚔️ <b>ДУЭЛЬ ЗАВЕРШЕНА!</b>\n\n"
                f"{winner_text}\n\n"
                f"📊 <b>Итоговый счет:</b>\n"
                f"├ @{duel['creator_username']}: {duel['creator_clicks']} кликов\n"
                f"└ @{duel['opponent_username']}: {duel['opponent_clicks']} кликов\n\n"
                f"💰 Ставка: {duel['bet']:,} кликов"
            )
            
            keyboard = [[InlineKeyboardButton("🔙 В меню", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(result_text, reply_markup=reply_markup, parse_mode='HTML')
            
            try:
                await context.bot.send_message(chat_id=duel["creator_id"], text=result_text, parse_mode='HTML')
                await context.bot.send_message(chat_id=duel["opponent_id"], text=result_text, parse_mode='HTML')
            except:
                pass
        else:
            await duel_enter(update, context, duel_id)
    else:
        await query.answer(result["message"], show_alert=True)

async def duel_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    duels = user_storage.get_user_duels(user_id)
    
    duels.sort(key=lambda x: x.get("started_at", ""), reverse=True)
    
    if not duels:
        history_text = "📋 <b>История дуэлей</b>\n\nУ вас пока нет завершенных дуэлей."
    else:
        history_text = "📋 <b>История дуэлей</b>\n\n"
        
        for i, duel in enumerate(duels[:10], 1):
            if duel["status"] == "finished":
                if duel["winner"] == "declined":
                    result = "❌ Отклонена"
                elif duel["winner"] == "draw":
                    result = "🤝 Ничья"
                elif duel["winner"] == user_storage.get_account_by_telegram_id(user_id).get("username"):
                    result = "✅ Победа"
                else:
                    result = "💔 Поражение"
                
                opponent = duel["opponent_username"] if user_id == duel["creator_id"] else duel["creator_username"]
                
                try:
                    date = datetime.fromisoformat(duel["started_at"]).strftime("%d.%m.%Y")
                except:
                    date = "Неизвестно"
                
                history_text += (
                    f"{i}. {result} vs @{opponent}\n"
                    f"   📅 {date} | ⚔️ {duel['duration'] // 60} мин | 💰 {duel['bet']:,}\n"
                    f"   📊 {duel['creator_clicks']}:{duel['opponent_clicks']}\n\n"
                )
        
        if len(duels) > 10:
            history_text += f"... и ещё {len(duels) - 10} дуэлей"
    
    keyboard = [
        [InlineKeyboardButton("🏆 Топ дуэлянтов", callback_data="duel_top")],
        [InlineKeyboardButton("⚔️ Новая дуэль", callback_data="duel_create")],
        [InlineKeyboardButton("🔙 В меню", callback_data="duels_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(history_text, reply_markup=reply_markup, parse_mode='HTML')

async def duel_top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    top_duelists = user_storage.get_top_duelists(10)
    
    top_text = "🏆 <b>ТОП ДУЭЛЯНТОВ</b>\n\n"
    
    if not top_duelists:
        top_text += "Пока никто не участвовал в дуэлях... Будь первым! ⚔️"
    else:
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        
        for i, (user_id, username, wins, losses, draws, total) in enumerate(top_duelists[:10]):
            medal = medals[i] if i < len(medals) else f"{i+1}."
            formatted_username = user_storage.get_formatted_username(username)
            winrate = (wins / total * 100) if total > 0 else 0
            
            top_text += (
                f"{medal} {formatted_username}\n"
                f"   🏆 Побед: {wins} | 💔 Поражений: {losses} | 🤝 Ничьих: {draws}\n"
                f"   📊 Всего дуэлей: {total} | ⚡ Винрейт: {winrate:.1f}%\n\n"
            )
    
    keyboard = [
        [InlineKeyboardButton("⚔️ Дуэли", callback_data="duels_menu")],
        [InlineKeyboardButton("🔙 В меню", callback_data="main_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(top_text, reply_markup=reply_markup, parse_mode='HTML')

# ========== ПРОФИЛЬ ==========

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    session = user_storage.get_session(user.id)
    
    if not session:
        await update.message.reply_text("❌ Пожалуйста, сначала войдите в аккаунт.")
        await show_auth_menu(update, context)
        return
    
    await show_profile_page(update, user.id)

async def show_profile_page(update: Update, user_id: int):
    user_data = user_storage.get_user(user_id)
    account_info = user_storage.get_account_by_telegram_id(user_id)
    rank_info = RANKS.get(user_data.get("rank", "user"), RANKS["user"])
    multiplier = user_storage.get_multiplier(user_id)
    nft_collection = user_storage.get_user_nft_collection(user_id)
    friends = user_storage.get_friends(user_id)
    
    username = account_info.get("username", user_data.get("username", "Без имени"))
    formatted_username = user_storage.get_formatted_username(username)
    created_at = account_info.get("created_at", user_data.get("registered_at", ""))
    
    try:
        created_date = datetime.fromisoformat(created_at).strftime("%d.%m.%Y %H:%M")
    except:
        created_date = "Неизвестно"
    
    verified_status = "☑️ <b>Верифицирован</b>" if account_info.get("verified") else "❌ Не верифицирован"
    verified_by = f"\n   Верифицировал: {account_info.get('verified_by')}" if account_info.get("verified_by") else ""
    
    multiplier_text = f"\n⚡ Активный множитель: x{multiplier}" if multiplier > 1 else ""
    
    profile_text = (
        f"📊 <b>Профиль пользователя</b>\n"
        f"├ Логин: {formatted_username}\n"
        f"├ ID: {user_id}\n"
        f"├ Ранг: {rank_info}\n"
        f"├ Статус: {verified_status}{verified_by}\n"
        f"├ 📅 Регистрация: {created_date}\n"
        f"├ 🎯 Текущих кликов: {user_data.get('clicks', 0):,}\n"
        f"├ 📈 Всего кликов: {user_data.get('total_clicks', user_data.get('clicks', 0)):,}\n"
        f"├ 🎁 Открыто кейсов: {user_data.get('cases_opened', 0)}\n"
        f"├ 🎨 NFT: {len(nft_collection)}\n"
        f"├ 🎫 Промокодов: {len(user_data.get('promocodes_used', []))}\n"
        f"├ 👥 Друзья: {len(friends)}\n"
        f"├ ⚔️ Дуэли: {user_data.get('duels_won', 0)} побед / {user_data.get('duels_lost', 0)} поражений / {user_data.get('duels_draw', 0)} ничьих\n"
        f"└ ⚡ Множитель: x{multiplier}{multiplier_text}"
    )
    
    keyboard = [
        [InlineKeyboardButton("🎯 Кликать!", callback_data="click_page")],
        [InlineKeyboardButton("🏆 Топ игроков", callback_data="top")],
        [InlineKeyboardButton("🎁 Кейсы", callback_data="cases"),
         InlineKeyboardButton("🎨 NFT", callback_data="nft_menu")],
        [InlineKeyboardButton("👥 Друзья", callback_data="friends_menu"),
         InlineKeyboardButton("⚔️ Дуэли", callback_data="duels_menu")],
        [InlineKeyboardButton("⚙️ Аккаунт", callback_data="account_settings")],
        [InlineKeyboardButton("🔙 В меню", callback_data="main_menu")]
    ]
    
    if user_id == ADMIN_ID or user_data.get("rank") in ["admin", "admin+"]:
        keyboard.append([InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.message.edit_text(profile_text, reply_markup=reply_markup, parse_mode='HTML')
    else:
        await update.message.reply_text(profile_text, reply_markup=reply_markup, parse_mode='HTML')

# ========== ТОП ==========

async def top_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    session = user_storage.get_session(user.id)
    
    if not session:
        await update.message.reply_text("❌ Пожалуйста, сначала войдите в аккаунт.")
        await show_auth_menu(update, context)
        return
    
    await show_top(update, context)

async def show_top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top_users = user_storage.get_top_users(15)
    
    top_text = "🏆 <b>ТОП 15 ИГРОКОВ ПО КЛИКАМ</b>\n\n"
    
    if not top_users:
        top_text += "Пока никто не начал кликать... Будь первым! 🎯"
    else:
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        
        for i, (user_id, username, clicks, total_clicks, rank) in enumerate(top_users[:15]):
            medal = medals[i] if i < len(medals) else f"{i+1}."
            formatted_username = user_storage.get_formatted_username(username)
            
            top_text += f"{medal} {formatted_username} - {clicks:,} кликов\n"
    
    top_text += "\n🎯 Кликай больше, чтобы подняться в топе!"
    
    keyboard = [
        [InlineKeyboardButton("🎯 Кликать!", callback_data="click_page")],
        [InlineKeyboardButton("📊 Мой профиль", callback_data="profile")],
        [InlineKeyboardButton("🏆 Топ дуэлянтов", callback_data="duel_top")],
        [InlineKeyboardButton("🎁 Кейсы", callback_data="cases")],
        [InlineKeyboardButton("🔙 В меню", callback_data="main_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.message.edit_text(top_text, reply_markup=reply_markup, parse_mode='HTML')
    else:
        await update.message.reply_text(top_text, reply_markup=reply_markup, parse_mode='HTML')

# ========== НАСТРОЙКИ АККАУНТА ==========

async def account_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    account_info = user_storage.get_account_by_telegram_id(user_id)
    user_data = user_storage.get_user(user_id)
    
    if not account_info:
        await query.answer("❌ Аккаунт не найден", show_alert=True)
        await show_auth_menu(update, context)
        return
    
    username = account_info.get("username", "")
    formatted_username = user_storage.get_formatted_username(username)
    created_at = account_info.get("created_at", "")
    
    try:
        created_date = datetime.fromisoformat(created_at).strftime("%d.%m.%Y %H:%M")
    except:
        created_date = "Неизвестно"
    
    verified_status = "☑️ Верифицирован" if account_info.get("verified") else "❌ Не верифицирован"
    
    settings_text = (
        f"⚙️ <b>Настройки аккаунта</b>\n\n"
        f"👤 Логин: {formatted_username}\n"
        f"📅 Зарегистрирован: {created_date}\n"
        f"✅ Статус: {verified_status}\n"
        f"🎯 Кликов: {user_data.get('clicks', 0):,}\n"
        f"🎨 NFT: {len(user_data.get('nft_collection', []))}\n\n"
        f"Выберите действие:"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔐 Сменить пароль", callback_data="change_password")],
        [InlineKeyboardButton("🚪 Выйти", callback_data="logout")],
        [InlineKeyboardButton("🔙 В меню", callback_data="main_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(settings_text, reply_markup=reply_markup, parse_mode='HTML')

async def logout_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_storage.logout(user_id)
    
    await query.edit_message_text(
        "✅ Вы успешно вышли из аккаунта.\n\nДля входа снова нажмите /start",
        parse_mode='HTML'
    )

# ========== ПРОМОКОДЫ ==========

async def use_promocode_command(update: Update, context: ContextTypes.DEFAULT_TYPE, code: str = None):
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id
    else:
        user_id = update.effective_user.id
    
    session = user_storage.get_session(user_id)
    if not session:
        if update.callback_query:
            await update.callback_query.message.edit_text("❌ Пожалуйста, сначала войдите в аккаунт.")
            await show_auth_menu(update, context)
        else:
            await update.message.reply_text("❌ Пожалуйста, сначала войдите в аккаунт.")
            await show_auth_menu(update, context)
        return
    
    if not code:
        await update.message.reply_text(
            "❌ Пожалуйста, укажите промокод!\n"
            "Пример: PROMO123"
        )
        return
    
    result = user_storage.use_promocode(user_id, code.upper())
    
    if result["success"]:
        success_text = f"{result['message']}"
        keyboard = [
            [InlineKeyboardButton("📊 Профиль", callback_data="profile")],
            [InlineKeyboardButton("🔙 В меню", callback_data="main_menu")]
        ]
    else:
        success_text = result["message"]
        keyboard = [
            [InlineKeyboardButton("🔙 В меню", callback_data="main_menu")]
        ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.message.edit_text(success_text, reply_markup=reply_markup, parse_mode='HTML')
    else:
        await update.message.reply_text(success_text, reply_markup=reply_markup, parse_mode='HTML')

# ========== КЛИКЕР ==========

async def click_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_data = user_storage.get_user(user_id)
    multiplier = user_storage.get_multiplier(user_id)
    
    multiplier_text = f" (x{multiplier})" if multiplier > 1 else ""
    
    click_text = (
        f"🎯 <b>КЛИКЕР</b>\n\n"
        f"📊 Ваши клики: {user_data.get('clicks', 0):,}\n"
        f"⚡ Множитель: x{multiplier}\n"
        f"📈 Всего кликов: {user_data.get('total_clicks', user_data.get('clicks', 0)):,}\n\n"
        f"Нажимай кнопку ниже, чтобы получить клики{multiplier_text}!"
    )
    
    keyboard = [
        [InlineKeyboardButton(f"🎯 Кликнуть{multiplier_text}", callback_data="click_action")],
        [InlineKeyboardButton("📊 Профиль", callback_data="profile"),
         InlineKeyboardButton("🏆 Топ", callback_data="top")],
        [InlineKeyboardButton("🎁 Кейсы", callback_data="cases")],
        [InlineKeyboardButton("🔙 В меню", callback_data="main_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(click_text, reply_markup=reply_markup, parse_mode='HTML')

async def click_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_data = user_storage.get_user(user_id)
    old_clicks = user_data.get("clicks", 0)
    
    multiplier = user_storage.get_multiplier(user_id)
    added_clicks = 1 * multiplier
    
    new_clicks = old_clicks + added_clicks
    user_data["clicks"] = new_clicks
    user_data["total_clicks"] = user_data.get("total_clicks", old_clicks) + added_clicks
    
    await check_easter_egg(user_id, old_clicks, new_clicks, context)
    
    user_storage.update_user(user_id, user_data)
    
    multiplier_text = f" (x{multiplier})" if multiplier > 1 else ""
    
    click_text = (
        f"🎯 <b>КЛИКЕР</b>\n\n"
        f"✅ +{added_clicks} клик{'ов' if added_clicks > 1 else ''}{f' (x{multiplier})' if multiplier > 1 else ''}\n\n"
        f"📊 Ваши клики: {user_data.get('clicks', 0):,}\n"
        f"⚡ Множитель: x{multiplier}\n"
        f"📈 Всего кликов: {user_data.get('total_clicks', user_data.get('clicks', 0)):,}\n\n"
        f"Нажимай кнопку ниже, чтобы получить клики{multiplier_text}!"
    )
    
    keyboard = [
        [InlineKeyboardButton(f"🎯 Кликнуть{multiplier_text}", callback_data="click_action")],
        [InlineKeyboardButton("📊 Профиль", callback_data="profile"),
         InlineKeyboardButton("🏆 Топ", callback_data="top")],
        [InlineKeyboardButton("🎁 Кейсы", callback_data="cases")],
        [InlineKeyboardButton("🔙 В меню", callback_data="main_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(click_text, reply_markup=reply_markup, parse_mode='HTML')

async def check_easter_egg(user_id: int, old_clicks: int, new_clicks: int, context: ContextTypes.DEFAULT_TYPE):
    if old_clicks < 1488 <= new_clicks:
        try:
            user_data = user_storage.get_user(user_id)
            account_info = user_storage.get_account_by_telegram_id(user_id)
            username = account_info.get("username", user_data.get("username", "Игрок"))
            formatted_username = user_storage.get_formatted_username(username)
            
            message = (
                f"🎉 ААААА ПАСХАЛКО ПАСХАЛКО ПАСХАЛОЧКА АААА 🎉\n\n"
                f"🔥 {formatted_username} достиг {new_clicks:,} кликов!\n"
                f"🎯 Это магическое число 1488!\n"
                f"✨ Поздравляем с пасхалкой! 🥚"
            )
            
            await context.bot.send_message(
                chat_id=user_id,
                text=message,
                parse_mode='HTML'
            )
            
            user_data["clicks"] = user_data.get("clicks", 0) + 500
            user_storage.update_user(user_id, user_data)
            
            bonus_message = (
                f"🎁 <b>БОНУС ЗА ПАСХАЛКУ!</b>\n"
                f"Вы получили +500 кликов! 🎯\n"
                f"Теперь у вас: {user_data.get('clicks', 0):,} кликов!"
            )
            
            await context.bot.send_message(
                chat_id=user_id,
                text=bonus_message,
                parse_mode='HTML'
            )
            
        except Exception as e:
            logger.error(f"Ошибка при отправке пасхалки: {e}")

# ========== КЕЙСЫ ==========

async def cases_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    session = user_storage.get_session(user.id)
    
    if not session:
        await update.message.reply_text("❌ Пожалуйста, сначала войдите в аккаунт.")
        await show_auth_menu(update, context)
        return
    
    await show_cases(update, context)

async def show_cases(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id if update.effective_user else update.callback_query.from_user.id
    user_data = user_storage.get_user(user_id)
    
    cases_text = (
        f"🎁 <b>МАГАЗИН КЕЙСОВ</b>\n\n"
        f"📊 Ваши клики: {user_data.get('clicks', 0):,}\n\n"
        f"<b>Доступные кейсов:</b>\n"
        f"📦 <b>Обычный кейс</b> - 1,000 кликов\n"
        f"   Шансы: x2(50%) x3(30%) x4(20%)\n\n"
        f"🎁 <b>Редкий кейс</b> - 5,000 кликов\n"
        f"   Шансы: x5(40%) x6(35%) x7(25%)\n\n"
        f"💎 <b>Эпический кейс</b> - 10,000 кликов\n"
        f"   Шансы: x8(30%) x9(40%) x10(30%)\n\n"
        f"⚡ Множитель действует 10 минут!"
    )
    
    keyboard = [
        [InlineKeyboardButton("📦 Открыть Обычный (1,000)", callback_data="open_case_common")],
        [InlineKeyboardButton("🎁 Открыть Редкий (5,000)", callback_data="open_case_rare")],
        [InlineKeyboardButton("💎 Открыть Эпический (10,000)", callback_data="open_case_epic")],
        [InlineKeyboardButton("📊 Профиль", callback_data="profile"),
         InlineKeyboardButton("🏆 Топ", callback_data="top")],
        [InlineKeyboardButton("🔙 В меню", callback_data="main_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.callback_query:
        await update.callback_query.message.edit_text(cases_text, reply_markup=reply_markup, parse_mode='HTML')
    else:
        await update.message.reply_text(cases_text, reply_markup=reply_markup, parse_mode='HTML')

async def open_case(update: Update, context: ContextTypes.DEFAULT_TYPE, case_type: str):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_data = user_storage.get_user(user_id)
    
    case_info = CASE_MULTIPLIERS[case_type]
    case_cost = 1000 if case_type == "common" else 5000 if case_type == "rare" else 10000
    
    if user_data.get("clicks", 0) < case_cost:
        await query.answer(f"❌ Недостаточно кликов! Нужно {case_cost:,}", show_alert=True)
        return
    
    user_data["clicks"] = user_data.get("clicks", 0) - case_cost
    user_data["cases_opened"] = user_data.get("cases_opened", 0) + 1
    
    multiplier = random.choices(
        case_info["multipliers"], 
        weights=case_info["chances"], 
        k=1
    )[0]
    
    user_storage.set_multiplier(user_id, multiplier)
    user_storage.update_user(user_id, user_data)
    
    result_text = (
        f"🎉 <b>КЕЙС ОТКРЫТ!</b>\n\n"
        f"🎁 Тип кейса: {case_info['name']}\n"
        f"💰 Стоимость: {case_cost:,} кликов\n"
        f"⚡ Выпавший множитель: <b>x{multiplier}</b>\n"
        f"⏰ Действует: 10 минут\n\n"
        f"📊 Осталось кликов: {user_data.get('clicks', 0):,}\n"
        f"🎁 Всего открыто кейсов: {user_data.get('cases_opened', 0)}"
    )
    
    keyboard = [
        [InlineKeyboardButton("🎯 Кликать с множителем!", callback_data="click_page")],
        [InlineKeyboardButton("🎁 Ещё кейс", callback_data="cases")],
        [InlineKeyboardButton("📊 Профиль", callback_data="profile")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(result_text, reply_markup=reply_markup, parse_mode='HTML')

# ========== NFT МЕНЮ ==========

async def nft_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_data = user_storage.get_user(user_id)
    nft_collection = user_storage.get_user_nft_collection(user_id)
    
    nft_text = (
        f"🎨 <b>NFT КОЛЛЕКЦИЯ</b>\n\n"
        f"📊 Ваши NFT: {len(nft_collection)}\n"
        f"🎯 Ваши клики: {user_data.get('clicks', 0):,}\n\n"
    )
    
    if nft_collection:
        nft_text += "<b>Ваши NFT:</b>\n"
        for i, nft in enumerate(nft_collection[:5], 1):
            category_info = NFT_CATEGORIES.get(nft.get("category"), {})
            nft_text += f"{i}. {category_info.get('emoji', '🎨')} {category_info.get('name', 'NFT')} - <code>{nft.get('id', 'N/A')[:8]}...</code>\n"
        
        if len(nft_collection) > 5:
            nft_text += f"\n... и ещё {len(nft_collection) - 5} NFT"
    else:
        nft_text += "У вас пока нет NFT. Покупайте кейсы или активируйте промокоды из канала!"
    
    keyboard = [
        [InlineKeyboardButton("📦 Купить NFT кейс", callback_data="buy_nft_case")],
        [InlineKeyboardButton("📋 Мои NFT", callback_data="my_nft_collection")],
        [InlineKeyboardButton("🔙 В меню", callback_data="main_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(nft_text, reply_markup=reply_markup, parse_mode='HTML')

async def my_nft_collection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    nft_collection = user_storage.get_user_nft_collection(user_id)
    
    if not nft_collection:
        collection_text = "📋 <b>Мои NFT</b>\n\nУ вас пока нет NFT."
    else:
        collection_text = "📋 <b>Мои NFT</b>\n\n"
        
        for i, nft in enumerate(nft_collection, 1):
            category = nft.get("category", "common")
            category_info = NFT_CATEGORIES.get(category, {})
            nft_id = nft.get("id", "N/A")
            created_at = nft.get("created_at", "")
            
            try:
                created_date = datetime.fromisoformat(created_at).strftime("%d.%m.%Y")
            except:
                created_date = "Неизвестно"
            
            collection_text += (
                f"{i}. {category_info.get('emoji', '🎨')} <b>{category_info.get('name', 'NFT')}</b>\n"
                f"   🆔 <code>{nft_id}</code>\n"
                f"   📅 Получен: {created_date}\n\n"
            )
    
    keyboard = [
        [InlineKeyboardButton("🎨 NFT меню", callback_data="nft_menu")],
        [InlineKeyboardButton("🔙 В меню", callback_data="main_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(collection_text, reply_markup=reply_markup, parse_mode='HTML')

async def buy_nft_case(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_data = user_storage.get_user(user_id)
    
    nft_categories = NFT_CATEGORIES  # ИСПРАВЛЕНО: используем глобальную переменную
    
    buy_text = (
        f"📦 <b>Магазин NFT кейсов</b>\n\n"
        f"📊 Ваши клики: {user_data.get('clicks', 0):,}\n\n"
        f"<b>Доступные NFT кейсы:</b>\n"
    )
    
    for category, info in nft_categories.items():
        buy_text += f"• {info['emoji']} {info['name']} - {info['price']:,} кликов\n"
    
    keyboard = []
    
    for category, info in nft_categories.items():
        keyboard.append([
            InlineKeyboardButton(
                f"{info['emoji']} {info['name']} ({info['price']:,} кликов)",
                callback_data=f"buy_nft_{category}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="nft_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(buy_text, reply_markup=reply_markup, parse_mode='HTML')

async def buy_nft_case_action(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_data = user_storage.get_user(user_id)
    
    category_info = NFT_CATEGORIES.get(category)
    if not category_info:
        await query.answer("❌ Неверная категория NFT", show_alert=True)
        return
    
    price = category_info.get("price", 1000)
    
    if user_data.get("clicks", 0) < price:
        await query.answer(f"❌ Недостаточно кликов! Нужно {price:,}", show_alert=True)
        return
    
    user_data["clicks"] = user_data.get("clicks", 0) - price
    user_storage.update_user(user_id, user_data)
    
    result = user_storage.add_nft_to_user(user_id, category)
    
    if result["success"]:
        result_text = (
            f"🎉 <b>NFT успешно получен!</b>\n\n"
            f"🎨 Название: {result['nft_name']}\n"
            f"💎 Редкость: {category_info['name']}\n"
            f"🆔 ID: <code>{result['nft_id'][:8]}...</code>\n\n"
            f"📊 Осталось кликов: {user_data.get('clicks', 0):,}"
        )
    else:
        result_text = "❌ Ошибка при получении NFT"
    
    keyboard = [
        [InlineKeyboardButton("📋 Мои NFT", callback_data="my_nft_collection")],
        [InlineKeyboardButton("📦 Купить ещё", callback_data="buy_nft_case")],
        [InlineKeyboardButton("🔙 В меню", callback_data="main_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(result_text, reply_markup=reply_markup, parse_mode='HTML')

# ========== ИСПРАВЛЕННАЯ АДМИН ПАНЕЛЬ ==========

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Админ панель - ИСПРАВЛЕНО"""
    query = update.callback_query
    user_id = query.from_user.id
    
    user_data = user_storage.get_user(user_id)
    rank = user_data.get("rank", "user")
    
    if user_id != ADMIN_ID and rank not in ["admin", "admin+"]:
        await query.answer("❌ Доступ запрещен!", show_alert=True)
        return
    
    # ✅ ОЧИЩАЕМ СОСТОЯНИЕ АДМИНА
    if user_id in user_states:
        del user_states[user_id]
    
    await query.answer()
    
    admin_text = (
        f"👑 <b>Админ панель</b>\n"
        f"Ранг: {RANKS.get(rank, 'Администратор')}\n\n"
        f"Выберите раздел:"
    )
    
    keyboard = [
        [InlineKeyboardButton("👤 Управление пользователями", callback_data="admin_users")],
        [InlineKeyboardButton("✅ Верификация пользователей", callback_data="admin_verification")],
        [InlineKeyboardButton("🎁 Управление кликами", callback_data="admin_clicks")],
        [InlineKeyboardButton("⭐ Управление рангами", callback_data="admin_ranks")],
        [InlineKeyboardButton("🎫 Управление промокодами", callback_data="admin_promocodes")],
        [InlineKeyboardButton("🎨 Управление NFT", callback_data="admin_nft")],
        [InlineKeyboardButton("📊 Статистика системы", callback_data="admin_stats")],
        [InlineKeyboardButton("📢 Статистика канала", callback_data="admin_channel_stats")],
        [InlineKeyboardButton("🔙 В меню", callback_data="main_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

# ========== АДМИН: ВЕРИФИКАЦИЯ ==========

async def admin_verification(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if user_id in user_states:
        del user_states[user_id]
    
    user_data = user_storage.get_user(user_id)
    
    if user_id != ADMIN_ID and user_data.get("rank") != "admin+":
        await query.answer("❌ Только Admin+ может верифицировать!", show_alert=True)
        return
    
    admin_text = (
        "✅ <b>Верификация пользователей</b>\n\n"
        "Выберите действие:"
    )
    
    keyboard = [
        [InlineKeyboardButton("📋 Список неверифицированных", callback_data="admin_unverified_list")],
        [InlineKeyboardButton("✅ Верифицировать пользователя", callback_data="admin_verify_user")],
        [InlineKeyboardButton("❌ Снять верификацию", callback_data="admin_unverify_user")],
        [InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

# ========== АДМИН: КЛИКИ ==========

async def admin_clicks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    if user_id in user_states:
        del user_states[user_id]
    
    admin_text = (
        "🎁 <b>Управление кликами</b>\n\n"
        "Выберите действие:"
    )
    
    keyboard = [
        [InlineKeyboardButton("➕ Выдать клики", callback_data="admin_give_clicks")],
        [InlineKeyboardButton("➖ Забрать клики", callback_data="admin_remove_clicks")],
        [InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

# ========== АДМИН: РАНГИ ==========

async def admin_ranks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    if user_id in user_states:
        del user_states[user_id]
    
    admin_text = (
        "⭐ <b>Управление рангами</b>\n\n"
        "Выберите действие:"
    )
    
    keyboard = [
        [InlineKeyboardButton("👤 Изменить ранг пользователя", callback_data="admin_change_rank")],
        [InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

# ========== АДМИН: NFT ==========

async def admin_nft(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    if user_id in user_states:
        del user_states[user_id]
    
    admin_text = (
        "🎨 <b>Управление NFT</b>\n\n"
        "Выберите действие:"
    )
    
    keyboard = [
        [InlineKeyboardButton("🎁 Выдать NFT пользователю", callback_data="admin_give_nft")],
        [InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

# ========== АДМИН: ПРОМОКОДЫ ==========

async def admin_promocodes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    if user_id in user_states:
        del user_states[user_id]
    
    admin_text = (
        "🎫 <b>Управление промокодами</b>\n\n"
        "Выберите действие:"
    )
    
    keyboard = [
        [InlineKeyboardButton("➕ Создать промокод (клики)", callback_data="admin_create_promo_clicks")],
        [InlineKeyboardButton("🎨 Создать промокод (NFT)", callback_data="admin_create_promo_nft")],
        [InlineKeyboardButton("📋 Список всех промокодов", callback_data="admin_promocodes_list")],
        [InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

# ========== АДМИН: СТАТИСТИКА ==========

async def admin_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    if user_id in user_states:
        del user_states[user_id]
    
    all_accounts = user_storage.get_all_accounts()
    total_clicks = sum(account.get("clicks", 0) for account in all_accounts)
    total_nft = sum(len(user_storage.get_user(acc.get("telegram_id")).get("nft_collection", [])) for acc in all_accounts if acc.get("telegram_id"))
    verified_count = sum(1 for acc in all_accounts if acc.get("verified", False))
    
    rank_distribution = {}
    for account in all_accounts:
        telegram_id = account.get("telegram_id")
        if telegram_id:
            user_data = user_storage.get_user(telegram_id)
            rank = user_data.get("rank", "user")
            rank_distribution[rank] = rank_distribution.get(rank, 0) + 1
    
    stats_text = (
        f"📊 <b>Статистика системы</b>\n\n"
        f"👥 Всего аккаунтов: {len(all_accounts)}\n"
        f"✅ Верифицировано: {verified_count}\n"
        f"❌ Не верифицировано: {len(all_accounts) - verified_count}\n\n"
        f"🎯 Всего кликов: {total_clicks:,}\n"
        f"🎨 Всего NFT: {total_nft}\n\n"
        f"⭐ <b>Распределение по рангам:</b>\n"
    )
    
    for rank, count in rank_distribution.items():
        stats_text += f"{RANKS.get(rank, rank)}: {count} чел.\n"
    
    keyboard = [
        [InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")],
        [InlineKeyboardButton("🔙 В меню", callback_data="main_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(stats_text, reply_markup=reply_markup, parse_mode='HTML')

async def admin_channel_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    if user_id in user_states:
        del user_states[user_id]
    
    stats = user_storage.channel_stats
    
    last_hourly = "Никогда"
    if stats.get("last_hourly_promo"):
        try:
            last_hourly = datetime.fromisoformat(stats["last_hourly_promo"]).strftime("%d.%m.%Y %H:%M")
        except:
            last_hourly = stats["last_hourly_promo"]
    
    last_daily = "Никогда"
    if stats.get("last_daily_promo"):
        try:
            last_daily = datetime.fromisoformat(stats["last_daily_promo"]).strftime("%d.%m.%Y %H:%M")
        except:
            last_daily = stats["last_daily_promo"]
    
    last_weekly = "Никогда"
    if stats.get("last_weekly_promo"):
        try:
            last_weekly = datetime.fromisoformat(stats["last_weekly_promo"]).strftime("%d.%m.%Y %H:%M")
        except:
            last_weekly = stats["last_weekly_promo"]
    
    stats_text = (
        f"📢 <b>Статистика канала</b>\n\n"
        f"📊 Канал: {CHANNEL_USERNAME}\n\n"
        f"🕐 <b>Часовые промокоды (100 кликов):</b>\n"
        f"   Всего: {stats.get('hourly_promo_count', 0)}\n"
        f"   Последний: {last_hourly}\n\n"
        f"📆 <b>Дневные промокоды (2,000 кликов):</b>\n"
        f"   Всего: {stats.get('daily_promo_count', 0)}\n"
        f"   Последний: {last_daily}\n\n"
        f"🗓️ <b>Недельные промокоды (Мифический NFT):</b>\n"
        f"   Всего: {stats.get('weekly_promo_count', 0)}\n"
        f"   Последний: {last_weekly}\n\n"
        f"📨 Всего промокодов отправлено: {stats.get('total_promos_sent', 0)}"
    )
    
    keyboard = [
        [InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")],
        [InlineKeyboardButton("🔙 В меню", callback_data="main_menu")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(stats_text, reply_markup=reply_markup, parse_mode='HTML')

# ========== АДМИН: ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========

async def admin_unverified_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    all_accounts = user_storage.get_all_accounts()
    unverified = [acc for acc in all_accounts if not acc.get("verified", False)]
    
    if not unverified:
        admin_text = "✅ <b>Неверифицированные пользователи</b>\n\nВсе пользователи верифицированы!"
    else:
        admin_text = "✅ <b>Неверифицированные пользователи</b>\n\n"
        
        for i, account in enumerate(unverified[:20], 1):
            username = account.get("username", "N/A")
            clicks = account.get("clicks", 0)
            rank = account.get("rank", "user")
            
            admin_text += (
                f"{i}. @{username}\n"
                f"   🎯 Кликов: {clicks:,}\n"
                f"   ⭐ Ранг: {RANKS.get(rank, rank)}\n\n"
            )
        
        if len(unverified) > 20:
            admin_text += f"\n... и ещё {len(unverified) - 20} пользователей"
    
    keyboard = [[InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

async def admin_verify_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    all_accounts = user_storage.get_all_accounts()
    unverified = [acc for acc in all_accounts if not acc.get("verified", False)]
    
    if not unverified:
        await query.answer("✅ Все пользователи уже верифицированы!", show_alert=True)
        return
    
    admin_text = "✅ <b>Верификация пользователя</b>\n\nВыберите пользователя для верификации:"
    
    keyboard = []
    
    for account in unverified[:10]:
        username = account.get("username", "N/A")
        clicks = account.get("clicks", 0)
        
        keyboard.append([
            InlineKeyboardButton(
                f"👤 @{username} ({clicks:,} кликов)",
                callback_data=f"admin_do_verify_{username}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

async def admin_do_verify(update: Update, context: ContextTypes.DEFAULT_TYPE, username: str):
    query = update.callback_query
    await query.answer()
    
    admin_id = query.from_user.id
    admin_data = user_storage.get_user(admin_id)
    admin_username = admin_data.get("username", "Admin")
    
    account = user_storage.get_account_by_username(username)
    if not account:
        await query.answer("❌ Аккаунт не найден", show_alert=True)
        return
    
    if user_storage.verify_user(username, admin_username):
        formatted_username = user_storage.get_formatted_username(username)
        
        admin_text = (
            f"✅ <b>Пользователь верифицирован!</b>\n\n"
            f"👤 Пользователь: {formatted_username}\n"
            f"👑 Верифицировал: @{admin_username}\n"
            f"📅 Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
            f"Теперь у пользователя есть галочка ☑️ в профиле!"
        )
        
        try:
            if account.get("telegram_id"):
                await context.bot.send_message(
                    chat_id=account["telegram_id"],
                    text=(
                        f"✅ <b>Поздравляем!</b>\n\n"
                        f"Администратор @{admin_username} верифицировал ваш аккаунт!\n"
                        f"Теперь у вас есть галочка ☑️ в профиле!"
                    ),
                    parse_mode='HTML'
                )
        except:
            pass
    else:
        admin_text = "❌ Ошибка при верификации пользователя"
    
    keyboard = [[InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

async def admin_unverify_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    all_accounts = user_storage.get_all_accounts()
    verified = [acc for acc in all_accounts if acc.get("verified", False)]
    
    if not verified:
        await query.answer("❌ Нет верифицированных пользователей", show_alert=True)
        return
    
    admin_text = "❌ <b>Снятие верификации</b>\n\nВыберите пользователя:"
    
    keyboard = []
    
    for account in verified[:10]:
        username = account.get("username", "N/A")
        keyboard.append([
            InlineKeyboardButton(f"👤 @{username}", callback_data=f"admin_do_unverify_{username}")
        ])
    
    keyboard.append([InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

async def admin_do_unverify(update: Update, context: ContextTypes.DEFAULT_TYPE, username: str):
    query = update.callback_query
    await query.answer()
    
    account = user_storage.get_account_by_username(username)
    if not account:
        await query.answer("❌ Аккаунт не найден", show_alert=True)
        return
    
    if user_storage.unverify_user(username):
        admin_text = (
            f"❌ <b>Верификация снята!</b>\n\n"
            f"👤 Пользователь: @{username}\n"
            f"📅 Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        )
        
        try:
            if account.get("telegram_id"):
                await context.bot.send_message(
                    chat_id=account["telegram_id"],
                    text=(
                        f"❌ <b>Верификация снята</b>\n\n"
                        f"Администратор снял с вашего аккаунта верификацию."
                    ),
                    parse_mode='HTML'
                )
        except:
            pass
    else:
        admin_text = "❌ Ошибка при снятии верификации"
    
    keyboard = [[InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

# ========== АДМИН: УПРАВЛЕНИЕ КЛИКАМИ ==========

async def admin_give_clicks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    all_accounts = user_storage.get_all_accounts()
    
    admin_text = "➕ <b>Выдать клики пользователю</b>\n\nВыберите пользователя:"
    
    keyboard = []
    
    for account in all_accounts[:10]:
        username = account.get("username", "N/A")
        clicks = account.get("clicks", 0)
        formatted_username = user_storage.get_formatted_username(username)
        
        keyboard.append([
            InlineKeyboardButton(
                f"👤 {formatted_username} ({clicks:,} кликов)",
                callback_data=f"admin_give_to_{account.get('username')}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

async def admin_give_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE, username: str):
    query = update.callback_query
    await query.answer()
    
    account = user_storage.get_account_by_username(username)
    if not account:
        await query.answer("❌ Аккаунт не найден", show_alert=True)
        return
    
    telegram_id = account.get("telegram_id")
    user_data = user_storage.get_user(telegram_id) if telegram_id else {}
    formatted_username = user_storage.get_formatted_username(username)
    
    admin_text = (
        f"➕ <b>Выдача кликов пользователю</b>\n\n"
        f"👤 Пользователь: {formatted_username}\n"
        f"📊 Текущие клики: {user_data.get('clicks', 0):,}\n\n"
        f"Выберите количество кликов для выдачи:"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("➕ 100", callback_data=f"admin_give_{username}_100"),
            InlineKeyboardButton("➕ 500", callback_data=f"admin_give_{username}_500"),
            InlineKeyboardButton("➕ 1,000", callback_data=f"admin_give_{username}_1000")
        ],
        [
            InlineKeyboardButton("➕ 5,000", callback_data=f"admin_give_{username}_5000"),
            InlineKeyboardButton("➕ 10,000", callback_data=f"admin_give_{username}_10000"),
            InlineKeyboardButton("➕ 50,000", callback_data=f"admin_give_{username}_50000")
        ],
        [InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

async def admin_give_clicks_amount(update: Update, context: ContextTypes.DEFAULT_TYPE, username: str, amount: int):
    query = update.callback_query
    await query.answer()
    
    account = user_storage.get_account_by_username(username)
    if not account:
        await query.answer("❌ Аккаунт не найден", show_alert=True)
        return
    
    telegram_id = account.get("telegram_id")
    if not telegram_id:
        await query.answer("❌ У пользователя нет Telegram ID", show_alert=True)
        return
    
    user_storage.add_clicks(telegram_id, amount)
    user_data = user_storage.get_user(telegram_id)
    formatted_username = user_storage.get_formatted_username(username)
    
    admin_text = (
        f"✅ <b>Клики успешно выданы!</b>\n\n"
        f"👤 Пользователь: {formatted_username}\n"
        f"🎁 Выдано кликов: {amount:,}\n"
        f"📊 Теперь у пользователя: {user_data.get('clicks', 0):,} кликов"
    )
    
    keyboard = [
        [InlineKeyboardButton("➕ Выдать ещё", callback_data=f"admin_give_to_{username}")],
        [InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

async def admin_remove_clicks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    all_accounts = user_storage.get_all_accounts()
    
    admin_text = "➖ <b>Забрать клики у пользователя</b>\n\nВыберите пользователя:"
    
    keyboard = []
    
    for account in all_accounts[:10]:
        username = account.get("username", "N/A")
        clicks = account.get("clicks", 0)
        if clicks > 0:
            formatted_username = user_storage.get_formatted_username(username)
            
            keyboard.append([
                InlineKeyboardButton(
                    f"👤 {formatted_username} ({clicks:,} кликов)",
                    callback_data=f"admin_remove_from_{account.get('username')}"
                )
            ])
    
    keyboard.append([InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

async def admin_remove_from_user(update: Update, context: ContextTypes.DEFAULT_TYPE, username: str):
    query = update.callback_query
    await query.answer()
    
    account = user_storage.get_account_by_username(username)
    if not account:
        await query.answer("❌ Аккаунт не найден", show_alert=True)
        return
    
    telegram_id = account.get("telegram_id")
    user_data = user_storage.get_user(telegram_id) if telegram_id else {}
    current_clicks = user_data.get("clicks", 0)
    formatted_username = user_storage.get_formatted_username(username)
    
    if current_clicks == 0:
        await query.answer("❌ У пользователя нет кликов", show_alert=True)
        return
    
    admin_text = (
        f"➖ <b>Отнятие кликов у пользователя</b>\n\n"
        f"👤 Пользователь: {formatted_username}\n"
        f"📊 Текущие клики: {current_clicks:,}\n\n"
        f"Выберите количество кликов для отнятия:"
    )
    
    keyboard = []
    
    amounts = [100, 500, 1000, 5000, 10000]
    available_amounts = [amount for amount in amounts if amount <= current_clicks]
    
    if available_amounts:
        for i in range(0, len(available_amounts), 3):
            row = []
            for amount in available_amounts[i:i+3]:
                row.append(InlineKeyboardButton(f"➖ {amount:,}", callback_data=f"admin_remove_{username}_{amount}"))
            if row:
                keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("➖ Все клики", callback_data=f"admin_remove_all_{username}")])
    keyboard.append([InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

async def admin_remove_clicks_amount(update: Update, context: ContextTypes.DEFAULT_TYPE, username: str, amount: int):
    query = update.callback_query
    await query.answer()
    
    account = user_storage.get_account_by_username(username)
    if not account:
        await query.answer("❌ Аккаунт не найден", show_alert=True)
        return
    
    telegram_id = account.get("telegram_id")
    if not telegram_id:
        await query.answer("❌ У пользователя нет Telegram ID", show_alert=True)
        return
    
    user_storage.remove_clicks(telegram_id, amount)
    user_data = user_storage.get_user(telegram_id)
    formatted_username = user_storage.get_formatted_username(username)
    
    admin_text = (
        f"✅ <b>Клики успешно отняты!</b>\n\n"
        f"👤 Пользователь: {formatted_username}\n"
        f"➖ Отнято кликов: {amount:,}\n"
        f"📊 Теперь у пользователя: {user_data.get('clicks', 0):,} кликов"
    )
    
    keyboard = [
        [InlineKeyboardButton("➖ Забрать ещё", callback_data=f"admin_remove_from_{username}")],
        [InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

async def admin_remove_all_clicks(update: Update, context: ContextTypes.DEFAULT_TYPE, username: str):
    query = update.callback_query
    await query.answer()
    
    account = user_storage.get_account_by_username(username)
    if not account:
        await query.answer("❌ Аккаунт не найден", show_alert=True)
        return
    
    telegram_id = account.get("telegram_id")
    if not telegram_id:
        await query.answer("❌ У пользователя нет Telegram ID", show_alert=True)
        return
    
    user_data = user_storage.get_user(telegram_id)
    current_clicks = user_data.get("clicks", 0)
    formatted_username = user_storage.get_formatted_username(username)
    
    user_storage.remove_clicks(telegram_id, current_clicks)
    user_data = user_storage.get_user(telegram_id)
    
    admin_text = (
        f"✅ <b>Все клики отняты!</b>\n\n"
        f"👤 Пользователь: {formatted_username}\n"
        f"➖ Отнято кликов: {current_clicks:,}\n"
        f"📊 Теперь у пользователя: {user_data.get('clicks', 0):,} кликов"
    )
    
    keyboard = [
        [InlineKeyboardButton("➕ Выдать клики", callback_data=f"admin_give_to_{username}")],
        [InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

# ========== АДМИН: УПРАВЛЕНИЕ РАНГАМИ ==========

async def admin_change_rank(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    all_accounts = user_storage.get_all_accounts()
    
    admin_text = "👤 <b>Изменение ранга пользователя</b>\n\nВыберите пользователя:"
    
    keyboard = []
    
    for account in all_accounts[:10]:
        username = account.get("username", "N/A")
        rank = account.get("rank", "user")
        formatted_username = user_storage.get_formatted_username(username)
        
        keyboard.append([
            InlineKeyboardButton(
                f"👤 {formatted_username} ({RANKS.get(rank, rank)})",
                callback_data=f"admin_rank_user_{account.get('username')}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

async def admin_rank_user(update: Update, context: ContextTypes.DEFAULT_TYPE, username: str):
    query = update.callback_query
    await query.answer()
    
    account = user_storage.get_account_by_username(username)
    if not account:
        await query.answer("❌ Аккаунт не найден", show_alert=True)
        return
    
    telegram_id = account.get("telegram_id")
    user_data = user_storage.get_user(telegram_id) if telegram_id else {}
    current_rank = user_data.get("rank", "user")
    formatted_username = user_storage.get_formatted_username(username)
    
    admin_text = (
        f"⭐ <b>Изменение ранга пользователя</b>\n\n"
        f"👤 Пользователь: {formatted_username}\n"
        f"📊 Текущий ранг: {RANKS.get(current_rank, current_rank)}\n\n"
        f"Выберите новый ранг:"
    )
    
    keyboard = [
        [InlineKeyboardButton("👤 User", callback_data=f"admin_set_rank_{username}_user")],
        [InlineKeyboardButton("⭐ VIP", callback_data=f"admin_set_rank_{username}_vip")],
        [InlineKeyboardButton("✨ VIP+", callback_data=f"admin_set_rank_{username}_vip+")],
        [InlineKeyboardButton("🌟 VIP++", callback_data=f"admin_set_rank_{username}_vip++")],
        [InlineKeyboardButton("👑 Admin", callback_data=f"admin_set_rank_{username}_admin")],
        [InlineKeyboardButton("👑👑 Admin+", callback_data=f"admin_set_rank_{username}_admin+")],
        [InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

async def admin_set_rank(update: Update, context: ContextTypes.DEFAULT_TYPE, username: str, rank: str):
    query = update.callback_query
    await query.answer()
    
    account = user_storage.get_account_by_username(username)
    if not account:
        await query.answer("❌ Аккаунт не найден", show_alert=True)
        return
    
    telegram_id = account.get("telegram_id")
    if not telegram_id:
        await query.answer("❌ У пользователя нет Telegram ID", show_alert=True)
        return
    
    user_data = user_storage.get_user(telegram_id)
    old_rank = user_data.get("rank", "user")
    user_data["rank"] = rank
    user_storage.update_user(telegram_id, user_data)
    
    formatted_username = user_storage.get_formatted_username(username)
    
    admin_text = (
        f"✅ <b>Ранг успешно изменен!</b>\n\n"
        f"👤 Пользователь: {formatted_username}\n"
        f"📊 Было: {RANKS.get(old_rank, old_rank)}\n"
        f"📈 Стало: {RANKS.get(rank, rank)}"
    )
    
    keyboard = [[InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

# ========== АДМИН: УПРАВЛЕНИЕ NFT ==========

async def admin_give_nft(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    all_accounts = user_storage.get_all_accounts()
    
    admin_text = "🎨 <b>Выдать NFT пользователю</b>\n\nВыберите пользователя:"
    
    keyboard = []
    
    for account in all_accounts[:10]:
        username = account.get("username", "N/A")
        clicks = account.get("clicks", 0)
        formatted_username = user_storage.get_formatted_username(username)
        
        keyboard.append([
            InlineKeyboardButton(
                f"👤 {formatted_username} ({clicks:,} кликов)",
                callback_data=f"admin_give_nft_to_{account.get('username')}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

async def admin_give_nft_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE, username: str):
    query = update.callback_query
    await query.answer()
    
    account = user_storage.get_account_by_username(username)
    if not account:
        await query.answer("❌ Аккаунт не найден", show_alert=True)
        return
    
    telegram_id = account.get("telegram_id")
    user_data = user_storage.get_user(telegram_id) if telegram_id else {}
    formatted_username = user_storage.get_formatted_username(username)
    
    admin_text = (
        f"🎨 <b>Выдача NFT пользователю</b>\n\n"
        f"👤 Пользователь: {formatted_username}\n"
        f"📊 Текущие NFT: {len(user_data.get('nft_collection', []))}\n\n"
        f"Выберите категорию NFT:"
    )
    
    keyboard = []
    
    for category, info in NFT_CATEGORIES.items():
        keyboard.append([
            InlineKeyboardButton(
                f"{info['emoji']} {info['name']}",
                callback_data=f"admin_give_nft_{category}_{username}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

async def admin_give_nft_category(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str, username: str):
    query = update.callback_query
    await query.answer()
    
    account = user_storage.get_account_by_username(username)
    if not account:
        await query.answer("❌ Аккаунт не найден", show_alert=True)
        return
    
    telegram_id = account.get("telegram_id")
    if not telegram_id:
        await query.answer("❌ У пользователя нет Telegram ID", show_alert=True)
        return
    
    try:
        result = user_storage.add_nft_to_user(telegram_id, category)
        
        if result["success"]:
            user_data = user_storage.get_user(telegram_id)
            formatted_username = user_storage.get_formatted_username(username)
            category_info = NFT_CATEGORIES.get(category, {})
            
            admin_text = (
                f"✅ <b>NFT успешно выдан!</b>\n\n"
                f"👤 Пользователь: {formatted_username}\n"
                f"🎨 NFT: {result['nft_name']}\n"
                f"💎 Категория: {category_info.get('name', 'NFT')}\n\n"
                f"📊 Всего NFT у пользователя: {len(user_data.get('nft_collection', []))}"
            )
            
            keyboard = [[InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')
            
            try:
                await context.bot.send_message(
                    chat_id=telegram_id,
                    text=(
                        f"🎉 <b>Вам выдан NFT!</b>\n\n"
                        f"🎨 Название: {result['nft_name']}\n"
                        f"💎 Редкость: {category_info.get('name', 'NFT')}\n\n"
                        f"📋 Проверьте свою коллекцию в разделе NFT!"
                    ),
                    parse_mode='HTML'
                )
            except:
                pass
        else:
            await query.answer("❌ Ошибка при выдаче NFT", show_alert=True)
            
    except Exception as e:
        logger.error(f"Ошибка при выдаче NFT: {e}")
        await query.answer(f"❌ Произошла ошибка", show_alert=True)

# ========== АДМИН: УПРАВЛЕНИЕ ПРОМОКОДАМИ ==========

async def admin_create_promo_clicks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    admin_text = (
        "🎯 <b>Создание промокода (клики)</b>\n\n"
        "Выберите количество кликов:"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("🎯 100", callback_data="admin_promo_clicks_100"),
            InlineKeyboardButton("🎯 500", callback_data="admin_promo_clicks_500"),
            InlineKeyboardButton("🎯 1,000", callback_data="admin_promo_clicks_1000")
        ],
        [
            InlineKeyboardButton("🎯 5,000", callback_data="admin_promo_clicks_5000"),
            InlineKeyboardButton("🎯 10,000", callback_data="admin_promo_clicks_10000"),
            InlineKeyboardButton("🎯 50,000", callback_data="admin_promo_clicks_50000")
        ],
        [InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

async def admin_create_promo_nft(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    admin_text = (
        "🎨 <b>Создание промокода (NFT)</b>\n\n"
        "Выберите категорию NFT:"
    )
    
    keyboard = []
    
    for category, info in NFT_CATEGORIES.items():
        keyboard.append([
            InlineKeyboardButton(
                f"{info['emoji']} {info['name']}",
                callback_data=f"admin_promo_nft_{category}"
            )
        ])
    
    keyboard.append([InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

async def admin_create_promocode_final(update: Update, context: ContextTypes.DEFAULT_TYPE, 
                                      reward_type: str, reward_value: int):
    query = update.callback_query
    await query.answer()
    
    promocode = user_storage.generate_promocode(10)
    
    user_storage.create_promocode(
        code=promocode,
        reward_type=reward_type,
        reward_value=reward_value,
        uses_limit=100,
        expires_days=30
    )
    
    if reward_type == "clicks":
        reward_text = f"🎯 {reward_value:,} кликов"
    elif reward_type == "nft":
        category_info = NFT_CATEGORIES.get(str(reward_value), {})
        reward_text = f"🎨 {category_info.get('name', 'NFT')}"
    else:
        reward_text = f"Награда ({reward_type})"
    
    admin_text = (
        f"✅ <b>Промокод успешно создан!</b>\n\n"
        f"🎫 Промокод: <code>{promocode}</code>\n"
        f"🎁 Награда: {reward_text}\n"
        f"🔢 Использований: 100\n"
        f"⏰ Срок действия: 30 дней\n\n"
        f"📋 Просто введите этот код в любом чате с ботом!"
    )
    
    keyboard = [[InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

async def admin_promocodes_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    all_promocodes = user_storage.get_all_promocodes()
    
    if not all_promocodes:
        admin_text = "📋 <b>Список промокодов</b>\n\nНет созданных промокодов."
    else:
        admin_text = "📋 <b>Список всех промокодов</b>\n\n"
        
        for i, promo in enumerate(all_promocodes[:10], 1):
            code = promo.get("code", "N/A")
            reward_type = promo.get("reward_type", "clicks")
            reward_value = promo.get("reward_value", 0)
            uses_count = promo.get("uses_count", 0)
            uses_limit = promo.get("uses_limit", 1)
            expires_at = promo.get("expires_at", "")
            is_active = promo.get("is_active", True)
            channel_promo = promo.get("channel_promo", False)
            
            try:
                expires_date = datetime.fromisoformat(expires_at).strftime("%d.%m.%Y")
            except:
                expires_date = "Неизвестно"
            
            status = "✅" if is_active else "🚫"
            source = "📢" if channel_promo else "👑"
            
            if reward_type == "clicks":
                reward_text = f"{reward_value:,} кликов"
            elif reward_type == "nft":
                category_info = NFT_CATEGORIES.get(str(reward_value), {})
                reward_text = f"NFT ({category_info.get('name', 'Unknown')})"
            else:
                reward_text = f"Награда ({reward_type})"
            
            admin_text += (
                f"{i}. {source} {status} <code>{code}</code>\n"
                f"   🎁 {reward_text}\n"
                f"   🔢 {uses_count}/{uses_limit} использований\n"
                f"   ⏰ До: {expires_date}\n\n"
            )
        
        if len(all_promocodes) > 10:
            admin_text += f"\n... и ещё {len(all_promocodes) - 10} промокодов"
    
    keyboard = [[InlineKeyboardButton("👑 Админ панель", callback_data="admin_panel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(admin_text, reply_markup=reply_markup, parse_mode='HTML')

# ========== ОБРАБОТЧИК КНОПОК ==========

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на кнопки - ИСПРАВЛЕНО"""
    query = update.callback_query
    
    if not query:
        return
    
    await query.answer()
    
    user_id = query.from_user.id
    
    # Основные кнопки
    if query.data == "auth_menu":
        await show_auth_menu(update, context)
    
    elif query.data == "login":
        await handle_login(update, context)
    
    elif query.data == "register":
        await handle_register(update, context)
    
    elif query.data == "main_menu":
        session = user_storage.get_session(user_id)
        if session:
            username = session.get("username", "")
            await show_main_menu(update, context, user_id, username)
        else:
            await show_auth_menu(update, context)
    
    elif query.data == "click_page":
        session = user_storage.get_session(user_id)
        if session:
            await click_page(update, context)
        else:
            await show_auth_menu(update, context)
    
    elif query.data == "click_action":
        session = user_storage.get_session(user_id)
        if session:
            await click_action(update, context)
        else:
            await show_auth_menu(update, context)
    
    elif query.data == "profile":
        session = user_storage.get_session(user_id)
        if session:
            await show_profile_page(update, user_id)
        else:
            await show_auth_menu(update, context)
    
    elif query.data == "top":
        session = user_storage.get_session(user_id)
        if session:
            await show_top(update, context)
        else:
            await show_auth_menu(update, context)
    
    elif query.data == "cases":
        session = user_storage.get_session(user_id)
        if session:
            await show_cases(update, context)
        else:
            await show_auth_menu(update, context)
    
    elif query.data == "account_settings":
        session = user_storage.get_session(user_id)
        if session:
            await account_settings(update, context)
        else:
            await show_auth_menu(update, context)
    
    elif query.data == "nft_menu":
        session = user_storage.get_session(user_id)
        if session:
            await nft_menu(update, context)
        else:
            await show_auth_menu(update, context)
    
    elif query.data == "my_nft_collection":
        session = user_storage.get_session(user_id)
        if session:
            await my_nft_collection(update, context)
        else:
            await show_auth_menu(update, context)
    
    elif query.data == "buy_nft_case":
        session = user_storage.get_session(user_id)
        if session:
            await buy_nft_case(update, context)
        else:
            await show_auth_menu(update, context)
    
    elif query.data.startswith("buy_nft_"):
        session = user_storage.get_session(user_id)
        if session:
            category = query.data.replace("buy_nft_", "")
            await buy_nft_case_action(update, context, category)
        else:
            await show_auth_menu(update, context)
    
    elif query.data.startswith("open_case_"):
        session = user_storage.get_session(user_id)
        if session:
            case_type = query.data.replace("open_case_", "")
            await open_case(update, context, case_type)
        else:
            await show_auth_menu(update, context)
    
    elif query.data == "logout":
        session = user_storage.get_session(user_id)
        if session:
            await logout_user(update, context)
    
    # Кнопки друзей
    elif query.data == "friends_menu":
        session = user_storage.get_session(user_id)
        if session:
            await friends_menu(update, context)
        else:
            await show_auth_menu(update, context)
    
    elif query.data == "friend_add":
        session = user_storage.get_session(user_id)
        if session:
            await friend_add(update, context)
        else:
            await show_auth_menu(update, context)
    
    elif query.data == "friend_pending":
        session = user_storage.get_session(user_id)
        if session:
            await friend_pending(update, context)
        else:
            await show_auth_menu(update, context)
    
    elif query.data == "friend_sent":
        session = user_storage.get_session(user_id)
        if session:
            await friend_sent(update, context)
        else:
            await show_auth_menu(update, context)
    
    elif query.data == "friend_remove":
        session = user_storage.get_session(user_id)
        if session:
            await friend_remove(update, context)
        else:
            await show_auth_menu(update, context)
    
    elif query.data.startswith("friend_accept_"):
        session = user_storage.get_session(user_id)
        if session:
            friend_username = query.data.replace("friend_accept_", "")
            await friend_accept(update, context, friend_username)
        else:
            await show_auth_menu(update, context)
    
    elif query.data.startswith("friend_decline_"):
        session = user_storage.get_session(user_id)
        if session:
            friend_username = query.data.replace("friend_decline_", "")
            await friend_decline(update, context, friend_username)
        else:
            await show_auth_menu(update, context)
    
    elif query.data.startswith("friend_remove_"):
        session = user_storage.get_session(user_id)
        if session:
            friend_username = query.data.replace("friend_remove_", "")
            await friend_remove_confirm(update, context, friend_username)
        else:
            await show_auth_menu(update, context)
    
    # Кнопки дуэлей
    elif query.data == "duels_menu":
        session = user_storage.get_session(user_id)
        if session:
            await duels_menu(update, context)
        else:
            await show_auth_menu(update, context)
    
    elif query.data == "duel_create":
        session = user_storage.get_session(user_id)
        if session:
            await duel_create(update, context)
        else:
            await show_auth_menu(update, context)
    
    elif query.data == "duel_history":
        session = user_storage.get_session(user_id)
        if session:
            await duel_history(update, context)
        else:
            await show_auth_menu(update, context)
    
    elif query.data == "duel_top":
        session = user_storage.get_session(user_id)
        if session:
            await duel_top(update, context)
        else:
            await show_auth_menu(update, context)
    
    elif query.data.startswith("duel_opponent_"):
        session = user_storage.get_session(user_id)
        if session:
            opponent = query.data.replace("duel_opponent_", "")
            await duel_opponent(update, context, opponent)
        else:
            await show_auth_menu(update, context)
    
    elif query.data.startswith("duel_duration_"):
        session = user_storage.get_session(user_id)
        if session:
            duration = int(query.data.replace("duel_duration_", ""))
            await duel_duration(update, context, duration)
        else:
            await show_auth_menu(update, context)
    
    elif query.data.startswith("duel_bet_"):
        session = user_storage.get_session(user_id)
        if session:
            parts = query.data.split("_")
            if len(parts) == 5:
                opponent = parts[2]
                duration = int(parts[3])
                bet = int(parts[4])
                await duel_create_final(update, context, opponent, duration, bet)
        else:
            await show_auth_menu(update, context)
    
    elif query.data.startswith("duel_enter_"):
        session = user_storage.get_session(user_id)
        if session:
            duel_id = query.data.replace("duel_enter_", "")
            await duel_enter(update, context, duel_id)
        else:
            await show_auth_menu(update, context)
    
    elif query.data.startswith("duel_click_"):
        session = user_storage.get_session(user_id)
        if session:
            duel_id = query.data.replace("duel_click_", "")
            await duel_click(update, context, duel_id)
        else:
            await show_auth_menu(update, context)
    
    # ========== АДМИН КНОПКИ (ИСПРАВЛЕНО) ==========
    
    elif query.data.startswith("admin_"):
        user_data = user_storage.get_user(user_id)
        rank = user_data.get("rank", "user")
        
        if user_id == ADMIN_ID or rank in ["admin", "admin+"]:
            # ✅ ОЧИЩАЕМ СОСТОЯНИЕ АДМИНА
            if user_id in user_states:
                del user_states[user_id]
            
            # Главное меню админки
            if query.data == "admin_panel":
                await admin_panel(update, context)
            
            # Админ: Верификация
            elif query.data == "admin_verification":
                await admin_verification(update, context)
            elif query.data == "admin_unverified_list":
                await admin_unverified_list(update, context)
            elif query.data == "admin_verify_user":
                await admin_verify_user(update, context)
            elif query.data == "admin_unverify_user":
                await admin_unverify_user(update, context)
            elif query.data.startswith("admin_do_verify_"):
                username = query.data.replace("admin_do_verify_", "")
                await admin_do_verify(update, context, username)
            elif query.data.startswith("admin_do_unverify_"):
                username = query.data.replace("admin_do_unverify_", "")
                await admin_do_unverify(update, context, username)
            
            # Админ: Клики
            elif query.data == "admin_clicks":
                await admin_clicks(update, context)
            elif query.data == "admin_give_clicks":
                await admin_give_clicks(update, context)
            elif query.data.startswith("admin_give_to_"):
                username = query.data.replace("admin_give_to_", "")
                await admin_give_to_user(update, context, username)
            elif query.data.startswith("admin_give_"):
                parts = query.data.split("_")
                if len(parts) == 4:
                    username = parts[2]
                    amount = int(parts[3])
                    await admin_give_clicks_amount(update, context, username, amount)
            elif query.data == "admin_remove_clicks":
                await admin_remove_clicks(update, context)
            elif query.data.startswith("admin_remove_from_"):
                username = query.data.replace("admin_remove_from_", "")
                await admin_remove_from_user(update, context, username)
            elif query.data.startswith("admin_remove_"):
                parts = query.data.split("_")
                if len(parts) == 4:
                    username = parts[2]
                    amount = int(parts[3])
                    await admin_remove_clicks_amount(update, context, username, amount)
            elif query.data.startswith("admin_remove_all_"):
                username = query.data.replace("admin_remove_all_", "")
                await admin_remove_all_clicks(update, context, username)
            
            # Админ: Ранги
            elif query.data == "admin_ranks":
                await admin_ranks(update, context)
            elif query.data == "admin_change_rank":
                await admin_change_rank(update, context)
            elif query.data.startswith("admin_rank_user_"):
                username = query.data.replace("admin_rank_user_", "")
                await admin_rank_user(update, context, username)
            elif query.data.startswith("admin_set_rank_"):
                parts = query.data.split("_")
                if len(parts) == 5:
                    username = parts[3]
                    rank = parts[4]
                    await admin_set_rank(update, context, username, rank)
            
            # Админ: NFT
            elif query.data == "admin_nft":
                await admin_nft(update, context)
            elif query.data == "admin_give_nft":
                await admin_give_nft(update, context)
            elif query.data.startswith("admin_give_nft_to_"):
                username = query.data.replace("admin_give_nft_to_", "")
                await admin_give_nft_to_user(update, context, username)
            elif query.data.startswith("admin_give_nft_"):
                parts = query.data.split("_")
                if len(parts) == 5:
                    category = parts[3]
                    username = parts[4]
                    await admin_give_nft_category(update, context, category, username)
            
            # Админ: Промокоды
            elif query.data == "admin_promocodes":
                await admin_promocodes(update, context)
            elif query.data == "admin_create_promo_clicks":
                await admin_create_promo_clicks(update, context)
            elif query.data.startswith("admin_promo_clicks_"):
                parts = query.data.split("_")
                amount = parts[3]
                reward_value = int(amount)
                await admin_create_promocode_final(update, context, "clicks", reward_value)
            elif query.data == "admin_create_promo_nft":
                await admin_create_promo_nft(update, context)
            elif query.data.startswith("admin_promo_nft_"):
                category = query.data.replace("admin_promo_nft_", "")
                await admin_create_promocode_final(update, context, "nft", category)
            elif query.data == "admin_promocodes_list":
                await admin_promocodes_list(update, context)
            
            # Админ: Статистика
            elif query.data == "admin_stats":
                await admin_stats(update, context)
            elif query.data == "admin_channel_stats":
                await admin_channel_stats(update, context)
            
            else:
                await query.answer("⚙️ Функция в разработке", show_alert=True)
        else:
            await query.answer("❌ Доступ запрещен!", show_alert=True)
    
    elif query.data == "change_password":
        await query.answer("🔐 Функция смены пароля в разработке", show_alert=True)

# ========== КОМАНДА /help ==========

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🆘 <b>Помощь по кликер-боту</b>\n\n"
        "📌 <b>Основные команды:</b>\n"
        "/start - Начать работу с ботом\n"
        "/profile - Посмотреть свой профиль\n"
        "/top - Топ игроков по кликам\n"
        "/case - Открыть кейс за клики\n"
        "/help - Получить помощь\n\n"
        "🎮 <b>Как играть:</b>\n"
        "1. Зарегистрируйтесь или войдите в аккаунт\n"
        "2. Нажмите '🎯 Кликать!' для получения кликов\n"
        "3. Открывайте кейсы за клики для получения множителей\n"
        "4. Покупайте NFT кейсы для коллекционирования\n"
        "5. Получите галочку ☑️ от Admin+ за активность\n\n"
        "👥 <b>Друзья и Дуэли:</b>\n"
        "1. Добавляйте друзей в разделе 👥 Друзья\n"
        "2. Вызывайте друзей на дуэль ⚔️\n"
        "3. Выбирайте длительность: 1, 3, 5, 10 минут\n"
        "4. Делайте ставки кликами или играйте без ставки\n"
        "5. Кто больше накликает за время - тот победитель!\n\n"
        "📢 <b>Канал с промокодами:</b>\n"
        f"{CHANNEL_USERNAME}\n"
        "🕐 Каждый час - 100 кликов\n"
        "📆 Каждый день - 2,000 кликов\n"
        "🗓️ Каждую неделю - Мифический NFT\n\n"
        "✅ <b>Верификация:</b>\n"
        "• Администраторы с рангом Admin+ могут выдавать галочку ☑️\n"
        "• Верифицированные пользователи выделяются в топе\n"
        "• Галочка отображается в профиле и везде"
    )
    
    await update.message.reply_text(help_text, parse_mode='HTML')

# ========== ЗАПУСК БОТА ==========

async def post_init(application: Application):
    """Функция после инициализации бота"""
    asyncio.create_task(check_and_send_channel_promos(application))

def main():
    """Запуск бота"""
    try:
        application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
        
        # Обработчики команд
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("profile", profile))
        application.add_handler(CommandHandler("top", top_command))
        application.add_handler(CommandHandler("case", cases_command))
        application.add_handler(CommandHandler("help", help_command))
        
        # Обработчик текстовых сообщений
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Обработчик кнопок
        application.add_handler(CallbackQueryHandler(button_click))
        
        print("✅ Бот запущен! Ожидание сообщений...")
        print(f"👑 Админ ID: {ADMIN_ID}")
        print(f"🔑 Токен: {BOT_TOKEN[:10]}...")
        print(f"📢 Канал: {CHANNEL_USERNAME}")
        print(f"👥 Система друзей активирована!")
        print(f"⚔️ Система дуэлей активирована!")
        print(f"✅ Галочка изменена на ☑️")
        print(f"👑 Админ панель ИСПРАВЛЕНА!")
        print(f"➕ Добавление в друзья ИСПРАВЛЕНО!")
        print(f"🚀 Бот полностью готов к работе!")
        
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        print(f"❌ Критическая ошибка: {e}")

if __name__ == '__main__':
    main()
