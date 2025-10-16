from fastapi import FastAPI
from app.routers import users, posts, comments

app = FastAPI(title="Mini-Blog API")

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
