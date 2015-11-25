"""empty message

Revision ID: 94fa8bef91
Revises: 155d2893ece
Create Date: 2015-11-24 23:40:47.437110

"""

# revision identifiers, used by Alembic.
revision = '94fa8bef91'
down_revision = '155d2893ece'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('domains',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=2083), nullable=False),
    sa.Column('crawled', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('domain_id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=2083), nullable=False),
    sa.ForeignKeyConstraint(['domain_id'], ['domains.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('img_urls')
    op.drop_table('site_urls')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('site_urls',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('site_urls_id_seq'::regclass)"), nullable=False),
    sa.Column('job_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('url', sa.VARCHAR(length=2083), autoincrement=False, nullable=False),
    sa.Column('crawled', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], name='site_urls_job_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='site_urls_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('img_urls',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('url', sa.VARCHAR(length=2083), autoincrement=False, nullable=False),
    sa.Column('site_url_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['site_url_id'], ['site_urls.id'], name='img_urls_site_url_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='img_urls_pkey')
    )
    op.drop_table('images')
    op.drop_table('domains')
    ### end Alembic commands ###
