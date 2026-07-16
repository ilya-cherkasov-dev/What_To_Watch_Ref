"""initial migration

Revision ID: ca224cc5aa52
Revises: 
Create Date: 2026-07-16 21:15:02.784440

"""
from alembic import op
import sqlalchemy as sa


# идентификаторы ревизии, используются Alembic
revision = 'ca224cc5aa52'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### команды сгенерированы Alembic автоматически — при необходимости поправь! ###
    op.create_table('opinion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('source', sa.String(length=256), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('added_by', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('text')
    )
    with op.batch_alter_table('opinion', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_opinion_timestamp'), ['timestamp'], unique=False)

    # ### конец команд Alembic ###


def downgrade():
    # ### команды сгенерированы Alembic автоматически — при необходимости поправь! ###
    with op.batch_alter_table('opinion', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_opinion_timestamp'))

    op.drop_table('opinion')
    # ### конец команд Alembic ###
