"""Add Task and Project models

Revision ID: 608a6f9fce76
Revises: 718a644abc08
Create Date: 2023-11-13 20:52:05.127493

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "608a6f9fce76"
down_revision: Union[str, None] = "718a644abc08"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "project",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "task",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("log", sa.ARRAY(sa.String()), nullable=True),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.Column("author", sa.String(), nullable=True),
        sa.Column("assignee", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["project.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_task_status"), "task", ["status"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_task_status"), table_name="task")
    op.drop_table("task")
    op.drop_table("project")
    # ### end Alembic commands ###
