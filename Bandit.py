from TableCreator import TableCreator
from ViewWindow import DemoWindow
from CanvasWindow import CanvasWindow

from tkinter import Tk, Label, Button, Entry, Text, Checkbutton, IntVar, filedialog, messagebox, Frame, Toplevel, StringVar, DISABLED, NORMAL, END, N, E, S, W
from pandastable import Table, TableModel
import pandas as pd

import time
import os



class MainWindow():
	def __init__(self, master):
		self.master = master
		self.TC = TableCreator()
		master.title("RateBook Bandit")

		self.pdf_path = ''
		
		self.entered_range = ''
		self.entered_table_name = ''
		self.entered_region_north = StringVar()
		self.entered_region_south = StringVar()
		self.entered_region_east = StringVar()
		self.entered_region_west = StringVar()

		self.table_count = 0
		self.table_count_text = StringVar()
		self.table_count_text.set(str(self.table_count))
		self.table_count_label = Label(master, textvariable = self.table_count_text)


		self.table_status = ''
		self.status_text = StringVar()
		self.status_text.set(self.table_status)
		self.status_label = Label(master, textvariable=self.status_text)

		self.pushRowVar = IntVar()

		#######################
		# DEFINE VALIDATORS
		#######################
		range_validator = master.register(self.validate_range)
		name_validator = master.register(self.validate_table_name)
		region_north_validator = master.register(self.validate_region_north)
		region_south_validator = master.register(self.validate_region_south)
		region_east_validator = master.register(self.validate_region_east)
		region_west_validator = master.register(self.validate_region_west)

		#######################
		# DEFINE BUTTONS
		#######################
		self.select_file_button = Button(master, text = 'Select Filing', command = self.load_file)
		self.view_demo_window_button = Button(master, text = 'View Sample', command = self.view_demo_window, state = DISABLED)
		self.create_table_button = Button(master, text = 'Create Table', command = self.create_table, state = DISABLED)
		self.create_region_table_button = Button(master, text = 'Create Regioned Table', command = self.create_canvas_window, state = DISABLED)
		self.add_table_button = Button(master, text = 'Add Table', command = self.add_table, state = DISABLED)
		self.create_book_button = Button(master, text = 'Print Rate Book', command = self.print_book, state = DISABLED)
		self.reset_button = Button(master, text = 'Reset Book', command = self.reset_book, state = DISABLED)
		self.push_row_button = Checkbutton(master, text = 'Push Row Down', variable = self.pushRowVar)
		# self.remove_blank_columns = Checkbutton(master, text = 'Remove Blank Columns', variable = self.removeBlanks)

		#######################
		# DEFINE TEXT ENTRIES
		#######################
		self.page_range_entry = Entry(master, validate = 'key', validatecommand = (range_validator, '%P'), state = DISABLED)
		self.column_name_entry = Entry(master, state = DISABLED)
		self.table_name_entry = Entry(master, validate = 'key', validatecommand = (name_validator, '%P'), state = DISABLED)
		self.region_north_entry = Entry(master, validate = 'key', validatecommand = (region_north_validator, '%P'), state = DISABLED)
		self.region_south_entry = Entry(master, validate = 'key', validatecommand = (region_south_validator, '%P'), state = DISABLED)
		self.region_east_entry = Entry(master, validate = 'key', validatecommand = (region_east_validator, '%P'), state = DISABLED)
		self.region_west_entry = Entry(master, validate = 'key', validatecommand = (region_west_validator, '%P'), state = DISABLED)

		########################
		# DEFINE LABELS
		########################
		self.page_range_label = Label(master, text = 'Page Range: 10-15')
		self.column_name_label = Label(master, text = 'Column Names: Age, Gender')
		self.table_name_label = Label(master, text = 'Table Name: Driver Points')



		########################
		# ADD WIDETS
		########################
		self.select_file_button.grid(row = 0, column = 0, sticky=W+E)
		self.view_demo_window_button.grid(row = 0, column = 5, sticky=W+E)
		self.push_row_button.grid(row = 0, column = 6)
		self.create_table_button.grid(row = 2, column = 0, sticky=W+E)
		self.create_region_table_button.grid(row = 3, column = 0, sticky = W+E)
		self.status_label.grid(row = 4, column = 0, sticky = W+E)
		self.add_table_button.grid(row = 5, column = 0, sticky=W+E)
		self.create_book_button.grid(row = 6, column = 0, sticky = W+E)
		self.table_count_label.grid(row = 6, column = 1, sticky = W+E)
		self.reset_button.grid(row = 6, column = 2, sticky = W+E)

		self.page_range_label.grid(row = 1, column = 1, columnspan = 2, sticky = W+E)
		self.column_name_label.grid(row = 2, column = 1, columnspan = 2, sticky = W+E)
		self.table_name_label.grid(row = 3, column = 1, columnspan = 2, sticky = W+E)
		self.page_range_entry.grid(row = 1, column = 3, columnspan = 4, sticky = W+E)
		self.column_name_entry.grid(row = 2, column = 3, columnspan = 4, sticky = W+E)
		self.table_name_entry.grid(row = 3, column = 3, columnspan = 4, sticky = W+E)



	def load_file(self):
		self.pdf_path = filedialog.askopenfilename(filetypes = [("Pdf files", "*.pdf")])
		self.TC.path = self.pdf_path
		self.select_file_button.configure(state = DISABLED)
		self.page_range_entry.configure(state = NORMAL)
		self.column_name_entry.configure(state = NORMAL)
		self.create_table_button.configure(state = NORMAL)
		self.table_name_entry.configure(state = NORMAL)
		self.region_north_entry.configure(state = NORMAL)
		self.region_south_entry.configure(state = NORMAL)
		self.region_east_entry.configure(state = NORMAL)
		self.region_west_entry.configure(state = NORMAL)
		self.create_region_table_button.configure(state = NORMAL)



	def create_table(self):
		try:
			self.status_text.set(self.table_status)
			self.TC.create_table(self.entered_range, self.column_name_entry.get().split(', '), self.table_name_entry.get(), self.pushRowVar.get())
			self.add_table_button.configure(state = NORMAL)
			self.view_demo_window_button.configure(state = NORMAL)
			self.table_status = 'Success!'
			self.status_text.set(self.table_status)
		except ValueError:
			self.table_status = 'Incorrect Number of Columns!'
			self.status_text.set(self.table_status)
		except AttributeError:
			self.table_status = 'No Columns Found!'
			self.status_text.set(self.table_status)
		except Exception as e:
			self.table_status = f'{e} Please report error to Adkin'
			self.status_text.set(self.table_status)

	def create_region_table(self):
		try:
			self.status_text.set(self.table_status)

			self.TC.create_region_table(self.entered_range, self.column_name_entry.get().split(', '), self.table_name_entry.get(),
									self.region_north_entry.get(), self.region_south_entry.get(),
									self.region_east_entry.get(), self.region_west_entry.get())
				
			self.add_table_button.configure(state = NORMAL)
			self.view_demo_window_button.configure(state = NORMAL)
			self.table_status = 'Success!'
			self.status_text.set(self.table_status)
		except Exception as e:
			self.table_status = f'{e} Please report error to Adkin'
			self.status_text.set(self.table_status)


	def create_canvas_window(self):

		self.top = Toplevel(self.master)
		self.top.title("Select Region")
		self.appC = CanvasWindow(self.top, self.entered_region_north, self.entered_region_south,
			self.entered_region_east, self.entered_region_west, self.pdf_path, int(self.entered_range))

		self.master.wait_window(self.top)

		
		self.TC.create_region_table(self.entered_range, self.column_name_entry.get().split(', '), self.table_name_entry.get(),
									str(self.entered_region_north.get()), str(self.entered_region_south.get()),
									str(self.entered_region_east.get()), str(self.entered_region_west.get()))
		self.add_table_button.configure(state = NORMAL)
		self.view_demo_window_button.configure(state = NORMAL)
		self.table_status = 'Success!'
		self.status_text.set(self.table_status)




	def add_table(self):
		try:
			self.TC.add_table()
			self.create_book_button.configure(state = NORMAL)
			self.add_table_button.configure(state = DISABLED)
			self.view_demo_window_button.configure(state = DISABLED)
			self.reset_button.configure(state = NORMAL)
			self.page_range_entry.delete(0, 'end')
			self.column_name_entry.delete(0, 'end')
			self.table_name_entry.delete(0, 'end')
			self.table_count = self.table_count + 1
			self.table_count_text.set(str(self.table_count))
			self.table_status = 'Added.'
			self.status_text.set(self.table_status)

		except Exception as e:
			self.table_status = f'{e} Please report error to Adkin'
			self.status_text.set(self.table_status)



	def view_demo_window(self):
		self.newWindow = Toplevel(self.master)
		self.app = DemoWindow(self.newWindow, self.TC.tempTable[0])

	def reset_book(self):
		try:
			self.page_range_entry.delete(0, 'end')
			self.column_name_entry.delete(0, 'end')
			self.table_name_entry.delete(0, 'end')
			self.TC.reset_tables()
			self.reset_button.configure(state = DISABLED)
			self.table_count = 0
			self.table_count_text.set(str(self.table_count))
			self.table_status = 'Successful Reset.'
			self.status_text.set(self.table_status)
		except Exception as e:
			self.table_status = f'{e} Please report error to Adkin'
			self.status_text.set(self.table_status)




	def print_book(self):
		try:
			self.TC.create_file()
			messagebox.showinfo("Message", "Table was created successfully!")
			self.master.destroy()
		except Exception as e:
			self.table_status = f'{e} Please report error to Adkin'
			self.status_text.set(self.table_status)

	# Validate that page range is either int or '-', only 1 '-' and first character is not '-'
	def validate_range(self, new_text):
		ops = ['-'] + [str(i) for i in range(10)]

		if not new_text: # the field is being cleared
			self.entered_range = ''
			return True

		if set(new_text).issubset(ops) and new_text.count('-') <= 1 and new_text[0] != '-':
			self.entered_range = new_text
			return True
		else:
			return False

	def validate_table_name(self, new_text):
		if not new_text:
			self.entered_table_name = ''
			return True

		if new_text[0] != ' ':
			self.entered_table_name = new_text
			return True
		else:
			return False

	def validate_region_north(self, new_text):
		ops = ['.'] + [str(i) for i in range(10)]

		if not new_text:
			self.entered_region_north = ''
			return True

		if set(new_text).issubset(ops) and new_text.count('.') <= 1:
			self.entered_region_north = new_text
			return True
		else:
			return False

	def validate_region_south(self, new_text):
		ops = ['.'] + [str(i) for i in range(10)]

		if not new_text:
			self.entered_region_south = ''
			return True

		if set(new_text).issubset(ops) and new_text.count('.') <= 1:
			self.entered_region_south = new_text
			return True
		else:
			return False

	def validate_region_east(self, new_text):
		ops = ['.'] + [str(i) for i in range(10)]

		if not new_text:
			self.entered_region_east = ''
			return True

		if set(new_text).issubset(ops) and new_text.count('.') <= 1:
			self.entered_region_east = new_text
			return True
		else:
			return False

	def validate_region_west(self, new_text):
		ops = ['.'] + [str(i) for i in range(10)]

		if not new_text:
			self.entered_region_west = ''
			return True

		if set(new_text).issubset(ops) and new_text.count('.') <= 1:
			self.entered_region_west = new_text
			return True
		else:
			return False


root = Tk()
my_gui = MainWindow(root)
root.mainloop()