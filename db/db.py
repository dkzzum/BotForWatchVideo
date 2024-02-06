from aiogram.types import Message
from collections import deque

db: dict[int, dict[str, str | int | bool | list | dict[str, str]]] = {}
deque_for_admins: deque[list[str | bool]] = deque()
approved_video: list[str] = []
