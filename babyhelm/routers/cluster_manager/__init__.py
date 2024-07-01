from fastapi import APIRouter

from babyhelm.routers.cluster_manager.applications import router as applications_router
from babyhelm.routers.cluster_manager.projects import router as projects_router

router = APIRouter(prefix="/cluster")
router.include_router(applications_router)
router.include_router(projects_router)
