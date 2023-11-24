from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.deps import arq, edgedb
from app.routers.v1.router import router as v1_router

app = FastAPI()
app.include_router(v1_router, prefix="/v1")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event() -> None:
    await edgedb.client.ensure_connected()
    await edgedb.client.execute(
        """
        CONFIGURE INSTANCE SET session_idle_timeout :=
            <duration>'5 minutes';
        """
    )
    await edgedb.client.execute(
        """
        CONFIGURE INSTANCE SET session_idle_transaction_timeout :=
            <duration>'5 minutes';
        """
    )
    await arq.init_client()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    if arq.client is not None:
        await arq.client.aclose()
    await edgedb.client.aclose()
