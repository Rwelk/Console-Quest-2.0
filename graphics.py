# graphics.py
	# Simple object oriented graphics library

	# The library is designed to make it very easy for novice programmers to
	# experiment with computer graphics in an object oriented fashion. It is
	# written by John Zelle for use with the book "Python Programming: An
	# Introduction to Computer Science" (Franklin, Beedle & Associates).

	# LICENSE: This is open-source software released under the terms of the
	# GPL (http://www.gnu.org/licenses/gpl.html).

	# PLATFORMS: The package is a wrapper around Tkinter and should run on
	# any platform where Tkinter is available.

	# INSTALLATION: Put this file somewhere where Python can see it.

	# OVERVIEW: There are two kinds of objects in the library. The GraphWin
	# class implements a window where drawing can be done and various
	# GraphicsObjects are provided that can be drawn into a GraphWin. As a
	# simple example, here is a complete program to draw a circle of radius
	# 10 centered in a 100x100 window:

	# --------------------------------------------------------------------
	# from graphics import *

	# def main():
	#	 win = GraphWin("My Circle", 100, 100)
	#	 c = Circle(Point(50,50), 10)
	#	 c.draw(win)
	#	 win.getMouse() # Pause to view result
	#	 win.close()	# Close window when done

	# main()
	# --------------------------------------------------------------------
	# GraphWin objects support coordinate transformation through the
	# setCoords method and mouse and keyboard interaction methods.

	# The library provides the following graphical objects:
	#	 Point
	#	 Line
	#	 Circle
	#	 Oval
	#	 Rectangle
	#	 Polygon
	#	 Text
	#	 Entry (for text-based input)
	#	 Image

	# Various attributes of graphical objects can be set such as
	# outline-color, fill-color and line-width. Graphical objects also
	# support moving and hiding for animation effects.

	# The library also provides a very simple class for pixel-based image
	# manipulation, Pixmap. A pixmap can be loaded from a file and displayed
	# using an Image object. Both getPixel and setPixel methods are provided
	# for manipulating the image.

	# DOCUMENTATION: For complete documentation, see Chapter 4 of "Python
	# Programming: An Introduction to Computer Science" by John Zelle,
	# published by Franklin, Beedle & Associates.  Also see
	# http://mcsp.wartburg.edu/zelle/python for a quick reference

