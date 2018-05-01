from sqlalchemy import Table, Column, Integer, String, MetaData, Date, DateTime, Float, Boolean
from migrate.changeset.constraint import UniqueConstraint

meta = MetaData()

account = Table(
    'properties', meta,
    Column('id', Integer, primary_key=True),
    Column('url', String(255)),
    Column('created_at', DateTime),
    Column('added_at', DateTime),
    Column('updated_at', DateTime),
    Column('area', Float),
    Column('description', String(1024)),
    Column('inactive', Boolean),
    Column('price', Float),
    Column('rooms', String(255)),
    Column('sold_by', String(255)),
    Column('title', String(255)),
    Column('type', String(255)),
    Column('visits', Integer, default=0),
)
cons = UniqueConstraint('url', table=account)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    #account.create()
    #cons.create()


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    cons.drop()
    account.drop()
