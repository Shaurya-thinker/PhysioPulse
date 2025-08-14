#!/usr/bin/env python3
"""
PhysioPulse Startup Script
This script starts the PhysioPulse telerehabilitation system.
"""
import os
import sys
import argparse
from pathlib import Path

def setup_environment():
    """Setup the environment for PhysioPulse."""
    print("🔧 Setting up PhysioPulse environment...")
    
    # Create required directories
    directories = ["input_videos", "output_data", "logs", "temp"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        if os.path.exists("env.example"):
            print("📝 Creating .env file from template...")
            with open("env.example", "r") as src, open(".env", "w") as dst:
                dst.write(src.read())
            print("✅ Created .env file from template")
        else:
            print("⚠️  No .env file found. Please create one manually.")
    
    print("✅ Environment setup complete")

def run_tests():
    """Run system tests."""
    print("🧪 Running system tests...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "test_system.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed")
            return True
        else:
            print("❌ Some tests failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return False

def start_api(host="0.0.0.0", port=8000, debug=False):
    """Start the API server."""
    print(f"🚀 Starting PhysioPulse API on {host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🔍 Health Check: http://{host}:{port}/health")
    print("Press Ctrl+C to stop the server")
    
    try:
        import uvicorn
        from src.api import app
        
        uvicorn.run(
            app,
            host=host,
            port=port,
            reload=debug,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down PhysioPulse...")
    except Exception as e:
        print(f"❌ Failed to start API: {e}")
        sys.exit(1)

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="PhysioPulse Telerehabilitation System")
    parser.add_argument("--setup", action="store_true", help="Setup environment only")
    parser.add_argument("--test", action="store_true", help="Run tests only")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    print("🏥 PhysioPulse - AI-Powered Telerehabilitation System")
    print("=" * 50)
    
    # Setup environment
    setup_environment()
    
    if args.setup:
        print("✅ Setup complete. Run without --setup to start the API.")
        return
    
    # Run tests if requested
    if args.test:
        if not run_tests():
            print("❌ Tests failed. Please fix issues before starting the API.")
            sys.exit(1)
        print("✅ Tests complete. Run without --test to start the API.")
        return
    
    # Run tests before starting (unless explicitly skipped)
    if not args.debug:  # Skip tests in debug mode for faster development
        print("🧪 Running quick system check...")
        if not run_tests():
            print("❌ System check failed. Please fix issues before starting the API.")
            print("💡 You can run with --debug to skip tests during development.")
            sys.exit(1)
    
    # Start the API
    start_api(args.host, args.port, args.debug)

if __name__ == "__main__":
    main()
