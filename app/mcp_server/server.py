# Import FastAPI framework
from fastapi import FastAPI


# Create FastAPI application instance
app = FastAPI(
    title="Autonomous AI DBA MCP Server",
    description="MCP Server for AI DBA Operations Platform",
    version="1.0"
)


# Root endpoint
# Used to verify server availability
@app.get("/")
def home():

    return {
        "message": "Autonomous AI DBA MCP Server Running"
    }


# Health check endpoint
# Used for monitoring and service validation
@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }