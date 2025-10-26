from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware

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
    response.set_cookie(key="user_id", value="123", httponly=True)
    return {"msg": "Logged in"}

@app.get("/profile")
def profile(request: Request):
    user_id = request.cookies.get("user_id")
    return {"user_id": user_id}


def main():
    import uvicorn
    print("Starting FastAPI backend server...")
    uvicorn.run(
        "backend.app:app",
        host="127.0.0.1",
        reload=True,#支持热重载
        port=8000,
        log_level="info"
    )


if __name__ == "__main__":
    main()