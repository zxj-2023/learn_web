from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt

# JWT配置
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# 简单的用户数据
users = {
    "admin": {"user_id": "123", "username": "admin", "password": "admin123"}
}

app = FastAPI()

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_token(username: str) -> str:
    """创建JWT token"""
    # 设置token过期时间为24小时
    expire = datetime.utcnow() + timedelta(hours=24)
    # 构建JWT载荷，包含用户名和过期时间
    payload = {
        "sub": username,  # subject: 用户名
        "exp": expire     # expiration: 过期时间
    }
    # 使用密钥和算法对载荷进行编码生成token
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> str:
    """验证JWT token"""
    # 解码JWT token获取载荷信息
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    # 从载荷中提取用户名
    username = payload.get("sub")
    return username

@app.post("/login")
def login(response: Response):
    """用户登录"""
    # 简化登录，直接使用默认用户
    username = "admin"
    # 从用户字典中获取用户信息
    user = users.get(username)
    
    # 为用户创建JWT token
    token = create_token(username)
    # 将token设置为httponly cookie，与现有前端兼容
    response.set_cookie(key="session_id", value=token, httponly=True)
    # 返回token信息和登录成功消息
    return {"access_token": token, "token_type": "bearer", "msg": "Logged in"}

@app.get("/profile")
def profile(request: Request):
    """获取用户信息"""
    # 首先尝试从cookie获取token（兼容现有前端）
    token = request.cookies.get("session_id")
    
    # 如果cookie中没有token，尝试从Authorization header获取
    if not token:
        auth_header = request.headers.get("authorization")
        # 检查是否为Bearer token格式
        if auth_header and auth_header.startswith("Bearer "):
            # 提取Bearer后面的token部分
            token = auth_header.split(" ")[1]
    
    # 验证token并获取用户名
    username = verify_token(token)
    # 根据用户名获取用户信息
    user = users.get(username)
    # 返回用户ID和用户名
    return {"user_id": user["user_id"], "username": user["username"]}

def main():
    import uvicorn
    print("Starting JWT FastAPI backend server...")
    uvicorn.run(
        "backend.JWT:app",
        host="127.0.0.1",
        reload=True,
        port=8000,
        log_level="info"
    )

if __name__ == "__main__":
    main()