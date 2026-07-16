import logging
from logging.config import fileConfig

from flask import current_app

from alembic import context

# это объект Config из Alembic, через него берём
# значения из используемого .ini файла
config = context.config

# Разбираем конфиг-файл для настройки логирования Python.
# По сути эта строка настраивает логгеры.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')


def get_engine():
    try:
        # работает с Flask-SQLAlchemy<3 и Alchemical
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # работает с Flask-SQLAlchemy>=3
        return current_app.extensions['migrate'].db.engine


def get_engine_url():
    try:
        return get_engine().url.render_as_string(hide_password=False).replace(
            '%', '%%')
    except AttributeError:
        return str(get_engine().url).replace('%', '%%')


# сюда добавляется объект MetaData твоих моделей
# для поддержки 'autogenerate'
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
config.set_main_option('sqlalchemy.url', get_engine_url())
target_db = current_app.extensions['migrate'].db

# остальные значения из конфига, которые нужны env.py,
# можно получить так:
# my_important_option = config.get_main_option("my_important_option")
# ... и т.д.


def get_metadata():
    if hasattr(target_db, 'metadatas'):
        return target_db.metadatas[None]
    return target_db.metadata


def run_migrations_offline():
    """Запуск миграций в 'offline' режиме.

    Тут контекст настраивается только через URL,
    без Engine, хотя Engine тоже подошёл бы.
    Пропуская создание Engine, можно вообще
    обойтись без DBAPI.

    Вызовы context.execute() здесь просто выводят
    переданную строку в скрипт.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=get_metadata(), literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Запуск миграций в 'online' режиме.

    В этом случае нужно создать Engine
    и связать соединение с контекстом.

    """

    # этот колбэк нужен, чтобы не генерировать пустую авто-миграцию,
    # когда в схеме нет изменений
    # см.: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    conf_args = current_app.extensions['migrate'].configure_args
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    connectable = get_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            **conf_args
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
