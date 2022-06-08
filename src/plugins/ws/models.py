# sourcery skip: avoid-builtin-shadow
from typing import List, Optional

from pydantic import BaseModel
from nonebot.adapters.onebot.v11 import Message

STATUS_TEMPLATE = """服务器名称：{server_name}
在线：{is_online}
版本：{version}
在线人数：{now_player}/{max_player}
在线玩家：{player_list}
假人：{fake_player_list}"""


class Status(BaseModel):
    status: str
    message: Optional[str] = None


class Info(BaseModel):
    type: str
    group: int


class ServerInfo(Info):
    type: str = "server_info"
    name: str
    is_online: bool
    version: str
    now_player: int
    max_player: int
    player_list: List[str]


class Request(BaseModel):
    type: str


class GetServerInfo(Request):
    type: str = "get_server_info"


def make_message(event: Info) -> Optional[Message]:
    if isinstance(event, ServerInfo):
        return Message(
            STATUS_TEMPLATE.format(
                server_name=event.name,
                is_online="是" if event.is_online else "否",
                version=event.version,
                now_player=event.now_player,
                max_player=event.max_player,
                player_list="，".join(
                    filter(
                        lambda x: not x.startswith("bot_"), event.player_list
                    )
                ) or "无",
                fake_player_list="，".join(
                    filter(lambda x: x.startswith("bot_"), event.player_list)
                ) or "无",
            )
        )


def parse_event(**kwargs) -> Optional[Info]:
    if kwargs["type"] == "server_info":
        return ServerInfo.parse_obj(kwargs)
