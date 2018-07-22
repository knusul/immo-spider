from sqlalchemy import Table, Column, Integer, String, MetaData, Date, DateTime, Float, Boolean
from migrate.changeset.constraint import UniqueConstraint

meta = MetaData()

account = Table(
    'rented_rooms', meta,
    Column('id', Integer, primary_key=True),
    Column('properties_id', Integer),
    Column('created_at', DateTime),
    Column('price', Float),
    Column('age', Integer, default=0),
    Column('lat', Float),
    Column('lon', Float),
)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    account.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    cons.drop()
    account.drop()
