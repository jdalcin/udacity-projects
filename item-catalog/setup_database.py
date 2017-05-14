from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import create_engine


Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	encrypted_password = Column(String(250), nullable = False)
	email = Column(String(250), nullable = False)
	picture = Column(String(250))

class Item(Base):
	__tablename__ = 'item'

	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	category = Column(String(250), nullable = False)
	picture = Column(String(250))
	description = Column(Text)
	date_uploaded = Column(DateTime(timezone = True), nullable = False, server_default = func.now())
	user_id = Column(Integer, ForeignKey('user.id'))

	user = relationship(User)
	item_owner_name = None

	@property
	def serialize(self):
		return {
			'name': self.name,
			'category': self.category,
			'picture': self.picture,
			'description': self.description,
			'date_uploaded': str(self.date_uploaded),
			'item_owner': self.item_owner_name
		}
