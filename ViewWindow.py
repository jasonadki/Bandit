from tkinter import Frame
from pandastable import Table


class DemoWindow():
	def __init__(self, master, sampleDf):
		self.master = master
		self.sampleDf = sampleDf
		self.frame = Frame(self.master)
		self.frame.pack()

		self.table = pt = Table(self.frame, dataframe = sampleDf, showstatusbar = True)
		pt.show()