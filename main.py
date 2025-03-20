from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
import matplotlib.pyplot as plt
import io

app = FastAPI()

# 配置模板
templates = Jinja2Templates(directory="templates")
fake_items_db = [{"item_name": "Item-1"}, {"item_name": "Item-2"}, {"item_name": "Item-3"},{"item_name": "Item-4"}]


@app.get("/items")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

@app.get("/users/{user_id}")
async def root(user_id):
    return {"message": f"Hi user {user_id}"}

@app.get("/users/{user_id}", response_class=HTMLResponse)
async def home(request: Request):
    # 渲染主页
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/plot")
async def get_plot():
    # 动态生成 Matplotlib 图形
    plt.figure(figsize=(6, 4))
    x = [i for i in range(10)]
    y = [i ** 2 for i in x]
    plt.plot(x, y, marker='o', label="y = x^2")
    plt.title("Sample Matplotlib Graph")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.legend()
    plt.grid(True)

    # 将图形保存到内存中
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    # 返回图形作为响应
    return StreamingResponse(buf, media_type="image/png")
