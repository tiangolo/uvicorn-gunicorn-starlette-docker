import sys

from starlette.applications import Starlette
from starlette.responses import JSONResponse

version = f"{sys.version_info.major}.{sys.version_info.minor}"

app = Starlette()


@app.route("/")
async def homepage(request):
    message = f"Hello world! From Starlette running on Uvicorn with Gunicorn. Using Python {version}"
    return JSONResponse({"message": message})
