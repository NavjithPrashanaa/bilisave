"""
BijliSave Full-Stack Application Launcher
Runs FastAPI backend on port 8000 and Vite frontend on port 5173.
"""

import os
import sys
import time
import subprocess
import signal

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")
DB_FILE = os.path.join(BACKEND_DIR, "bijlisave.db")

def main():
    print("=" * 60)
    print("⚡ Starting BijliSave - Electricity Bill Reduction App")
    print("=" * 60)

    # 1. Check database and seed if missing or requested
    if not os.path.exists(DB_FILE) or "--seed" in sys.argv:
        print("[1/3] Seeding demo database (Tamil Nadu TNEB household)...")
        seed_cmd = [sys.executable, "seed_data.py"]
        subprocess.run(seed_cmd, cwd=BACKEND_DIR, check=True)
    else:
        print("[1/3] Database found at backend/bijlisave.db.")

    # 2. Start Backend (Uvicorn)
    print("[2/3] Launching FastAPI Backend on http://localhost:8000...")
    backend_cmd = [
        sys.executable, "-m", "uvicorn", "app.main:app",
        "--host", "127.0.0.1", "--port", "8000"
    ]
    backend_proc = subprocess.Popen(
        backend_cmd,
        cwd=BACKEND_DIR,
        shell=(sys.platform == "win32")
    )

    # Allow backend 1.5 seconds to bind port
    time.sleep(1.5)

    # 3. Start Frontend (Vite)
    print("[3/3] Launching React+Vite Frontend on http://localhost:5173...")
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    frontend_cmd = [npm_cmd, "run", "dev", "--", "--port", "5173", "--host"]
    frontend_proc = subprocess.Popen(
        frontend_cmd,
        cwd=FRONTEND_DIR,
        shell=(sys.platform == "win32")
    )

    print("\n" + "=" * 60)
    print("✨ BIJLISAVE IS RUNNING!")
    print("🌐 Frontend URL: http://localhost:5173")
    print("🔌 Backend API & Docs: http://localhost:8000/docs")
    print("\nDemo Accounts for Evaluation:")
    print("  • Owner:  demo@bijlisave.in    Password:  Bijli@2026")
    print("  • Family: family@bijlisave.in  Password:  Bijli@2026")
    print("  • Invite Code: BIJLI888")
    print("=" * 60)
    print("Press Ctrl+C to terminate both servers.\n")

    try:
        while True:
            time.sleep(1)
            if backend_proc.poll() is not None:
                print("Backend exited unexpectedly.")
                break
            if frontend_proc.poll() is not None:
                print("Frontend exited unexpectedly.")
                break
    except KeyboardInterrupt:
        print("\nShutting down BijliSave servers...")
    finally:
        try:
            backend_proc.terminate()
        except Exception:
            pass
        try:
            frontend_proc.terminate()
        except Exception:
            pass
        print("Done. Goodbye!")

if __name__ == "__main__":
    main()
