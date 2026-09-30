"""FastAPI app. Mounted under /api; served by uvicorn on :8000 (``uv run mantle-api``)."""

from __future__ import annotations

import time
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Annotated, Any

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from mantle_ml import registry as mlreg

from . import __version__, live
from .engine import Engine
from .settings import Settings, get_settings
from .store import Store, UnknownWellError, WellData
from .util import clean

SOURCES = {
    "weather": {"id": "open-meteo", "kind": "real", "name": "Open-Meteo historical weather (Baghewala)", "licence": "CC BY 4.0"},
    "threew_events": {"id": "3w", "kind": "real", "name": "Petrobras 3W v2.0.0 undesirable-event time series",
                      "licence": "CC BY 4.0"},
    "viscosity_lit": {"id": "viscosity-literature", "kind": "real", "name": "Heavy-oil viscosity-temperature tables (open-access papers)",
                      "licence": "CC BY 4.0"},
}


class Scenario(BaseModel):
    day: float
    spm: float
    kd: float
    steam: float


class ApplyBody(BaseModel):
    spm: float = Field(ge=0.5, le=15)
    kd: float = Field(ge=0.4, le=0.7)


class ScheduleBody(BaseModel):
    steam: float = Field(ge=300, le=1400)
    p_inj: float = Field(ge=1, le=20)
    soak: float = Field(ge=0, le=30)
    cutoff: float = Field(ge=20, le=200)


def build_engine(settings: Settings | None = None) -> Engine:
    s = settings or get_settings()
    reg = mlreg.Registry.load(s.models_dir, skip=("O3",))
    return Engine(s, Store(s.db_path), reg)


def warm(e: Engine) -> None:
    wid = e.s.showcase_well
    try:
        wd = e.store.well(wid)
    except UnknownWellError:
        return
    d = e.defaults(wd)
    a = (wd, d["day"], d["spm"], d["kd"], d["steam"])
    e.state(*a)
    e.profile(*a)
    e.dyno(*a)
    e.health(*a)
    e.series(wd, d["spm"], d["kd"], d["steam"])
    e.plan(wd)
    e.well_detail(wd)


@asynccontextmanager
async def lifespan(app: FastAPI):
    e = build_engine()
    app.state.engine = e
    t = time.perf_counter()
    warm(e)
    app.state.warm_s = time.perf_counter() - t
    yield
    e.store.close()


def engine_of(request: Request) -> Engine:
    return request.app.state.engine


def get_well(well_id: str, e: Annotated[Engine, Depends(engine_of)]) -> WellData:
    try:
        return e.store.well(well_id)
    except UnknownWellError:
        raise HTTPException(404, f"unknown well {well_id!r}") from None


def scenario(wd: Annotated[WellData, Depends(get_well)], e: Annotated[Engine, Depends(engine_of)],
             day: Annotated[float | None, Query(ge=0, le=120)] = None,
             spm: Annotated[float | None, Query(ge=0.5, le=15)] = None,
             kd: Annotated[float | None, Query(ge=0.4, le=0.7)] = None,
             steam: Annotated[float | None, Query(ge=300, le=1400)] = None) -> Scenario:
    d = e.defaults(wd)
    return Scenario(day=round(d["day"] if day is None else day, 2), spm=round(d["spm"] if spm is None else spm, 3),
                    kd=round(d["kd"] if kd is None else kd, 3), steam=float(round(d["steam"] if steam is None else steam)))


def curve(wd: Annotated[WellData, Depends(get_well)], e: Annotated[Engine, Depends(engine_of)],
          spm: Annotated[float | None, Query(ge=0.5, le=15)] = None,
          kd: Annotated[float | None, Query(ge=0.4, le=0.7)] = None,
          steam: Annotated[float | None, Query(ge=300, le=1400)] = None) -> Scenario:
    return scenario(wd, e, 0.0, spm, kd, steam)


Well = Annotated[WellData, Depends(get_well)]
Eng = Annotated[Engine, Depends(engine_of)]
Scn = Annotated[Scenario, Depends(scenario)]
Crv = Annotated[Scenario, Depends(curve)]

router = APIRouter(prefix="/api")


@router.get("/health", tags=["service"])
def health(e: Eng) -> dict:
    return {"status": "ok", "version": __version__, "models_loaded": list(e.reg.loaded)}


