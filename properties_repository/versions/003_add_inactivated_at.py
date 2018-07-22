from sqlalchemy import Table, MetaData, String, Column, Float, DateTime, Integer

meta = MetaData()


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    properties = Table('properties', meta, autoload=True)
    deactivated_c = Column('deactivated_at', DateTime)
    external_id = Column('external_id', Integer)
    deactivated_c.create(properties)
    external_id.create(properties)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    properties = Table('properties', meta, autoload=True)
    properties.c.deactivated_at.drop()
    properties.c.external_id.drop()
