import sqlalchemy
from sqlalchemy import DateTime
from main.database_set import metadata

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("full_name", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("chat_id", sqlalchemy.BigInteger),
    sqlalchemy.Column('username', sqlalchemy.String),
    sqlalchemy.Column('lang', sqlalchemy.String),
    sqlalchemy.Column("phone_number", sqlalchemy.String),
    sqlalchemy.Column('created_at', sqlalchemy.DateTime(timezone=True))
)

menu = sqlalchemy.Table(
    "menu",
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column('lang', sqlalchemy.String),
    sqlalchemy.Column('name_to_get', sqlalchemy.String), # This column need get one menu without translations
)

foods = sqlalchemy.Table(
    "foods",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.Integer),
    sqlalchemy.Column('photo', sqlalchemy.String),
    sqlalchemy.Column("menu", sqlalchemy.String),
    sqlalchemy.Column('lang', sqlalchemy.String)
)

payemnts = sqlalchemy.Table(
    "payments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("lang", sqlalchemy.String),
)

cards = sqlalchemy.Table(
    "cards",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('card_number', sqlalchemy.String),
    sqlalchemy.Column('card_holder', sqlalchemy.String),
)

filials = sqlalchemy.Table(
    'filials',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String),
    sqlalchemy.Column('latitude', sqlalchemy.String),
    sqlalchemy.Column('longitude', sqlalchemy.String),
    sqlalchemy.Column("lang", sqlalchemy.String)
)

history_buys = sqlalchemy.Table(
    'history_buys',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('chat_id', sqlalchemy.BigInteger),
    sqlalchemy.Column('order_number', sqlalchemy.Integer)
)

order_numbers = sqlalchemy.Table(
    'order_numbers',
    metadata,
    sqlalchemy.Column("order_number", sqlalchemy.BigInteger),
    sqlalchemy.Column("product", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.Integer),
    sqlalchemy.Column("quantity", sqlalchemy.Integer),
    sqlalchemy.Column("total", sqlalchemy.Integer),
)

basket = sqlalchemy.Table(
    'basket',
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("product", sqlalchemy.String),
    sqlalchemy.Column("quantity", sqlalchemy.Integer),
    sqlalchemy.Column("price", sqlalchemy.Integer),
    sqlalchemy.Column("chat_id", sqlalchemy.BigInteger),
)

admins = sqlalchemy.Table(
    'admins',
    metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('chat_id', sqlalchemy.BigInteger)
)
