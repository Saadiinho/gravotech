from fastapi import FastAPI, HTTPException, Request

from app.api.models import (
    LoadFile,
    Mask,
    PushFile,
    SetValue,
    GetValue,
    Rule,
    Response,
    HealthcheckResponse,
)
from app.config import settings
from libs.core.gravotech import Gravotech

IP = settings.graveuse_ip
PORT = settings.graveuse_port

__version__ = "1.0.0"


async def lifespan(app: FastAPI):
    instance = Gravotech(ip=IP, port=PORT)
    app.state.graveuse = instance
    yield
    instance.Streamer.close()


app = FastAPI(
    lifespan=lifespan,
    title="Gravotech",
    description="API for communication with app graveuse",
    version=__version__,
    root_path="/api/v1",
)


def check_graveuse(graveuse: Gravotech) -> None:
    if graveuse is None:
        raise HTTPException(status_code=400, detail="Not connected to Gravotech")


@app.get("/healthcheck", response_model=HealthcheckResponse)
async def healthcheck():
    return {
        "name": "Gravotech API",
        "status": "OK",
        "version": __version__,
    }


@app.post("/acquit-default", response_model=Response)
async def ad(request: Request):
    graveuse = request.app.state.graveuse
    check_graveuse(graveuse)
    try:
        resp = graveuse.Actions.ad()
        return {"response": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/stop-marquage", response_model=Response)
async def am(request: Request):
    graveuse = request.app.state.graveuse
    check_graveuse(graveuse)
    try:
        resp = graveuse.Actions.am()
        return {"response": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/start-marquage", response_model=Response)
async def go(request: Request):
    graveuse = request.app.state.graveuse
    check_graveuse(graveuse)
    try:
        resp = graveuse.Actions.go()
        return {"response": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get-state", response_model=Response)
async def gp(request: Request):
    graveuse = request.app.state.graveuse
    check_graveuse(graveuse)
    try:
        resp = graveuse.Actions.gp()
        return {"response": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/load-file", response_model=Response)
async def ld(request_body: LoadFile, request: Request):
    graveuse = request.app.state.graveuse
    check_graveuse(graveuse)
    try:
        resp = graveuse.Actions.ld(
            request_body.filename,
            request_body.nb_marking,
            request_body.mode
        )
        return {"response": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/list-file", response_model=Response)
async def ls(request_body: Mask, request: Request):
    graveuse = request.app.state.graveuse
    check_graveuse(graveuse)
    try:
        resp = graveuse.Actions.ls(request_body.mask)
        return {"response": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/push-file", response_model=Response)
async def pf(request_body: PushFile, request: Request):
    graveuse = request.app.state.graveuse
    check_graveuse(graveuse)
    try:
        filename = request_body.filename
        data = request_body.data
        resp = graveuse.Actions.pf(filename, data)
        return {"response": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/remove-file", response_model=Response)
async def rm(request_body: Mask, request: Request):
    graveuse = request.app.state.graveuse
    check_graveuse(graveuse)
    try:
        resp = graveuse.Actions.rm(request_body.mask)
        return {"response": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/set-rule", response_model=Response)
async def sp(request_body: Rule, request: Request):
    graveuse = request.app.state.graveuse
    check_graveuse(graveuse)
    try:
        resp = graveuse.Actions.sp(request_body.rule)
        return {"response": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get-status", response_model=Response)
async def st(request: Request):
    graveuse = request.app.state.graveuse
    check_graveuse(graveuse)
    try:
        resp = graveuse.Actions.st()
        return {"response": resp}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/get-value", response_model=Response)
async def vg(request_body: GetValue, request: Request):
    graveuse = request.app.state.graveuse
    check_graveuse(graveuse)
    try:
        resp = graveuse.Actions.vg(request_body.value)
        return {"response": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/set-value", response_model=Response)
async def vs(request_body: SetValue, request: Request):
    graveuse = request.app.state.graveuse
    check_graveuse(graveuse)
    try:
        index = request_body.index
        text = request_body.text
        resp = graveuse.Actions.vs(index, text)
        return {"response": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
