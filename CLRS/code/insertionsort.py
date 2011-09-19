#!/usr/bin/env python2
import os
import time
import threading
import wx

def thread_order(buttons):
	elements = buttons
	for idx, item in enumerate(elements):
		if idx == 0:
			continue
		print "start order %d" % idx
		split_num = -1
		for i in range(idx):
			print "    compare to %d" % i
			if item.val() < elements[i].val():
				split_num = i
				break
		if split_num < 0:
			continue

		for j in range(idx, i, -1):
			elements[j] = elements[j-1]
			elements[j].setIdx(j)
		elements[i] = item
		elements[i].setIdx(i)

class COrderElement(wx.Button):
	def __init__(self, par, val, idx, scale):
		self.__val = val
		self.__idx = idx
		self.__scale = scale
		wx.Button.__init__(self, par, -1, "",
			pos=(idx * scale[0], 0),
			size=(scale[0], scale[1] * val))

	def val(self):
		return self.__val

	def setIdx(self, idx):
		oriIdx = self.__idx
		newIdx = idx
		oriPos = self.GetPosition()
		newPos = (newIdx * self.__scale[0], 0)

		direction = 1
		if oriPos[0] > newPos[0]:
			direction = -1
		for i in range(oriPos[0], newPos[0] + direction, direction):
			time.sleep(0.05)
			self.SetPosition((i, newPos[1]))

		self.__idx = idx
		self.SetPosition((self.__idx * self.__scale[0], 0))


class MainWindow(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(400,300))
		# self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
		# A StatusBar in the bottom of the window
		self.CreateStatusBar()

		# Setting up the menu.
		filemenu= wx.Menu()

		# wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
		menuAbout = filemenu.Append(wx.ID_ABOUT, "&About",
			" Information about this program")
		menuExit = filemenu.Append(wx.ID_EXIT,"E&xit",
			" Terminate the program")

		# Creating the menubar.
		menuBar = wx.MenuBar()
		# Adding the "filemenu" to the MenuBar
		menuBar.Append(filemenu,"&File")
		# Adding the MenuBar to the Frame content.
		self.SetMenuBar(menuBar)

		# Set events.
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

		self.InitOrderElements()

		self.Show(True)

	def OnAbout(self,e):
		# A message dialog box with an OK button.
		# wx.OK is a standard ID in wxWidgets.
		dlg = wx.MessageDialog( self, "A small text editor",
			"About Sample Editor", wx.OK)
		dlg.ShowModal() # Show it
		dlg.Destroy() # finally destroy it when finished.

		self.__threads=[]
		self.__threads.append(threading.Thread(target=thread_order, args=(self.__orderElements,)))

		for x in self.__threads:
			x.start()

	def OnExit(self,e):
		for x in self.__threads:
			x.join()
		self.Close(True)  # Close the frame.

	def InitOrderElements(self):
		# buttons
		to_order_data = [ 3, 1, 4, 10, 8, 6, 2, 5, 9 ]
		self.__orderElements = []
		for idx, val in enumerate(to_order_data):
			self.__orderElements.append(COrderElement(self,
				val, idx, (20, 20)))

app = wx.App(False)
frame = MainWindow(None, "Sample editor")
app.MainLoop()

