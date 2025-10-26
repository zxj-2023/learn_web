from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import uuid

# 简化的内存session存储
sessions = {}

app = FastAPI()

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有前端地址
    allow_credentials=True, # 允许携带 Cookie
    allow_methods=["*"],# 允许所有 HTTP 方法
    allow_headers=["*"],# 允许所有 HTTP 头
)

@app.post("/login")
def login(response: Response):
    # 创建新的session
    session_id = str(uuid.uuid4())
    session_data = {"user_id": "123", "username": "admin"}
    
    # 将session数据存储到内存字典
    sessions[session_id] = session_data
    
    # 设置session cookie
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True
    )
    
    logger.info(f"用户登录成功，session_id: {session_id}")
    return {"msg": "Logged in", "session_id": session_id}

@app.get("/profile")
def profile(request: Request):
    # 从cookie中获取session_id
    session_id = request.cookies.get("session_id")
    
    if session_id is None:
        logger.warning("未找到session cookie")
        return {"error": "请先登录", "user_id": None}
    
    # 从内存字典获取session数据
    session_data = sessions.get(session_id)
    
    if session_data is None:
        logger.error(f"Session不存在: {session_id}")
        return {"error": "Session已过期", "user_id": None}
    
    logger.info(f"获取session数据成功: {session_data}")
    return {"user_id": session_data.get("user_id"), "username": session_data.get("username")}


def main():
    import uvicorn
    print("Starting FastAPI backend server...")
    uvicorn.run(
        "backend.session:app",
        host="127.0.0.1",
        reload=True,
        port=8000,
        log_level="info"
    )


if __name__ == "__main__":
    main()