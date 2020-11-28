from fastapi import APIRouter

from app.routers.apis import (
    routes, 
    stops, 
    predictions,
    user,
    )


router = APIRouter()
router.include_router(routes.router, prefix='/routes')
router.include_router(stops.router, prefix='/stops')
router.include_router(predictions.router, prefix='/predictions')
router.include_router(user.router, prefix='/saved')
