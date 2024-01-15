# Copyright (c) 2024 Daxa. All rights reserved.

import uvicorn
from fastapi import FastAPI
from routers.routers import router_instance

# Initialise app instance
app = FastAPI()

# Register the router instance with the main app
app.include_router(router_instance.router)


if __name__ == "__main__":
    # running local server
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
