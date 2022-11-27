"""insert table artigos e usuarios

Revision ID: ecf0624cd9c0
Revises: 
Create Date: 2022-11-26 22:07:40.437754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecf0624cd9c0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(length=256), nullable=True),
    sa.Column('sobrenome', sa.String(length=256), nullable=True),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('senha', sa.String(length=256), nullable=False),
    sa.Column('eh_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usuarios_email'), 'usuarios', ['email'], unique=True)
    op.create_table('artigos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('titulo', sa.String(length=256), nullable=True),
    sa.Column('descricao', sa.String(length=256), nullable=True),
    sa.Column('url_fonte', sa.String(length=256), nullable=True),
    sa.Column('usuario_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('artigos')
    op.drop_index(op.f('ix_usuarios_email'), table_name='usuarios')
    op.drop_table('usuarios')
    # ### end Alembic commands ###