from typing import Union, Optional

from nonebot import get_asgi, on_command
from nonebot.internal.matcher import Matcher
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from starlette.websockets import WebSocket, WebSocketDisconnect

from .bot import send
from .models import Info, Status, parse_event, make_message

app = get_asgi()
matcher = on_command("服务器状态", aliases={"状态"})


class ConnectionManager:
    """连接管理器"""

    def __init__(self):
        self.connection: Optional[WebSocket] = None

    async def connect(self, websocket: WebSocket) -> None:
        """与 WebSocket 客户端建立连接"""
        await websocket.accept()
        self.connection = websocket

    async def broadcast(self, data: Union[Info, dict]):
        """广播 Event"""
        if isinstance(data, Info):
            data = data.dict()
            connection = self.connection
            if connection:
                await connection.send_json(data)


manager = ConnectionManager()


@app.websocket("/mcdr")
async def mcdr(websocket: WebSocket):
    try:
        await manager.connect(websocket)
        while True:
            data = await websocket.receive_json()
            event = parse_event(**data)
            if event:
                message = make_message(event)
                if message:
                    resp = await send(message, event.group)
                    await websocket.send_json(resp.dict())
                else:
                    await websocket.send_json(
                        Status(status="invalid_message").json()
                    )
            else:
                await websocket.send_json(Status(status="invalid_type").json())
    except WebSocketDisconnect:
        manager.connection = None


@matcher.handle()
async def send_status(matcher: Matcher, event: GroupMessageEvent):
    connection = manager.connection
    if not connection:
        await matcher.finish("当前未连接服务器，无法获取信息，请稍后再试", at_sender=True)
    await connection.send_json(
        {"type": "get_server_info", "group": event.group_id}
    )
