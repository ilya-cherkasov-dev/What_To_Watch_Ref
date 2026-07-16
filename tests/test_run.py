import os
import subprocess
import sys
import time


def test_flask_run(project_root):
    env = os.environ.copy()
    env["FLASK_APP"] = "opinions_app"
    env["FLASK_DEBUG"] = "1"
    env["DATABASE_URI"] = "sqlite:///test.db"
    env["SECRET_KEY"] = "test-secret-key"

    process = subprocess.Popen(
        [sys.executable, "-m", "flask", "run"],
        cwd=project_root,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        time.sleep(5)
        assert process.poll() is None, "Приложение не запускается командой `flask run`."
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()