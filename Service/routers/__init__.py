from fastapi import FastAPI

from . import eeg, ppg

base_api_route = "/mental-connect/algorithm/api"


def register_routes(app: FastAPI):
    """
    init all routers
    """
    # eeg router
    app.include_router(eeg.router, prefix=base_api_route)
    app.include_router(ppg.router, prefix=base_api_route)