__version__ = "5.0beta"

	# Version 5
	#	 * update at bottom to fix MacOS issue causing askopenfile() to hang
	#	 * update takes an optional parameter specifying update rate
	#	 * Entry objects get focus when drawn
	#	 * __repr_ for all objects
	#	 * fixed offset problem in window, made canvas borderless

	# Version 4.3 4/25/2014
	#	 * Fixed Image getPixel to work with Python 3.4, TK 8.6 (tuple type handling)
	#	 * Added interactive keyboard input (getKey and checkKey) to GraphWin
	#	 * Modified setCoords to cause redraw of current objects, thus
	#	   changing the view. This supports scrolling around via setCoords.
	#
	# Version 4.2 5/26/2011
	#	 * Modified Image to allow multiple undraws like other GraphicsObjects
	# Version 4.1 12/29/2009
	#	 * Merged Pixmap and Image class. Old Pixmap removed, use Image.
	# Version 4.0.1 10/08/2009
	#	 * Modified the autoflush on GraphWin to default to True
	#	 * Autoflush check on close, setBackground
	#	 * Fixed getMouse to flush pending clicks at entry
	# Version 4.0 08/2009
	#	 * Reverted to non-threaded version. The advantages (robustness,
	#		 efficiency, ability to use with other Tk code, etc.) outweigh
	#		 the disadvantage that interactive use with IDLE is slightly more
	#		 cumbersome.
	#	 * Modified to run in either Python 2.x or 3.x (same file).
	#	 * Added Image.getPixmap()
	#	 * Added update() -- stand alone function to cause any pending
	#		   graphics changes to display.
	#
	# Version 3.4 10/16/07
	#	 Fixed GraphicsError to avoid "exploded" error messages.
	# Version 3.3 8/8/06
	#	 Added checkMouse method to GraphWin
	# Version 3.2.3
	#	 Fixed error in Polygon init spotted by Andrew Harrington
	#	 Fixed improper threading in Image constructor
	# Version 3.2.2 5/30/05
	#	 Cleaned up handling of exceptions in Tk thread. The graphics package
	#	 now raises an exception if attempt is made to communicate with
	#	 a dead Tk thread.
	# Version 3.2.1 5/22/05
	#	 Added shutdown function for tk thread to eliminate race-condition
	#		error "chatter" when main thread terminates
	#	 Renamed various private globals with _
	# Version 3.2 5/4/05
	#	 Added Pixmap object for simple image manipulation.
	# Version 3.1 4/13/05
	#	 Improved the Tk thread communication so that most Tk calls
	#		do not have to wait for synchonization with the Tk thread.
	#		(see _tkCall and _tkExec)
	# Version 3.0 12/30/04
	#	 Implemented Tk event loop in separate thread. Should now work
	#		interactively with IDLE. Undocumented autoflush feature is
	#		no longer necessary. Its default is now False (off). It may
	#		be removed in a future version.
	#	 Better handling of errors regarding operations on windows that
	#	   have been closed.
	#	 Addition of an isClosed method to GraphWindow class.

	# Version 2.2 8/26/04
	#	 Fixed cloning bug reported by Joseph Oldham.
	#	 Now implements deep copy of config info.
	# Version 2.1 1/15/04
	#	 Added autoflush option to GraphWin. When True (default) updates on
	#		the window are done after each action. This makes some graphics
	#		intensive programs sluggish. Turning off autoflush causes updates
	#		to happen during idle periods or when flush is called.
	# Version 2.0
	#	 Updated Documentation
	#	 Made Polygon accept a list of Points in constructor
	#	 Made all drawing functions call TK update for easier animations
	#		  and to make the overall package work better with
	#		  Python 2.3 and IDLE 1.0 under Windows (still some issues).
	#	 Removed vestigial turtle graphics.
	#	 Added ability to configure font for Entry objects (analogous to Text)
	#	 Added setTextColor for Text as an alias of setFill
	#	 Changed to class-style exceptions
	#	 Fixed cloning of Text objects

	# Version 1.6
	#	 Fixed Entry so StringVar uses _root as master, solves weird
	#			interaction with shell in Idle
	#	 Fixed bug in setCoords. X and Y coordinates can increase in
	#		   "non-intuitive" direction.
	#	 Tweaked wm_protocol so window is not resizable and kill box closes.

	# Version 1.5
	#	 Fixed bug in Entry. Can now define entry before creating a
	#	 GraphWin. All GraphWins are now toplevel windows and share
	#	 a fixed root (called _root).

	# Version 1.4
	#	 Fixed Garbage collection of Tkinter images bug.
	#	 Added ability to set text atttributes.
	#	 Added Entry boxes.

import time, os

try:  # import as appropriate for 2.x vs. 3.x
   import tkinter as tk
except:
   import Tkinter as tk


##########################################################################
# Module Exceptions

class GraphicsError(Exception):
	"""Generic error class for graphics module exceptions."""
	pass
	
UNSUPPORTED_METHOD = "Object doesn't support operation"
BAD_OPTION = "Illegal option value"

##########################################################################
# global variables and funtions

_root = tk.Tk()
_root.withdraw()

_update_lasttime = time.time()

def update(rate=None):
	global _update_lasttime
	if rate:
		now = time.time()
		pauseLength = 1/rate-(now-_update_lasttime)
		if pauseLength > 0:
			time.sleep(pauseLength)
			_update_lasttime = now + pauseLength
		else:
			_update_lasttime = now

	_root.update()

############################################################################
# Graphics classes start here

