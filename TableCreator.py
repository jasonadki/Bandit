import tabula
import os
import pandas as pd
import numpy as np

class TableCreator():
	def __init__(self):
		self.path = ''
		self.tempTable = []
		self.tempTableName = []
		self.allTables = []
		self.tableNames = []


	def fix_repeat_cell(self, st):
		if(st.count('.') > 1):
			pos = st.find('.', st.find('.') + 1)
			return st[:pos]
		elif(st in [str(i)+'.' for i in range(1,6)]):
			return st[:1]
		else:
			return st

  
	def create_table(self, pageRange, columnNames, tableName, pushRow):
		"""
		Turn a list of pages from pdf into pandas dataframe and add to current list of pages

		:param path: <str> string literal of location of pdf
		:param pageRange: <list> pages that hold current table
		:param tableName: <str> string literal of name of table. Will be used as sheet name
		:param currentBase: <list> List of all tables currently created
		:return: List including newly created table
		"""

		
		# Turn table into pandas data frames
		df = tabula.read_pdf(self.path, guess = True, encoding = 'latin1', pages = pageRange, nospreadsheet = True)

		if pushRow == 1:
			numEl = len(list(df))
			df.columns = [self.fix_repeat_cell(st) for st in list(df.columns)]
			newRow = pd.DataFrame(np.array(list(df)).reshape(1,numEl), columns = list(df.columns))
			df = newRow.append(df, ignore_index = True)
			
		if columnNames != ['']:
			df.columns = columnNames

		self.tempTableName = []
		self.tempTable = []

		self.tempTableName.append(tableName)
		self.tempTable.append(df)



	def create_region_table(self, pageRange, columnNames, tableName, cordN, cordS, cordE, cordW):
		"""
		Turn a list of pages from pdf into pandas dataframe and add to current list of pages

		:param path: <str> string literal of location of pdf
		:param pageRange: <list> pages that hold current table
		:param tableName: <str> string literal of name of table. Will be used as sheet name
		:param currentBase: <list> List of all tables currently created
		:return: List including newly created table
		"""

		cords = [cordN, cordW, cordS, cordE]
		cords = [float(i) for i in cords]
		
		# Turn table into pandas data frames
		# df = tabula.read_pdf('C:/Users/adkija/Desktop/RatingTables/PermGen.pdf', encoding = 'latin1', pages = [31], area = [[260.0,50.0,440.0,500.0]] )
		df = tabula.read_pdf(self.path, encoding = 'latin1', pages = pageRange, area = [cords])
			
		if columnNames != ['']:
			df.columns = columnNames

		self.tempTableName = []
		self.tempTable = []

		self.tempTableName.append(tableName)
		self.tempTable.append(df)


	def add_table(self):
		self.allTables.append(self.tempTable.pop())
		self.tableNames.append(self.tempTableName.pop())


	def reset_tables(self):
		self.allTables = []
		self.tableNames = []


	def create_file(self):
		newFile = self.path.replace('.pdf', '.xlsx')
		writer = pd.ExcelWriter(newFile)

		for i in range(len(self.tableNames)):
			self.allTables[i].to_excel(writer, self.tableNames[i], index = False)



		writer.save()