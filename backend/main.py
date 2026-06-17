from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from api import workflows, webhooks

app = FastAPI()

# Allow CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception handler to match the expected format of the frontend
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        # Handle custom ValueError messages raised by @model_validator
        msg = err.get("msg", "")
        # If the msg is our custom concatenated string (" | ".join(...)), split it
        if "Value error, " in msg:
            msg = msg.replace("Value error, ", "")
            
        if " | " in msg:
            errors.extend(msg.split(" | "))
        else:
            loc = " -> ".join([str(l) for l in err.get("loc", [])])
            errors.append(f"{loc}: {msg}")
            
    print(f"❌ Workflow validation failed: {errors}")
    return JSONResponse(
        status_code=400,
        content={"success": False, "errors": errors}
    )

app.include_router(workflows.router, prefix="/api")
app.include_router(webhooks.router, prefix="/webhook")

@app.get("/health")
def health_check():
    return {"status": "ok"}