class GraphWin(tk.Canvas):

	"""A GraphWin is a toplevel window for displaying graphics."""

	def __init__(self, title="Graphics Window",
				 width=200, height=200, autoflush=True):
		assert type(title) == type(""), "Title must be a string"
		master = tk.Toplevel(_root)
		master.protocol("WM_DELETE_WINDOW", self.close)
		tk.Canvas.__init__(self, master, width=width, height=height,
						   highlightthickness=0, bd=0)
		self.master.title(title)
		self.pack()
		master.resizable(0,0)
		self.foreground = "black"
		self.items = []
		self.mouseX = None
		self.mouseY = None
		self.bind("<Button-1>", self._onClick)
		self.bind("<Motion>", self._mousemotion)
		self.bind("<ButtonRelease-1>", self._mouserelease)
		self.clicked = False
		self.bind_all("<Key>", self._onKey)
		self.height = int(height)
		self.width = int(width)
		self.autoflush = autoflush
		self._mouseCallback = None
		self.trans = None
		self.closed = False
		master.lift()
		self.lastKey = ""
		if autoflush: _root.update()

	def __repr__(self):
		if self.isClosed():
			return "<Closed GraphWin>"
		else:
			return "GraphWin('{}', {}, {})".format(self.master.title(),
											 self.getWidth(),
											 self.getHeight())

	def __str__(self):
		return repr(self)

	def __checkOpen(self):
		if self.closed:
			raise GraphicsError("window is closed")

	def _onKey(self, evnt):
		self.lastKey = evnt.keysym

	def _onClick(self, e):
		self.mouseX = e.x
		self.mouseY = e.y
		self.clicked = True
		if self._mouseCallback:
			self._mouseCallback(Point(e.x, e.y))

	def _mousemotion(self, e):
		'''Callback for mouse motion in the GUI.'''
		if self.clicked:
			self.mouseX = e.x
			self.mouseY = e.y

	def _mouserelease(self, e):
		'''Callback for releasing a mouse click.'''
		self.clicked = False
		self.mouseX = None
		self.mouseY = None


	def setBackground(self, color):
		"""Set background color of the window"""
		self.__checkOpen()
		self.config(bg=color)
		self.__autoflush()

	def setCoords(self, x1, y1, x2, y2):
		"""Set coordinates of window to run from (x1,y1) in the
		lower-left corner to (x2,y2) in the upper-right corner."""
		self.trans = Transform(self.width, self.height, x1, y1, x2, y2)
		self.redraw()

	def close(self):
		"""Close the window"""

		if self.closed: return
		self.closed = True
		self.master.destroy()
		self.__autoflush()


	def isClosed(self):
		return self.closed


	def isOpen(self):
		return not self.closed


	def __autoflush(self):
		if self.autoflush:
			_root.update()


	def plot(self, x, y, color="black"):
		"""Set pixel (x,y) to the given color"""
		self.__checkOpen()
		xs,ys = self.toScreen(x,y)
		self.create_line(xs,ys,xs+1,ys, fill=color)
		self.__autoflush()

	def plotPixel(self, x, y, color="black"):
		"""Set pixel raw (independent of window coordinates) pixel
		(x,y) to color"""
		self.__checkOpen()
		self.create_line(x,y,x+1,y, fill=color)
		self.__autoflush()

	def flush(self):
		"""Update drawing to the window"""
		self.__checkOpen()
		self.update_idletasks()

	def getMouse(self):
		"""Wait for mouse click and return Point object representing
		the click"""
		self.update()	  # flush any prior clicks
		self.mouseX = None
		self.mouseY = None
		while self.mouseX == None or self.mouseY == None:
			self.update()
			if self.isClosed(): raise GraphicsError("getMouse in closed window")
			time.sleep(.1) # give up thread
		x,y = self.toWorld(self.mouseX, self.mouseY)
		self.mouseX = None
		self.mouseY = None
		return Point(x,y)

	def checkMouse(self):
		"""Return last mouse click or None if mouse has
		not been clicked since last call"""
		if self.isClosed():
			raise GraphicsError("checkMouse in closed window")
		self.update()
		if self.mouseX != None and self.mouseY != None:
			x,y = self.toWorld(self.mouseX, self.mouseY)
			self.mouseX = None
			self.mouseY = None
			return Point(x,y)
		else:
			return None

	def getKey(self):
		"""Wait for user to press a key and return it as a string."""
		self.lastKey = ""
		while self.lastKey == "":
			self.update()
			if self.isClosed(): raise GraphicsError("getKey in closed window")
			time.sleep(.1) # give up thread

		key = self.lastKey
		self.lastKey = ""
		return key

	def checkKey(self):
		"""Return last key pressed or None if no key pressed since last call"""
		if self.isClosed():
			raise GraphicsError("checkKey in closed window")
		self.update()
		key = self.lastKey
		self.lastKey = ""
		return key

	def getHeight(self):
		"""Return the height of the window"""
		return self.height

	def getWidth(self):
		"""Return the width of the window"""
		return self.width

	def toScreen(self, x, y):
		trans = self.trans
		if trans:
			return self.trans.screen(x,y)
		else:
			return x,y

	def toWorld(self, x, y):
		trans = self.trans
		if trans:
			return self.trans.world(x,y)
		else:
			return x,y

	def setMouseHandler(self, func):
		self._mouseCallback = func

	def addItem(self, item):
		self.items.append(item)

	def delItem(self, item):
		self.items.remove(item)

	def redraw(self):
		hide = Rectangle(Point(-5, -5), Point(self.width + 1, self.height + 1))
		hide.draw(self)
		for item in self.items[:]:
			item.undraw()
			item.draw(self)
			hide.lift()
		
		hide.undraw()
		self.update()

	def clear(self, start=0):
		for item in self.items[start:]:
			item.undraw()



