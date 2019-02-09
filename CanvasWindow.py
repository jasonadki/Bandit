from tkinter import Tk, Frame, N, S, W, E, Canvas, INSERT
import PIL.Image
from PIL import Image, ImageTk

from pdf2image import convert_from_path

from PyPDF2 import PdfFileReader


class CanvasWindow():
	def __init__(self, master, north, south, east, west, pdf_path, page_number):
		
		self.master = master
		self.north = north
		self.south = south
		self.east = east
		self.west = west
		self.pdfPath = pdf_path
		self.pageNumber = page_number

		self.frame = Frame(self.master)


		####################
		# DRAWING VARIABLES
		####################
		self.x = self.y = 0
		self.rect = None
		self.start_x = None
		self.start_y = None



		# Get pdf file size 612, 792
		self.w, self.h = PdfFileReader(open(self.pdfPath, 'rb')).getPage(self.pageNumber-1).mediaBox[2:]



		######################
		# CREATE BLANK CANVAS
		######################
		self.canvas = Canvas(self.master,  cursor="cross", height = self.h, width = self.w)
		self.canvas.grid(row=0,column=0,sticky=N+S+E+W)


		###########################
		# BIND FUNCTIONS TO CANVAS
		###########################
		self.canvas.bind("<ButtonPress-1>", self.on_button_press)
		self.canvas.bind("<B1-Motion>", self.on_move_press)
		self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

		



		self.im = convert_from_path(pdf_path = self.pdfPath, dpi = 500, first_page = self.pageNumber, last_page = self.pageNumber)[0]

		self.im = self.im.resize((self.w, self.h))
		self.wazil, self.lard = self.im.size
		self.canvas.config(scrollregion=(0, 0, self.wazil, self.lard))
		self.tk_im = ImageTk.PhotoImage(self.im)
		self.canvas.create_image(0, 0, anchor="nw", image=self.tk_im)







	def on_button_press(self, event):
		# save mouse drag start position, cannot be less than 0
		self.start_x = max(0, self.canvas.canvasx(event.x))
		self.start_y = max(0, self.canvas.canvasy(event.y))

		# create rectangle if not yet exist
		if not self.rect:
			self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='red')

	def on_move_press(self, event):
		
		curX = self.canvas.canvasx(event.x)
		curY = self.canvas.canvasy(event.y)

		# expand rectangle as you drag the mouse
		self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)   


	def on_button_release(self, event):

		self.north.set(max(0, min(int(self.start_y), event.y)))
		self.south.set(min(self.h, max(int(self.start_y), event.y)))
		self.east.set(min(self.w, max(int(self.start_x), event.x)))
		self.west.set(max(0, min(int(self.start_x), event.x)))

		self.master.destroy()

		print('-------------------------------------------')
		pass