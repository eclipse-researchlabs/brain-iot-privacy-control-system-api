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

# Standard Library
import os

# Third Party
from gunicorn.app.base import BaseApplication
from pydantic import BaseSettings

# Internal
from app.main import app

# -------------------------------------------------------------


class GunicornSettings(BaseSettings):
    log_level: str
    cores_number: int
    keep_alive: int
    server_port: int
    database_max_connection_number: int
    max_workers_number: int
    timeout: int

    class Config:
        env_file = ".env"


# -------------------------------------------------------------------------------


class StandaloneApplication(BaseApplication):
    """Our Gunicorn application."""

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


# -------------------------------------------------------------------------------


if __name__ == "__main__":
    settings = GunicornSettings()
    options = {
        "bind": f"0.0.0.0:{settings.server_port}",
        "workers": (settings.cores_number * 2) + 1,
        "keepalive": settings.keep_alive,
        "loglevel": settings.log_level,
        "accesslog": "-",
        "errorlog": "-",
        "timeout": settings.timeout,
        "worker_class": "uvicorn.workers.UvicornWorker",
    }
    # Regulate workers
    if options["workers"] > settings.max_workers_number:
        options["workers"] = settings.max_workers_number

    # Ensure connections to the database are set to the max value possible
    os.environ["CONNECTION_NUMBER"] = f'{int(settings.database_max_connection_number / options["workers"])}'

    StandaloneApplication(app, options).run()