class Transform:

	"""Internal class for 2-D coordinate transformations"""

	def __init__(self, w, h, xlow, ylow, xhigh, yhigh):
		# w, h are width and height of window
		# (xlow,ylow) coordinates of lower-left [raw (0,h-1)]
		# (xhigh,yhigh) coordinates of upper-right [raw (w-1,0)]
		xspan = (xhigh-xlow)
		yspan = (yhigh-ylow)
		self.xbase = xlow
		self.ybase = yhigh
		self.xscale = xspan/float(w-1)
		self.yscale = yspan/float(h-1)

	def screen(self,x,y):
		# Returns x,y in screen (actually window) coordinates
		xs = (x-self.xbase) / self.xscale
		ys = (self.ybase-y) / self.yscale
		return int(xs+0.5),int(ys+0.5)

	def world(self,xs,ys):
		# Returns xs,ys in world coordinates
		x = xs*self.xscale + self.xbase
		y = self.ybase - ys*self.yscale
		return x,y


# Default values for various item configuration options. Only a subset of
#   keys may be present in the configuration dictionary for a given item
DEFAULT_CONFIG = {"fill":"",
	"outline":"black",
	"width":"1",
	"arrow":"none",
	"text":"",
	"anchor":"w",
	"justify":"left",
	"font": ("courier", 20, "normal")}

class GraphicsObject:

	"""Generic base class for all of the drawable objects"""
	# A subclass of GraphicsObject should override _draw and
	#   and _move methods.

	def __init__(self, options):
		# options is a list of strings indicating which options are
		# legal for this object.

		# When an object is drawn, canvas is set to the GraphWin(canvas)
		#	object where it is drawn and id is the TK identifier of the
		#	drawn shape.
		self.canvas = None
		self.id = None

		# config is the dictionary of configuration options for the widget.
		config = {}
		for option in options:
			config[option] = DEFAULT_CONFIG[option]
		self.config = config

	def setFill(self, color):
		"""Set interior color to color"""
		self._reconfig("fill", color)

	def setOutline(self, color):
		"""Set outline color to color"""
		self._reconfig("outline", color)

	def setWidth(self, width):
		"""Set line weight to width"""
		self._reconfig("width", width)

	def draw(self, graphwin):

		"""Draw the object in graphwin, which should be a GraphWin
		object.  A GraphicsObject may only be drawn into one
		window. Returns silently if the object is already drawn."""

		if self.canvas and not self.canvas.isClosed(): return
		if graphwin.isClosed(): raise GraphicsError("Can't draw to closed window")
		self.canvas = graphwin

		self.id = self._draw(graphwin, self.config)
		graphwin.addItem(self)		
		if graphwin.autoflush:
			_root.update()
		
		return self


	def undraw(self):

		"""Undraw the object (i.e. hide it). Returns silently if the
		object is not currently drawn."""

		if not self.canvas: return
		if not self.canvas.isClosed():
			self.canvas.delete(self.id)
			self.canvas.delItem(self)
			if self.canvas.autoflush:
				_root.update()
		self.canvas = None
		self.id = None


	def move(self, dx, dy):

		"""move object dx units in x direction and dy units in y
		direction"""

		self._move(dx,dy)
		canvas = self.canvas
		if canvas and not canvas.isClosed():
			trans = canvas.trans

			if trans:
				x = dx/ trans.xscale
				y = -dy / trans.yscale
			else:
				x = dx
				y = dy


			self.canvas.move(self.id, x, y)

			if canvas.autoflush:
				_root.update()

	def lower(self, item=None):

		canvas = self.canvas
		if canvas and not canvas.isClosed():
			
			if item:
				self.canvas.lower(self.id, item.id)
			else:
				self.canvas.lower(self.id)

			if canvas.autoflush:
				_root.update()

	def lift(self, item=None):

		canvas = self.canvas
		if canvas and not canvas.isClosed():
			
			if item:
				self.canvas.lift(self.id, item.id)
			else:
				self.canvas.lift(self.id)

			if canvas.autoflush:
				_root.update()

	def _reconfig(self, option, setting):
		# Internal method for changing configuration of the object
		# Raises an error if the option does not exist in the config
		#	dictionary for this object
		if option not in self.config:
			raise GraphicsError(UNSUPPORTED_METHOD)
		options = self.config
		options[option] = setting
		if self.canvas and not self.canvas.isClosed():
			self.canvas.itemconfig(self.id, options)
			if self.canvas.autoflush:
				_root.update()


	def _draw(self, canvas, options):
		"""draws appropriate figure on canvas with options provided
		Returns Tk id of item drawn"""
		pass # must override in subclass


	def _move(self, dx, dy):
		"""updates internal state of object to move it dx,dy units"""
		pass # must override in subclass

