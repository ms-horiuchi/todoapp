from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from routers.item import router as item_router
from routers.user import router as user_router
from fastapi.middleware.cors import CORSMiddleware
from utils.exceptions import TodoAppException

app = FastAPI()

app.include_router(
    item_router
    )
app.include_router(
    user_router
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(TodoAppException)
async def todo_exception_handler(request, exc: TodoAppException):
    """
    カスタム例外のハンドラー
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.message}
    )