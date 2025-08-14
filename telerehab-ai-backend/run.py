#!/usr/bin/env python3
"""
PhysioPulse API Server Startup Script
"""
import uvicorn
from src.config import settings

def main():
    """Start the PhysioPulse API server."""
    print("🚀 Starting PhysioPulse Telerehabilitation API Server...")
    print(f"📡 Server will be available at: http://{settings.HOST}:{settings.PORT}")
    print(f"📚 API Documentation: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"🔍 Health Check: http://{settings.HOST}:{settings.PORT}/health")
    print("Press Ctrl+C to stop the server\n")
    
    uvicorn.run(
        "src.api:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )

if __name__ == "__main__":
    main()
