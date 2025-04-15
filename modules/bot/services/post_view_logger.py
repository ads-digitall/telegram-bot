import os
from datetime import datetime

LOG_FILE = "post_reads.log"

def log_post_view(user_id: int, post_id: int, action_type: str = "view") -> None:
    """
    Записывает информацию о прочтении поста пользователем в лог-файл.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] user_id={user_id} viewed post_id={post_id} ({action_type})\n"
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception as e:
        print(f"Ошибка при логировании просмотра поста: {e}")
