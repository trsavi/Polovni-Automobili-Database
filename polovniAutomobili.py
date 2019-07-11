#!/bin/bash/env python

import requests
import urllib.request
from bs4 import BeautifulSoup as bs
import mysql.connector
"""
mydb = mysql.connector.connect(
	host='localhost',
	user='root',
	passwd=''
)
"""
#print(mydb)

def parse_page(url):
	try:
		r = requests.get(url)
		soup = bs(r.text, 'html.parser')
		return soup
	except:
		pass

# returns a list of all models of one brand
def get_models(brand):
	brand = (brand.replace(' ', '-')).lower()
	url ='https://www.polovniautomobili.com/auto-oglasi/pretraga?brand=' + brand
	soup = parse_page(url)
	models= soup.find(id='model')
	models_list=[]
	for model in models:
		models_list.append(model.get_text())
	return models_list[1:]


# returns a list of all brands 
def all_Brands():
	url = 'https://www.polovniautomobili.com/#'
	soup = parse_page(url)
	brands = soup.find(id='brand')
	brands_list = []
	for brand in brands:
		brands_list.append(brand.get_text())

	return brands_list[1:]


# get all cars from one brand and model
def get_cars(brand, model):

	brand = (brand.replace(' ', '-')).lower()
	model = (model.replace(' ', '-')).lower()
	url ='https://www.polovniautomobili.com/auto-oglasi/pretraga?brand=' + brand + '&model[]=' + model

	#soup = parse_page(url)
	
	for i in range(1,6):
		#print('page='+str(i))
		print("")
		soup = parse_page(url+'&page='+str(i))
		pages = soup.findAll('article')
		for page in pages:
				#print(page)
			pageT = page.find('a')
			#print(pageT)
			try:
				title = pageT.get('title')
				if title==None:
					pass
				else:
					#print(title)
					discount = page.find(class_='price price-discount')
					#print(discount.get_text())
					if discount!=None:
						#print(discount.get_text())
						continue
					else:
						price = page.find(class_='price')
						price = price.get_text()
					content = page.findAll(class_='inline-block')
					blocks = []
					for con in content:
						blocks.append(con.get_text())
					dictionary = {
							'Auto': title,
							'Cena': price,
							'Godiste': blocks[0][:-2],
							'Kilometraza':blocks[1][:-2],
							'Gorivo':blocks[2][:-2],
							'Kubikaza':blocks[3],
							'Karoserija':blocks[4],
							'Snaga':blocks[5]
					}

					return(dictionary)

			except:
				pass


get_cars('bmw','x1')


#brands = all_Brands()
"""
for brand in brands:
	print(brand)
	print(get_models(brand))
"""
