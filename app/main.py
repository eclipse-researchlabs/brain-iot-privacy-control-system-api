"""

:author: Angelo Cutaia
*******************************************************************************
* Copyright (C) 2021 LINKS Foundation
*
* This program and the accompanying materials are made
* available under the terms of the Eclipse Public License 2.0
* which is available at https://www.eclipse.org/legal/epl-2.0/
*
* SPDX-License-Identifier: EPL-2.0
 ******************************************************************************
"""

# Third Party
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_redoc_html
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Internal
from .db.postgresql import get_database
from .internals.logger import get_logger
from .internals.session import get_keycloak_session, close_keycloak_session
from .routers import brain_user, gateway, brain_consumers

# Instantiate app
database = get_database()
app = FastAPI(
    root_path="/brainpep",
    docs_url=None,
    redoc_url=None,
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(brain_user.router)
app.include_router(gateway.router)
app.include_router(brain_consumers.router)


# Configure logger
@app.on_event("startup")
async def configure_logger():
    get_logger()
    get_keycloak_session()
    await database.connect()


# Shutdown logger
@app.on_event("shutdown")
async def shutdown_logger():
    logger = get_logger()
    await close_keycloak_session()
    await database.disconnect()
    await logger.shutdown()


# Documentation end-point
@app.get("/docs", include_in_schema=False)
async def custom_redoc_ui_html():
    return get_redoc_html(
        openapi_url=f"/brainpep{app.openapi_url}",
        title="BrainPeP",
        redoc_js_url="/brainpep/static/redoc.standalone.js",
        redoc_favicon_url="/brainpep/static/BRAIN_IoT_Favicon.png",
    )


# Cache and custom documentation
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="BrainPeP",
        version="1.0.0",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "/brainpep/static/BRAIN_IoT_FullLogo_LD.png"
    }
    openapi_schema["servers"] = [{"url": app.root_path}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Substitute the docs with the custom one
app.openapi = custom_openapi
