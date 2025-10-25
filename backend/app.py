from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],  # 允许的前端地址
    allow_credentials=True,                   # 允许携带 Cookie
    allow_methods=["*"],
    allow_headers=["*"],
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
        reload=True,
        port=8000,
        log_level="info"
    )


if __name__ == "__main__":
    main()