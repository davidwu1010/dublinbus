from pydantic import BaseModel


class UserRoutePostItem(BaseModel):
    # { route_id: “39”, origin: “783”, dest: “786” }
    route_id: str
    origin: str
    dest: str