class Point(GraphicsObject):
	def __init__(self, x, y):
		GraphicsObject.__init__(self, ["outline", "fill"])
		self.setFill = self.setOutline
		self.x = float(x)
		self.y = float(y)

	def __repr__(self):
		return "Point({}, {})".format(self.x, self.y)

	def _draw(self, canvas, options):
		x,y = canvas.toScreen(self.x,self.y)
		return canvas.create_rectangle(x,y,x+1,y+1,options)

	def _move(self, dx, dy):
		self.x = self.x + dx
		self.y = self.y + dy

	def clone(self):
		other = Point(self.x,self.y)
		other.config = self.config.copy()
		return other

	def getX(self): return self.x
	def getY(self): return self.y

class _BBox(GraphicsObject):
	# Internal base class for objects represented by bounding box
	# (opposite corners) Line segment is a degenerate case.

	def __init__(self, p1, p2, options=["outline","width","fill"]):
		GraphicsObject.__init__(self, options)
		self.p1 = p1.clone()
		self.p2 = p2.clone()

	def _move(self, dx, dy):
		self.p1.x = self.p1.x + dx
		self.p1.y = self.p1.y + dy
		self.p2.x = self.p2.x + dx
		self.p2.y = self.p2.y  + dy

	def getP1(self): return self.p1.clone()

	def getP2(self): return self.p2.clone()

	def getCenter(self):
		p1 = self.p1
		p2 = self.p2
		return Point((p1.x+p2.x)/2.0, (p1.y+p2.y)/2.0)

class Rectangle(_BBox):

	def __init__(self, p1, p2):
		_BBox.__init__(self, p1, p2)

	def __repr__(self):
		return "Rectangle({}, {})".format(str(self.p1), str(self.p2))

	def _draw(self, canvas, options):
		p1 = self.p1
		p2 = self.p2
		x1,y1 = canvas.toScreen(p1.x,p1.y)
		x2,y2 = canvas.toScreen(p2.x,p2.y)
		return canvas.create_rectangle(x1,y1,x2,y2,options)

	def clone(self):
		other = Rectangle(self.p1, self.p2)
		other.config = self.config.copy()
		return other

class Line(_BBox):

	def __init__(self, p1, p2):
		_BBox.__init__(self, p1, p2, ["arrow","fill","width"])
		self.setFill(DEFAULT_CONFIG['outline'])
		self.setOutline = self.setFill

	def __repr__(self):
		return "Line({}, {})".format(str(self.p1), str(self.p2))

	def clone(self):
		other = Line(self.p1, self.p2)
		other.config = self.config.copy()
		return other

	def _draw(self, canvas, options):
		p1 = self.p1
		p2 = self.p2
		x1,y1 = canvas.toScreen(p1.x,p1.y)
		x2,y2 = canvas.toScreen(p2.x,p2.y)
		return canvas.create_line(x1,y1,x2,y2,options)

	def setArrow(self, option):
		if not option in ["first","last","both","none"]:
			raise GraphicsError(BAD_OPTION)
		self._reconfig("arrow", option)

class Polygon(GraphicsObject):

	def __init__(self, *points):
		# if points passed as a list, extract it
		if len(points) == 1 and type(points[0]) == type([]):
			points = points[0]
		self.points = list(map(Point.clone, points))
		GraphicsObject.__init__(self, ["outline", "width", "fill"])

	def __repr__(self):
		return "Polygon"+str(tuple(p for p in self.points))

	def clone(self):
		other = Polygon(*self.points)
		other.config = self.config.copy()
		return other

	def getPoints(self):
		return list(map(Point.clone, self.points))

	def _move(self, dx, dy):
		for p in self.points:
			p.move(dx,dy)

	def _draw(self, canvas, options):
		args = [canvas]
		for p in self.points:
			x,y = canvas.toScreen(p.x,p.y)
			args.append(x)
			args.append(y)
		args.append(options)
		return GraphWin.create_polygon(*args)

