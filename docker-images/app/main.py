import sys

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

version = f"{sys.version_info.major}.{sys.version_info.minor}"


async def homepage(request):
    message = f"Hello world! From Starlette running on Uvicorn with Gunicorn. Using Python {version}"
    return JSONResponse({"message": message})


app = Starlette(routes=[Route("/", homepage)])
