#!/usr/bin/env python

import turtle
import random
from PIL import Image, ImageDraw


# variable
me   = 50**2
seed = "banana" 
side = 10

board = range(1, me+1)
boardImage = Image.new("RGB", ((side*int(me**0.5))+(3*side), )*2)
boardDraw   = ImageDraw.Draw(boardImage)
boardDraw.rectangle((0, 0, boardImage.size[0], boardImage.size[1]), (255, 255, 255))

# a quick stack implementation

class stack:

	def __init__(self):
		self.l = []
		
	def size(self):
		return len(self.l)

	def push(self, e):	
		self.l.append(e)

	def pop(self):
		return self.l.pop(-1)

	def exists(self, e):
		return e in self.l

	def top(self):
		return self.l[-1]
# helper functions
transpose = lambda m: zip(*m)
order     = lambda m: (len(m), len(m[0]))
toMatrix  = lambda f: [f[i:i+int(me**0.5)] for i in range(len(f)) if i%int(me**0.5)==0]


def boardCoords(n):
	"""converts the cell address to x,y coordinates"""	
	h  = toMatrix(board)
	c  = board.index(n)/int(me**0.5)
	ha = h[c].index(n)
	va = transpose(h)[ha].index(n)
	return (ha, va)

def nneighbors(n, ff=False):
	"""computes the nearest neighbors, (up, down, left, right) only"""
	coord = boardCoords(n)
	h  = toMatrix(board)
	neighbors = []

	hn = filter(lambda x: 0<=x<me**0.5, [coord[1]-1, coord[1]+1])
	vn = filter(lambda x: 0<=x<me**0.5, [coord[0]-1, coord[0]+1])

	neighbors.extend([h[coord[1]][i] for i in vn])
	neighbors.extend([transpose(h)[coord[0]][i] for i in hn])
	
	return neighbors

# plotting using PIL
def mkBox(coord, cons):
	
	x, y = coord
	s = int(side/2)
	box = [
		(x+s, y-s, x+s, y+s),
		(x-s, y-s, x+s, y-s),
		(x-s, y-s, x-s, y+s),
		(x-s, y+s, x+s, y+s)
	]
	for i in zip(cons, box):
		if i[0]:
			boardDraw.line(i[1], fill=0)
		
	

def plotonImage():
	"""generates the maze and plots it"""
	
	# initializing variables

	start, end = 1, me
	visited = []
	boxD = {1:[0, 1, 1, 0]}
	directs = {-1:[0, 1, 1, 1], 
		   1:[1, 1, 0, 1], 
	          -me**0.5:[1, 1, 1, 0], 
		   me**0.5:[1, 0, 1, 1], 
		   0:[0, 1, 1, 0]}
	s = stack()
	s.push(start)
	prev = start
	ss = 1

	# main loop
	while len(s.l)>0:
		
		c = s.top()
		
		cr = boardCoords(c)
		xc, yc = ((cr[0]*int(side)+side*2), (cr[1]*int(side)+side*2))
		
		# generating constraints for the walls
		nb = filter(lambda x: x not in visited, nneighbors(c))
		pd = directs[c - prev]
		nvnb = map(lambda y: c-y, filter(lambda x: x not in visited, nneighbors(c)))
		pds  = [directs[i] for i in nvnb]
		boxD[c] = [all((pd[i], boxD[prev][i]))for i in range(4)] if boxD.has_key(c) else pd
		for i in pds:
			boxD[c] =  [all((i[k], boxD[c][k]))for k in range(4)] if boxD.has_key(c) else i 
	       	
		if c not in visited:
			mkBox((xc, yc), boxD[c])

		# seeking next cell
		if len(nb)>0:
			nx = random.choice(nb)
			s.push(nx)
			print "[+] Moving to : ", nx

		else:
			# backtracking
			q = s.pop()
			print "[-] Backtracking from : ", q

			# updating the end pos, based on size of stack
			ss = s.size() if s.size()>=ss else ss
			end = c if ss==s.size() else end

		visited.append(c)
		prev = c
	
	# plotting the start and end
	for points in [start, end]:
	
		coord = boardCoords(points)
		cw = lambda i, r: coord[i]*int(side)+(side*2)+r
		boardDraw.ellipse((cw(0, -2), cw(1, -2), cw(0, 2), cw(1, 2)), fill=255)

if __name__ == "__main__":
	
	plotonImage()
	print "[*] DONE!"
	boardImage.save("maze.png")
