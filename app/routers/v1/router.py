from fastapi import APIRouter

from app.routers.v1 import lectures

router = APIRouter()
router.include_router(lectures.router)
