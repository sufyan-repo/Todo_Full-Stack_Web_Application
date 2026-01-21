import asyncio
import sys
import os
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO

# Capture any output during initialization
stdout_capture = StringIO()
stderr_capture = StringIO()

try:
    with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
        from app.main import app
        from app.db import create_db_and_tables
        
        # Test the database connection
        async def test_db():
            try:
                await create_db_and_tables()
                return True, None
            except Exception as e:
                return False, str(e)
        
        db_ok, db_error = asyncio.run(test_db())
        
        if not db_ok:
            print(f"DB Error: {db_error}")
            sys.exit(1)
        
        print("Database OK")
        
        # Test that we can access routes
        routes = []
        for route in app.routes:
            if hasattr(route, 'path'):
                routes.append(route.path)
        print(f"Routes: {routes[:5]}...")  # Just first 5 routes
        
        # Now try to start the server
        import uvicorn
        
        print("Attempting to start server...")
        
        # Write a simple script that we'll execute in a subprocess
        server_script = '''
import uvicorn
from app.main import app

print("Starting uvicorn server...")
uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")
'''
        
        # Write the server script to a temporary file
        with open('temp_server.py', 'w') as f:
            f.write(server_script)
        
        # Execute the server in a subprocess
        import subprocess
        import time
        
        print("Launching server subprocess...")
        proc = subprocess.Popen([sys.executable, 'temp_server.py'])
        
        # Wait a bit to see if it starts
        time.sleep(3)
        
        # Check if the process is still running
        if proc.poll() is None:
            print("Server process is running (PID: {})".format(proc.pid))
            print("Server should be available at http://127.0.0.1:8080")
            
            # Keep this parent process alive
            try:
                proc.wait()
            except KeyboardInterrupt:
                proc.terminate()
                proc.wait()
        else:
            print("Server process exited early")
            print("Return code:", proc.returncode)
            
except Exception as e:
    print(f"Error during initialization: {e}")
    import traceback
    traceback.print_exc()
finally:
    # Print captured output if there was any
    stdout_output = stdout_capture.getvalue()
    stderr_output = stderr_capture.getvalue()
    
    if stdout_output.strip():
        print("Captured stdout:", stdout_output)
    if stderr_output.strip():
        print("Captured stderr:", stderr_output)