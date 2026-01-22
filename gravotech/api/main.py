from typing import Optional
from fastapi import FastAPI, HTTPException

from gravotech.core.gravotech import Gravotech

graveuse = Optional[Gravotech]

IP="127.0.0.1"
PORT=3000

async def lifespan(app: FastAPI):
    app.state.graveuse = Gravotech(ip=IP, port=PORT)
    yield
    graveuse.Streamer.close()
app = FastAPI(
    lifespan=lifespan,
    title="Gravotech",
    description="API for communication with gravotech graveuse",
    version=__version__,
    root_path="/api/v1",
)

@app.post("/st")
def st():
    if graveuse is None:
        raise HTTPException(status_code=400, detail="Not connected to Gravotech")

    try:
        resp = graveuse.Actions.st()
        return resp

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
