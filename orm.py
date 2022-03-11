import psycopg2

connection = psycopg2.connect( #-> \c db_name
    database='db_practice',
    user='test_user',
    password='',
    host='localhost',
    port='5432'
)
print('Database successfully opened')

cursor = connection.cursor()


cursor.execute(
    """CREATE TABLE company (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        city VARCHAR(50) NOT NULL
    )
    """
)

print('Table successfully created')
connection.commit()
connection.close()


cursor.execute(
    """
    INSERT INTO company(name, city) VALUES ('IBM', 'Los Angeles'),
    ('Apple', 'Cupertino'),('HP', 'San Francisco'), ('DELL', 'New York')
    """
)

connection.commit()
print('Inserted successfully')
connection.close()

cursor.execute(
    '''
    INSERT INTO company(name, city) VALUES ('Samsung', 'Seoul')
    '''
)
cursor.execute(
    '''
    INSERT INTO company(name, city) VALUES ('Tokyota', 'Tokyo')
    '''
)

connection.commit()
print('Inserted successfully')
connection.close()

cursor = connection.cursor()
cursor.execute(
    'SELECT * FROM company'
)
# print(cursor.fetchall())
data = cursor.fetchall()
for item in data:
    # print(f"id: {item[0]}, name: {item[1]}, city: {item[2]}")
    print(*item)
connection.close()

cursor.execute(
    'SELECT name, city FROM company WHERE id=4'
)

data = cursor.fetchone()
print(data)

cursor.execute(
    '''
    UPDATE company SET city='New Mexico' WHERE id=2
    '''
)
connection.commit()
cursor.execute(
    '''SELECT * from company ORDER BY id'''
)
data = cursor.fetchall()
for item in data:
    print(*item)
connection.close()

cursor.execute(
    """
    DELETE FROM company WHERE id=3
    """
)
connection.commit()
print(f'Total count of deleted {cursor.rowcount}')
cursor.execute(
    'SELECT * FROM company ORDER BY id'
)

data = cursor.fetchall()
for item in data:
    print(*item)
connection.close()


students_table.create(bind=engine)
print('Successfully created table')

inserted_data = students_table.insert().values(name='Alice',
                                                last_name='White')
engine.execute(inserted_data)
print('Successfully inserted')

from sqlalchemy import select
query = select([students_table.c.name,students_table.c.last_name])
data = engine.execute(query).fetchall()
for item in data:
    print(*item)



from sqlalchemy import Column, Table, Integer, String, MetaData

metadata = MetaData()
company_table = Table(
    'company', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('city', String)
)
metadata.create_all(engine)
class Company:
    def __init__(self, name, city):
        self.name = name
        self.city = city

    def __str__(self):
        return f'Company {self.name} in {self.city} city'

from sqlalchemy.orm import mapper
mapper(Company, company_table)
print('Successfully created table')

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
engine = create_engine('postgresql+psycopg2://test_user: @localhost:5432/db_practice')

Base = declarative_base()

class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)

    def __init__(self,name, city):
        self.name = name
        self.city = city

    def __str__(self):
        return f'Company {self.name} in {self.city} city'
Base.metadata.create_all(engine)
print('Table created')

Session = sessionmaker(bind=engine)
session = Session()
apple = Company(name= 'Apple', city='Cupertino')
session.add(apple)
session.commit()

query = session.query(Company.name, Company.city).all()
print(query)

samsung = Company('Samsung', 'Seoul')
session.add(samsung)
session.commit()
query = session.query(Company.name, Company.city).all()
print(query)

our_company = session.query(Company).filter_by(city='Seoul').first()
print(our_company)

session.add_all([Company('IBM', 'Washington'), Company('Dell', 'New York')])
session.commit()
query = session.query(Company.name, Company.city).order_by('name').all()
for item in query:
    print(*item)
print(*query)