class Text(GraphicsObject):

	def __init__(self, p, text=""):
		GraphicsObject.__init__(self, ["anchor","justify","fill","text","font"])
		self.setText(text)
		self.anchor = p.clone()
		self.setFill("white")
		self.setOutline = self.setFill

	def __repr__(self):
		return "Text({}, '{}')".format(self.anchor, self.getText())

	def _draw(self, canvas, options):
		p = self.anchor
		x,y = canvas.toScreen(p.x,p.y)
		return canvas.create_text(x,y,options)

	def _move(self, dx, dy):
		self.anchor.move(dx,dy)

	def clone(self):
		other = Text(self.anchor, self.config['text'])
		other.config = self.config.copy()
		return other

	def setText(self,text):
		self._reconfig("text", text)

	def getText(self):
		return self.config["text"]

	def setFont(self, face):
		if face in ['helvetica','arial','courier','times roman']:
			f,s,b = self.config['font']
			self._reconfig("font",(face,s,b))
		else:
			raise GraphicsError(BAD_OPTION)

	def setSize(self, size):
		if 5 <= size <= 36:
			f,s,b = self.config['font']
			self._reconfig("font", (f,size,b))
		else:
			raise GraphicsError(BAD_OPTION)

	def setStyle(self, style):
		if style in ['bold','normal','italic', 'bold italic']:
			f,s,b = self.config['font']
			self._reconfig("font", (f,s,style))
		else:
			raise GraphicsError(BAD_OPTION)

	def setJustification(self,justification):
		self._reconfig("justify", justification)

	def setTextColor(self, color):
		self.setFill(color)

	def setAnchor(self, anchor):
		self._reconfig("anchor", anchor)

class Image(GraphicsObject):

	idCount = 0
	imageCache = {} # tk photoimages go here to avoid GC while drawn

	def __init__(self, p, *pixmap):
		GraphicsObject.__init__(self, ["anchor"])
		self.anchor = p.clone()
		self.imageId = Image.idCount
		Image.idCount = Image.idCount + 1
		if len(pixmap) == 1: # file name provided
			self.img = tk.PhotoImage(file=pixmap[0], master=_root)
		else: # width and height provided
			width, height = pixmap
			self.img = tk.PhotoImage(master=_root, width=width, height=height)

	def __repr__(self):
		return "Image({}, {}, {})".format(self.anchor, self.getWidth(), self.getHeight())

	def _draw(self, canvas, options):
		p = self.anchor
		x,y = canvas.toScreen(p.x,p.y)
		self.imageCache[self.imageId] = self.img # save a reference
		return canvas.create_image(x,y,image=self.img)

	def _move(self, dx, dy):
		self.anchor.move(dx,dy)

	def undraw(self):
		try:
			del self.imageCache[self.imageId]  # allow gc of tk photoimage
		except KeyError:
			pass
		GraphicsObject.undraw(self)

	def getAnchor(self):
		return self.anchor.clone()

	def clone(self):
		other = Image(Point(0,0), 0, 0)
		other.img = self.img.copy()
		other.anchor = self.anchor.clone()
		other.config = self.config.copy()
		return other

	def getWidth(self):
		"""Returns the width of the image in pixels"""
		return self.img.width()

	def getHeight(self):
		"""Returns the height of the image in pixels"""
		return self.img.height()

	def getPixel(self, x, y):
		"""Returns a list [r,g,b] with the RGB color values for pixel (x,y)
		r,g,b are in range(256)

		"""

		value = self.img.get(x,y)
		if type(value) ==  type(0):
			return [value, value, value]
		elif type(value) == type((0,0,0)):
			return list(value)
		else:
			return list(map(int, value.split()))

	def setPixel(self, x, y, color):
		"""Sets pixel (x,y) to the given color

		"""
		self.img.put("{" + color +"}", (x, y))


	def save(self, filename):
		"""Saves the pixmap image to filename.
		The format for the save image is determined from the filname extension.

		"""

		path, name = os.path.split(filename)
		ext = name.split(".")[-1]
		self.img.write( filename, format=ext)


def color_rgb(r,g,b):
	"""r,g,b are intensities of red, green, and blue in range(256)
	Returns color specifier string for the resulting color"""
	return "#%02x%02x%02x" % (r,g,b)

def test_keys():
	gw = GraphWin('Test Keys', 300)
	directions = Text(Point(150, 10), 'Press [RETURN] to exit.')
	directions.setFill('black')
	directions.setSize(12)
	directions.setAnchor('n')
	directions.draw(gw)

	txt = Text(Point(150, 100), '')
	txt.setFill('black')
	txt.setSize(12)
	txt.setAnchor('c')
	txt.draw(gw)

	while True:
		key = gw.checkKey()

		if key:
			txt.setText(key)
		
			if key == 'Return':
				time.sleep(1)
				break


