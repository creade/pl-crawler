"""empty message

Revision ID: 155d2893ece
Revises: 3da074383b1
Create Date: 2015-11-24 21:29:31.942167

"""

# revision identifiers, used by Alembic.
revision = '155d2893ece'
down_revision = '3da074383b1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('img_urls', sa.Column('site_url_id', sa.Integer(), nullable=False))
    op.drop_constraint('img_urls_job_id_fkey', 'img_urls', type_='foreignkey')
    op.create_foreign_key(None, 'img_urls', 'site_urls', ['site_url_id'], ['id'])
    op.drop_column('img_urls', 'job_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('img_urls', sa.Column('job_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'img_urls', type_='foreignkey')
    op.create_foreign_key('img_urls_job_id_fkey', 'img_urls', 'jobs', ['job_id'], ['id'])
    op.drop_column('img_urls', 'site_url_id')
    ### end Alembic commands ###