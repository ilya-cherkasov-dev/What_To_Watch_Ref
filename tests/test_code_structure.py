from pathlib import Path

import pytest
from sqlalchemy import Integer, String, Text, DateTime


@pytest.mark.parametrize(
    "path",
    (
        "settings.py",
        "opinions_app/__init__.py",
        "opinions_app/cli_commands.py",
        "opinions_app/error_handlers.py",
        "opinions_app/forms.py",
        "opinions_app/models.py",
        "opinions_app/views.py",
    ),
)
def test_required_files_exist(project_root: Path, path: str):
    assert (project_root / path).is_file(),  f"Убедитесь, что файл `{path}` существует."


def test_config_class():
    from settings import Config

    assert Config is not None, (
        "Убедитесь, что в файле `settings.py` описан класс `Config`."
    )
    assert hasattr(Config, "SQLALCHEMY_DATABASE_URI"), (
        "Убедитесь, что класс `Config` содержит атрибут "
        "`SQLALCHEMY_DATABASE_URI`."
    )
    assert hasattr(Config, "SECRET_KEY"), (
        "Убедитесь, что класс `Config` содержит атрибут "
        "`SECRET_KEY`."
    )


@pytest.mark.parametrize(
    "path", ("opinions_app/static", "opinions_app/templates",)
)
def test_required_directories_exist(project_root: Path, path: str):
    assert (project_root / path).is_dir(), f"Убедитесь, что директория `{path}` существует."


def test_opinion_model_exists():
    from opinions_app.models import Opinion
    assert Opinion is not None, "Убедитесь, что в `models.py` описан класс `Opinion`."


def test_opinion_model_fields():
    from opinions_app.models import Opinion

    expected_fields = {"id", "title", "text", "source", "timestamp", "added_by"}
    actual_fields = set(Opinion.__table__.columns.keys())

    assert expected_fields == actual_fields, (
        "Убедитесь, что модель `Opinion` содержит поля "
        "`id`, `title`, `text`, `source`."
    )

    columns = Opinion.__table__.columns

    assert isinstance(columns["id"].type, Integer)
    assert isinstance(columns["title"].type, String)
    assert isinstance(columns["text"].type, Text)
    assert isinstance(columns["source"].type, String)
    assert isinstance(columns["timestamp"].type, DateTime)
    assert isinstance(columns["added_by"].type, String)


def test_opinion_form_fields():
    from opinions_app import app
    from opinions_app.forms import OpinionForm

    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_request_context():
        form = OpinionForm()
    expected_fields = {"title", "text", "source", "submit"}

    assert expected_fields.issubset(form._fields.keys()), (
        "Убедитесь, что форма `OpinionForm` содержит поля "
        "`title`, `text`, `source`, `submit`."
    )


def test_views_exist():
    from opinions_app.views import (
        add_opinion_view,
        index_view,
        opinion_view,
    )

    assert callable(index_view), "Убедитесь, что во `views.py` есть view-функция `index_view`."
    assert callable(add_opinion_view), "Убедитесь, что во `views.py` есть view-функция `add_opinion_view`."
    assert callable(opinion_view), "Убедитесь, что во `views.py` есть view-функция `opinion_view`."


def test_error_handlers_registered():
    from opinions_app import app

    assert 404 in app.error_handler_spec[None], (
        "Убедитесь, что зарегистрирован обработчик ошибки 404 "
        "через декоратор `@app.errorhandler(404)`."
    )

    assert 500 in app.error_handler_spec[None], (
        "Убедитесь, что зарегистрирован обработчик ошибки 500 "
        "через декоратор `@app.errorhandler(500)`."
    )


def test_cli_command_registered():
    from opinions_app import app

    assert "load_opinions" in app.cli.commands, (
        "Убедитесь, что зарегистрирована CLI-команда `load_opinions`."
    )