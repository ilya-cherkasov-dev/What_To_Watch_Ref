from pathlib import Path
import os
import sys

import pytest


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault("FLASK_APP", "opinions_app")
os.environ.setdefault("FLASK_DEBUG", "1")
os.environ.setdefault("DATABASE_URI", "sqlite:///test.db")
os.environ.setdefault("SECRET_KEY", "test-secret-key")


@pytest.fixture(scope="session")
def project_root():
    return BASE_DIR