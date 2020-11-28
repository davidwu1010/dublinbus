from fastapi import APIRouter

from app.routers.deps import get_routes  


router = APIRouter()


routes_dict = get_routes()


@router.get(
    '/',
    tags=['routes'],
    summary='Return all routes',
    description='Return all the routes in routes.json'
)
async def read_routes():
    return routes_dict