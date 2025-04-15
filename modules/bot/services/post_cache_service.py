import os
import json
import time

CACHE_DIR = "post_cache"
CACHE_DURATION_SECONDS = 60 * 60  # 60 минут

os.makedirs(CACHE_DIR, exist_ok=True)

def _get_cache_path(user_id: int) -> str:
    return os.path.join(CACHE_DIR, f"user_{user_id}.json")

def load_cache(user_id: int) -> dict:
    path = _get_cache_path(user_id)
    if not os.path.exists(path):
        return {"viewed": {}, "reactions": {}}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"viewed": {}, "reactions": {}}

def save_cache(user_id: int, cache: dict) -> None:
    path = _get_cache_path(user_id)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cache, f)
    except Exception as e:
        print(f"[post_cache] Ошибка при сохранении: {e}")

def get_cached_post_ids(user_id: int) -> list[int]:
    cache = load_cache(user_id)
    now = time.time()
    recent = {
        int(post_id): ts
        for post_id, ts in cache.get("viewed", {}).items()
        if now - ts <= CACHE_DURATION_SECONDS
    }
    return list(recent.keys())

def add_posts_to_cache(user_id: int, post_ids: list[int]) -> None:
    cache = load_cache(user_id)
    now = time.time()
    viewed = cache.get("viewed", {})
    for post_id in post_ids:
        viewed[str(post_id)] = now
    cache["viewed"] = viewed
    save_cache(user_id, cache)

def has_recent_reaction(user_id: int, post_id: int) -> bool:
    cache = load_cache(user_id)
    ts = cache.get("reactions", {}).get(str(post_id))
    return ts and (time.time() - ts <= CACHE_DURATION_SECONDS)

def add_recent_reaction(user_id: int, post_id: int) -> None:
    cache = load_cache(user_id)
    reactions = cache.get("reactions", {})
    reactions[str(post_id)] = int(time.time())
    cache["reactions"] = reactions
    save_cache(user_id, cache)

def clean_cache():
    now = time.time()
    for filename in os.listdir(CACHE_DIR):
        path = os.path.join(CACHE_DIR, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            viewed = {
                pid: ts for pid, ts in data.get("viewed", {}).items()
                if now - ts <= CACHE_DURATION_SECONDS
            }
            reactions = {
                pid: ts for pid, ts in data.get("reactions", {}).items()
                if now - ts <= CACHE_DURATION_SECONDS
            }

            if not viewed and not reactions:
                os.remove(path)
            else:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump({"viewed": viewed, "reactions": reactions}, f)

        except Exception as e:
            print(f"[post_cache] Ошибка при очистке файла {filename}: {e}")

# ✅ Добавлено
def update_activity(user_id: int) -> None:
    """
    Обновляет активность пользователя, сохраняя timestamp в 'last_seen'.
    """
    cache = load_cache(user_id)
    cache["last_seen"] = int(time.time())
    save_cache(user_id, cache)

# ✅ Новые функции кеша подписки
def get_last_subscription_refresh(user_id: int) -> int | None:
    cache = load_cache(user_id)
    return cache.get("last_refresh")

def set_last_subscription_refresh(user_id: int) -> None:
    cache = load_cache(user_id)
    cache["last_refresh"] = int(time.time())
    save_cache(user_id, cache)
