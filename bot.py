import nonebot
from nonebot.log import logger, default_format
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter

logger.add(
    "logs/{time:YYYY-MM-DD}/error.log",
    rotation="00:00",
    diagnose=False,
    level="ERROR",
    format=default_format,
)
logger.add(
    "logs/{time:YYYY-MM-DD}/info.log",
    rotation="00:00",
    diagnose=False,
    level="INFO",
    format=default_format,
)

nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)
nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.run(app="__mp_main__:app")
