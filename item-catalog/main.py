import datetime

from flask import Flask
from flask import render_template, request, redirect

from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime, create_engine, text
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import desc


category_list = ['Videogames', 'Books', 'Movies', 'Music', 'Technology', 'Food', 'Furniture'] 
Base = declarative_base()

class User(Base):

	__tablename__ = '__User__'

	name = Column(String(200), nullable = False,primary_key = True)

class Item(Base):

	__tablename__ = '__Item__'

	id = Column(Integer, primary_key = True)
	name = Column(String(200), nullable = False)
	description = Column(Text, nullable = False)
	owner = Column(String(200), nullable = False)
	category = Column(String(100), nullable = False)
	date = Column(DateTime(timezone = True), nullable = False, server_default = func.now())

engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

app = Flask(__name__)

@app.route('/')
def main_handler():
	item_list = session.query(Item).order_by(desc(Item.date)).limit(10).all()
	return render_template('homepage.html', item_list = item_list, category_list = category_list)

@app.route('/item')
def item_handler():
	return ''

@app.route('/item/add', methods = ['POST', 'GET'])
def item_add_handler():
	if request.method == 'GET':
		return render_template('item-add.html', category_list = category_list)
	elif request.method == 'POST':
		item_name = request.form['item-name']
		item_description = request.form['item-description']
		item_category = request.form['item-category']
		if not session.query(Item).filter(func.lower(Item.name) == item_name.lower()).first():
			if item_name and item_description and item_category:
				session.add(Item(name = item_name, description = item_description, category = item_category, owner = "Jeremy Dalcin"))
				session.commit()
				return  redirect('/')
			else:
				error = "Invalid Form"
		else:
			error = "Name Already Taken"
		return render_template('item-add.html', category_list = category_list, error = error, item_name = item_name, item_description = item_description, item_category = item_category)

@app.route('/<category>/items', methods = ['POST', 'GET'])
def category_handler(category):
	if request.method == 'GET':
		item_list = session.query(Item).filter(Item.category == category).all()
		return render_template('category.html', item_list = item_list, category = category, category_list = category_list, item_count = len(item_list))

@app.route('/<item>', methods = ['POST', 'GET'])
def item_info_handler(item):
	if request.method == 'GET':
		item = session.query(Item).filter(Item.name == item).first()
		return render_template('item-info.html', item = item, category_list = category_list)

@app.route('/<item>/insert')
def item_insert_handler():
	return ''

@app.route('/<item>/edit', methods = ['POST', 'GET'])
def item_edit_handler(item):
	if request.method == 'GET':
		item = session.query(Item).filter(Item.name == item).first()
		return render_template('edit.html', item_id = item.id, item_name = item.name, item_description = item.description, item_category = item.category, category_list = category_list)
	elif request.method == 'POST':
		item_name_edited = request.form.get('item-name')
		item_description_edited = request.form.get('item-description')
		item_category_edited = request.form.get('item-category')
		item_id = request.form.get('item-id')
		item = session.query(Item).filter(Item.id == item_id).first()
		if item_name_edited and item_description_edited and item_category_edited:
			name_edited_item_count = len(session.query(Item).filter(func.lower(Item.name) == item_name_edited.lower()).all())
			if item_name_edited.lower() == str(item.name).lower() or name_edited_item_count == 0:
				item.name = request.form.get('item-name')
				item.description = request.form.get('item-description')
				item.category = request.form.get('item-category')
				return  redirect('/' + item_name_edited)
			else:
				error = "Name Already Taken"
		else:
			error = "Invalid Form"
		if not item_name_edited:
			item_name_edited = item.name
		return render_template('edit.html', category_list = category_list, error = error, item_name = item_name_edited, item_description = item_description_edited, item_category = item_category_edited, item_id = item_id)
		
		session.commit()
		return redirect('/')

@app.route('/<item>/delete', methods=['POST', 'GET'])
def item_delete_handler(item):
	if request.method == 'GET':
		item_id = request.args.get("item-id")
		item = session.query(Item).filter(Item.id == item_id).first()
		return render_template('delete.html', item = item, category_list = category_list)
	elif request.method == 'POST':
		item_id = request.form.get("item-id")
		item = session.query(Item).filter(Item.id == item_id).first()
		session.delete(item)
		session.commit()
		return redirect('/')

@app.route('/login')
def login_handler():
	return ''


if __name__ == '__main__':
	app.debug = True
	port = 8080;
	print("Running on port: " + str(port))
	app.run(host = '0.0.0.0', port = port)
