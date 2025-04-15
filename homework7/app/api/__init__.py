from fastapi import APIRouter
from .users.views import router as user_router
from .root import router as root_router

router = APIRouter(prefix="/api")


router.include_router(root_router)
router.include_router(user_router)