def show_all_colors():
	COLORS = ['Snow', 'GhostWhite', 'WhiteSmoke', 'Gainsboro', 'FloralWhite', 'OldLace',
	'Linen', 'AntiqueWhite', 'PapayaWhip', 'BlanchedAlmond', 'Bisque', 'PeachPuff',
	'NavajoWhite', 'LemonChiffon', 'MintCream', 'Azure', 'AliceBlue', 'Lavender',
	'LavenderBlush', 'MistyRose', 'DarkSlateGray', 'DimGray', 'SlateGray',
	'LightSlateGray', 'Gray', 'LightGrey', 'MidnightBlue', 'Navy', 'CornflowerBlue', 'DarkSlateBlue',
	'SlateBlue', 'MediumSlateBlue', 'LightSlateBlue', 'MediumBlue', 'RoyalBlue',  'Blue',
	'DodgerBlue', 'DeepSkyBlue', 'SkyBlue', 'LightSkyBlue', 'SteelBlue', 'LightSteelBlue',
	'LightBlue', 'PowderBlue', 'PaleTurquoise', 'DarkTurquoise', 'MediumTurquoise', 'Turquoise',
	'Cyan', 'LightCyan', 'CadetBlue', 'MediumAquamarine', 'Aquamarine', 'DarkGreen', 'DarkOliveGreen',
	'DarkSeaGreen', 'SeaGreen', 'MediumSeaGreen', 'LightSeaGreen', 'PaleGreen', 'SpringGreen',
	'LawnGreen', 'MediumSpringGreen', 'GreenYellow', 'LimeGreen', 'YellowGreen',
	'ForestGreen', 'OliveDrab', 'DarkKhaki', 'Khaki', 'PaleGoldenrod', 'LightGoldenrodYellow',
	'LightYellow', 'Yellow', 'Gold', 'LightGoldenrod', 'Goldenrod', 'DarkGoldenrod', 'RosyBrown',
	'IndianRed', 'SaddleBrown', 'SandyBrown',
	'DarkSalmon', 'Salmon', 'LightSalmon', 'Orange', 'DarkOrange',
	'Coral', 'LightCoral', 'Tomato', 'OrangeRed', 'Red', 'HotPink', 'DeepPink', 'Pink', 'LightPink',
	'PaleVioletRed', 'Maroon', 'MediumVioletRed', 'VioletRed',
	'MediumOrchid', 'DarkOrchid', 'DarkViolet', 'BlueViolet', 'Purple', 'MediumPurple',
	'Thistle', 'Snow2', 'Snow3',
	'Snow4', 'Seashell2', 'Seashell3', 'Seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
	'AntiqueWhite3', 'AntiqueWhite4', 'Bisque2', 'Bisque3', 'Bisque4', 'PeachPuff2',
	'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
	'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'Cornsilk2', 'Cornsilk3',
	'Cornsilk4', 'Ivory2', 'Ivory3', 'Ivory4', 'Honeydew2', 'Honeydew3', 'Honeydew4',
	'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
	'MistyRose4', 'Azure2', 'Azure3', 'Azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
	'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'Blue2', 'Blue4',
	'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
	'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
	'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
	'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
	'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
	'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
	'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
	'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
	'CadetBlue4', 'Turquoise1', 'Turquoise2', 'Turquoise3', 'Turquoise4', 'Cyan2', 'Cyan3',
	'Cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
	'Aquamarine2', 'Aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
	'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
	'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
	'Green2', 'Green3', 'Green4', 'Chartreuse2', 'Chartreuse3', 'Chartreuse4',
	'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
	'DarkOliveGreen3', 'DarkOliveGreen4', 'Khaki1', 'Khaki2', 'Khaki3', 'Khaki4',
	'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
	'LightYellow2', 'LightYellow3', 'LightYellow4', 'Yellow2', 'Yellow3', 'Yellow4',
	'Gold2', 'Gold3', 'Gold4', 'Goldenrod1', 'Goldenrod2', 'Goldenrod3', 'Goldenrod4',
	'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
	'RosyBrown', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
	'IndianRed3', 'IndianRed4', 'Sienna1', 'Sienna2', 'Sienna3', 'Sienna4', 'Burlywood1',
	'Burlywood2', 'Burlywood3', 'Burlywood4', 'Wheat1', 'Wheat2', 'Wheat3', 'Wheat4', 'Tan1',
	'Tan2', 'Tan4', 'Chocolate1', 'Chocolate2', 'Chocolate3', 'Firebrick1', 'Firebrick2',
	'Firebrick3', 'Firebrick4', 'Brown1', 'Brown2', 'Brown3', 'Brown4', 'Salmon1', 'Salmon2',
	'Salmon3', 'Salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'Orange2',
	'Orange3', 'Orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
	'Coral1', 'Coral2', 'Coral3', 'Coral4', 'Tomato2', 'Tomato3', 'Tomato4', 'OrangeRed2',
	'OrangeRed3', 'OrangeRed4', 'Red2', 'Red3', 'Red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
	'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'Pink1', 'Pink2', 'Pink3', 'Pink4',
	'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
	'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'Maroon1', 'Maroon2',
	'Maroon3', 'Maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
	'Magenta2', 'Magenta3', 'Magenta4', 'Orchid1', 'Orchid2', 'Orchid3', 'Orchid4', 'Plum1',
	'Plum2', 'Plum3', 'Plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
	'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
	'Purple1', 'Purple2', 'Purple3', 'Purple4', 'MediumPurple1', 'MediumPurple2',
	'MediumPurple3', 'MediumPurple4', 'Thistle1', 'Thistle2', 'Thistle3', 'Thistle4',
	'Gray1', 'Gray2', 'Gray3', 'Gray4', 'Gray5', 'Gray6', 'Gray7', 'Gray8', 'Gray9', 'Gray10',
	'Gray11', 'Gray12', 'Gray13', 'Gray14', 'Gray15', 'Gray16', 'Gray17', 'Gray18', 'Gray19',
	'Gray20', 'Gray21', 'Gray22', 'Gray23', 'Gray24', 'Gray25', 'Gray26', 'Gray27', 'Gray28',
	'Gray29', 'Gray30', 'Gray31', 'Gray32', 'Gray33', 'Gray34', 'Gray35', 'Gray36', 'Gray37',
	'Gray38', 'Gray39', 'Gray40', 'Gray42', 'Gray43', 'Gray44', 'Gray45', 'Gray46', 'Gray47',
	'Gray48', 'Gray49', 'Gray50', 'Gray51', 'Gray52', 'Gray53', 'Gray54', 'Gray55', 'Gray56',
	'Gray57', 'Gray58', 'Gray59', 'Gray60', 'Gray61', 'Gray62', 'Gray63', 'Gray64', 'Gray65',
	'Gray66', 'Gray67', 'Gray68', 'Gray69', 'Gray70', 'Gray71', 'Gray72', 'Gray73', 'Gray74',
	'Gray75', 'Gray76', 'Gray77', 'Gray78', 'Gray79', 'Gray80', 'Gray81', 'Gray82', 'Gray83',
	'Gray84', 'Gray85', 'Gray86', 'Gray87', 'Gray88', 'Gray89', 'Gray90', 'Gray91', 'Gray92',
	'Gray93', 'Gray94', 'Gray95', 'Gray97', 'Gray98', 'Gray99', 'White', 'Black', 'Green',]

	white_text = ['MidnightBlue', 'Navy', 'MediumBlue', 'Blue', 'Blue2', 'Blue4', 'Black', 'DarkGreen', 'Green',
	'Maroon', 'Purple4', 'SlateBlue4', 'VioletRed4', 
	'Gray1', 'Gray2', 'Gray3', 'Gray4', 'Gray5', 'Gray6', 'Gray7', 'Gray8', 'Gray9', 'Gray10',
	'Gray11', 'Gray12', 'Gray13', 'Gray14', 'Gray15', 'Gray16', 'Gray17', 'Gray18', 'Gray19',
	'Gray20', 'Gray21', 'Gray22', 'Gray23', 'Gray24', 'Gray25', 'Gray26', 'Gray27', 'Gray28',
	'Gray29', 'Gray30', 'Gray31', 'Gray32', 'Gray33', 'Gray34', 'Gray35', 'Gray36', 'Gray37',
	'Gray38', 'Gray39', 'Gray40', 'Gray42', 'Gray43', 'Gray44', 'Gray45', 'Gray46', 'Gray47',
	'Gray48', 'Gray49', 'Gray50', 'Gray51', 'Gray52', 'Gray53', 'Gray54', 'Gray55', 'Gray56',
	'Gray57', 'Gray58', 'Gray59', 'Gray60']

	box_width = 100
	box_height = 14

	gw = GraphWin("All Colors Chart", box_width * 10, box_height * 49)
	row = 0
	col = 0

	for color in COLORS:

		x, y = col * box_width, row * box_height
		rect = Rectangle(Point(x, y), Point(x + box_width, y + box_height))
		rect.setFill(color)
		rect.draw(gw)
		txt = Text(Point(x + (box_width // 2), y + (box_height // 2)), color)
		txt.setAnchor('c')
		txt.setSize(7)
		if color in white_text:
			txt.setFill('gray80')
		else:
			txt.setFill('black')
		txt.draw(gw)


		row += 1
		if (row > 48):
			row = 0
			col += 1
			

	while True:
		if gw.checkKey() or gw.checkMouse():
			gw.close()
			break

	

#MacOS fix 2
#tk.Toplevel(_root).destroy()

# MacOS fix 1
update()

if __name__ == "__main__":
	# test()
	show_all_colors()
	# test_keys()
	
	pass
