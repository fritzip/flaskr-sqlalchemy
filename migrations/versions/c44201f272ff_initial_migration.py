"""Initial migration

Revision ID: c44201f272ff
Revises: 
Create Date: 2024-04-03 21:23:35.441643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c44201f272ff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_tag'))
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
    sa.UniqueConstraint('username', name=op.f('uq_user_username'))
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=140), nullable=True),
    sa.Column('body', sa.String(length=300), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], name=op.f('fk_post_author_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_post'))
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['user.id'], name=op.f('fk_comment_author_id_user')),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], name=op.f('fk_comment_post_id_post')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_comment'))
    )
    op.create_table('post_tags',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], name=op.f('fk_post_tags_post_id_post')),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], name=op.f('fk_post_tags_tag_id_tag')),
    sa.PrimaryKeyConstraint('post_id', 'tag_id', name=op.f('pk_post_tags'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_tags')
    op.drop_table('comment')
    op.drop_table('post')
    op.drop_table('user')
    op.drop_table('tag')
    # ### end Alembic commands ###