@router.get("/meta", tags=["service"])
def meta(e: Eng) -> dict:
    s = e.s
    sources: list[dict[str, Any]] = [{"id": "physics-synthetic", "kind": "physics_synthetic",
                "name": "Physics-twin synthetic field records (S1 roster, S2 cycles, S5 failures)", "licence": "generated"}]
    sources += [{**v, "in_database": e.store.table_count(t) > 0} for t, v in SOURCES.items()]
    models = [{"id": r["id"], "loaded": r["loaded"], "version": r["version"], "trained_at": r["trained_at"],
               "source": r["source"], "trained_on": r["data_hash"], "metrics": r["metrics"]} for r in e.reg.describe()]
    gen = datetime.fromtimestamp(s.db_path.stat().st_mtime).isoformat(timespec="seconds") if s.db_path.exists() else None
    return clean({"data_source": "physics_synthetic", "sources": sources, "models": models,
                  "prices": {"oil_inr_bbl": s.oil_inr_bbl, "steam_inr_t": s.steam_inr_t, "power_inr_kwh": s.power_inr_kwh},
                  "field": s.field_name, "reservoir": s.reservoir, "generated_at": gen})


@router.get("/wells", tags=["wells"])
def wells(e: Eng) -> list[dict]:
    return clean(e.roster())


@router.get("/wells/{well_id}", tags=["wells"])
def well(wd: Well, e: Eng) -> dict:
    return e.well_detail(wd)


@router.get("/wells/{well_id}/state", tags=["twin"])
def state(wd: Well, e: Eng, sc: Scn) -> dict:
    return e.state(wd, sc.day, sc.spm, sc.kd, sc.steam)


@router.get("/wells/{well_id}/series", tags=["twin"])
def series(wd: Well, e: Eng, sc: Crv) -> dict:
    return e.series(wd, sc.spm, sc.kd, sc.steam)


@router.get("/wells/{well_id}/profile", tags=["twin"])
def profile(wd: Well, e: Eng, sc: Scn) -> dict:
    return e.profile(wd, sc.day, sc.spm, sc.kd, sc.steam)


@router.get("/wells/{well_id}/dyno", tags=["twin"])
def dyno(wd: Well, e: Eng, sc: Scn) -> dict:
    return e.dyno(wd, sc.day, sc.spm, sc.kd, sc.steam)


@router.get("/wells/{well_id}/health", tags=["twin"])
def well_health(wd: Well, e: Eng, sc: Scn) -> dict:
    return e.health(wd, sc.day, sc.spm, sc.kd, sc.steam)


@router.get("/wells/{well_id}/recommend/pump", tags=["twin"])
def recommend(wd: Well, e: Eng, sc: Scn) -> dict:
    return e.recommend(wd, sc.day, sc.spm, sc.kd, sc.steam)


@router.get("/wells/{well_id}/plan/next-cycle", tags=["twin"])
def plan(wd: Well, e: Eng) -> dict:
    return e.plan(wd)


@router.post("/wells/{well_id}/apply", tags=["actions"])
def apply(wd: Well, e: Eng, body: ApplyBody) -> dict:
    return e.apply(wd, body.spm, body.kd)


@router.post("/wells/{well_id}/plan/schedule", tags=["actions"])
def schedule(wd: Well, e: Eng, body: ScheduleBody) -> dict:
    return e.schedule(wd, body.model_dump())


@router.websocket("/wells/{well_id}/live")
async def live_ws(ws: WebSocket, well_id: str) -> None:
    e: Engine = ws.app.state.engine
    try:
        wd = e.store.well(well_id)
    except UnknownWellError:
        await ws.close(code=4404)
        return
    await live.serve(ws, e, wd)


def create_app() -> FastAPI:
    s = get_settings()
    app = FastAPI(title="Mantle API", version=__version__, lifespan=lifespan,
                  description="Digital twin of a cyclic-steam heavy-oil well: physics, recorded data and ML/optimiser models.")
    app.add_middleware(CORSMiddleware, allow_origins=s.cors_origins, allow_methods=["*"], allow_headers=["*"])
    app.include_router(router)
    return app


app = create_app()
_: Any = None
