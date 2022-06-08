from nonebot import get_bot
from nonebot.adapters.onebot.v11 import Message, ActionFailed

from .models import Status


async def send(message: Message, group: int) -> Status:
    try:
        bot = get_bot()
    except ValueError as e:
        return Status(status="null_bot", message=str(e))

    try:
        await bot.send_group_msg(group_id=group, message=message)
    except ActionFailed as e:
        return Status(status="action_failed", message=e.info["wording"])
    return Status(status="ok")
