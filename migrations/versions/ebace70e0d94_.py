"""empty message

Revision ID: ebace70e0d94
Revises: 
Create Date: 2018-12-20 17:10:13.887634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebace70e0d94'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=70), nullable=True),
    sa.Column('phone', sa.String(length=25), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customer_email'), 'customer', ['email'], unique=False)
    op.create_index(op.f('ix_customer_name'), 'customer', ['name'], unique=False)
    op.create_index(op.f('ix_customer_phone'), 'customer', ['phone'], unique=False)
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=25), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shippingaddress',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customerID', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=100), nullable=False),
    sa.Column('city', sa.String(length=40), nullable=False),
    sa.Column('state', sa.String(length=40), nullable=False),
    sa.Column('zip', sa.String(length=11), nullable=False),
    sa.ForeignKeyConstraint(['customerID'], ['customer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subscription',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customerID', sa.Integer(), nullable=False),
    sa.Column('itemID', sa.Integer(), nullable=False),
    sa.Column('shippingAddressID', sa.Integer(), nullable=False),
    sa.Column('startDate', sa.Date(), nullable=False),
    sa.Column('stopDate', sa.Date(), nullable=False),
    sa.Column('note', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['customerID'], ['customer.id'], ),
    sa.ForeignKeyConstraint(['itemID'], ['item.id'], ),
    sa.ForeignKeyConstraint(['shippingAddressID'], ['shippingaddress.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subscription')
    op.drop_table('shippingaddress')
    op.drop_table('item')
    op.drop_index(op.f('ix_customer_phone'), table_name='customer')
    op.drop_index(op.f('ix_customer_name'), table_name='customer')
    op.drop_index(op.f('ix_customer_email'), table_name='customer')
    op.drop_table('customer')
    # ### end Alembic commands ###
