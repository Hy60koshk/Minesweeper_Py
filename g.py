
from graphics import * # https://mcsp.wartburg.edu/zelle/python/graphics.py
from random import randrange

bnColors = ['#dddddd', '#0000ff', '#00a850', '#ff0000', '#0000A8'
, '#A80050', '#00a0a0', '#a000a0', '#a0a0a0']

win = GraphWin('Minesweeper', 400, 600)
cells = []
bombs = 0
openCells = 0
message = Text(Point(40, 520), 'You Lost!')

class MineCell:
	def __init__(self, isBomb: bool, x: int, y: int):
		self.isOpen = False
		self.isMarked = False
		self.isBomb = isBomb
		self.x = x
		self.y = y
		self.X = x * 20
		self.Y = y * 20 + 100
		self.Rect = Rectangle(Point(self.X, self.Y), Point(self.X + 19, self.Y + 19))
		self.Rect.setWidth(1)
		self.Rect.setFill('#bbbbbb')
		self.Rect.draw(win)
		self._Mark = Polygon(
			Point(self.X + 4, self.Y + 4)
			, Point(self.X + 15, self.Y + 9)
			, Point(self.X + 4, self.Y + 15)
		)
		self._Mark.setFill('#F00000')

	def reinit(self, isBomb: bool):
		self.Rect.undraw()
		if (self.isMarked):
			self.isMarked = False
			self._Mark.undraw()
		self.isOpen = False
		self.isBomb = isBomb
		self.Rect.setFill('#bbbbbb')
		self.Rect.draw(win)

	def Open(self):
		if (not self.isOpen):
			self.isOpen = True
			self.Rect.undraw()
			if (self.isBomb):
				self.Rect.setFill('#f00000')
				self.Rect.draw(win)
				bomb = Circle(Point(self.X + 9, self.Y + 10), 6)
				bomb.setFill('black')
				bomb.draw(win)
			else:
				global openCells
				openCells = openCells + 1
				self.Rect.setFill('#eeeeee')
				self.Rect.draw(win)
				x = self.x
				y = self.y
				stx = x - 1 if x > 0 else 0
				sty = y - 1 if y > 0 else 0
				endx = x + 1 if x < 19 else 19
				endy = y + 1 if y < 19 else 19
				bombnum = 0
				for i in range(stx, endx + 1):
					for j in range(sty, endy + 1):
						if cells[i][j].isBomb: bombnum += 1
				if bombnum > 0:
					bnlabel = Text(Point(self.X + 9, self.Y + 10), bombnum)
					bnlabel.setTextColor(bnColors[bombnum])
					bnlabel.draw(win)
				else:
					for i in range(stx, endx + 1):
						for j in range(sty, endy + 1):
							if not (i == x and j == y):
								cells[i][j].Open()
			

	def Mark(self):
		self.isMarked = not self.isMarked
		if (self.isMarked):
			self._Mark.draw(win)
		else:
			self._Mark.undraw()

def isWithin(point: Point, rect: Rectangle):
	p1 = rect.getP1()
	p2 = rect.getP2()
	return p1.x <= point.x and p2.x >= point.x and p1.y <= point.y and p2.y >= point.y

def isWithinC(point: Point, circ: Circle):
	c = circ.getCenter()
	r = circ.getRadius()
	return (point.x - c.x) ** 2 + (point.y - c.y) ** 2 <= r * r

def resetField():
	message.undraw()
	global openCells, bombs
	bombs = 0
	openCells = 0
	for i in range(0, 20):
		for j in range(0, 20):
			if (bombs < 40):
				isBomb = randrange(20) > 17
				if (isBomb):
					bombs += 1
			else:
				isBomb = False
			cells[i][j].reinit(isBomb)

closebtn = Rectangle(Point(350, 0), Point(399, 29))
closebtn.setFill('#e60c0c')
closebtn.draw(win)
closebtnlabel = Text(Point(374, 15), 'X')
closebtnlabel.setTextColor('#ffffff')
closebtnlabel.draw(win)

resetbtn = Rectangle(Point(0, 0), Point(79, 29))
resetbtn.setFill('#808080')
resetbtn.draw(win)
resetbtnlabel = Text(Point(39, 15), 'Reset')
resetbtnlabel.setTextColor('#ffffff')
resetbtnlabel.draw(win)

for i in range(0, 20):
	cells.append([])
	for j in range(0, 20):
		if (bombs < 40):
			isBomb = randrange(20) > 17
			if (isBomb):
				bombs += 1
		else:
			isBomb = False
		cells[i].append(MineCell(isBomb, i, j))

while True:
	clickpoint = win.getMouse()
	if (isWithin(clickpoint, closebtn)):
		win.close()
	elif (isWithin(clickpoint, resetbtn)):
		resetField()
	else:
		x = int(clickpoint.x // 20)
		y = int((clickpoint.y - 100) // 20)
		if x > -1 and x < 20 and y > -1 and y < 20:
			cell = cells[x][y]
			if (win.mouseBtn == "L"):
				if (not cell.isMarked):
					if (cell.isBomb):
						message.setText('You Lost!')
						message.draw(win)
					cell.Open()
					if openCells + bombs == 400:
						message.setText('You won!')
						message.draw(win)
			else:
				cell.Mark()
