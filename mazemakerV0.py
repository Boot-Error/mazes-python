#!/usr/bin/rnv python

import turtle
import random

# variable
me   = 100
seed = "banana" 

board = range(1, me+1)


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
	
	h  = toMatrix(board)
	c  = board.index(n)/int(me**0.5)
	ha = h[c].index(n)
	va = transpose(h)[ha].index(n)
	return (ha, va)

def nneighbors(n, ff=False):

	coord = boardCoords(n)
	h  = toMatrix(board)
	neighbors = []

	hn = filter(lambda x: 0<=x<me**0.5, [coord[1]-1, coord[1]+1])
	vn = filter(lambda x: 0<=x<me**0.5, [coord[0]-1, coord[0]+1])

	neighbors.extend([h[coord[1]][i] for i in vn])
	neighbors.extend([transpose(h)[coord[0]][i] for i in hn])
	
	return neighbors

def mkBox(cons):

	cp = turtle.pos()
	s = 0
	d = 15
	turtle.pu()
	turtle.goto((cp[0]+d, cp[1]+d))
	endp = [(d, -d), (-d, -d), (-d, d), (d, d)]
	while s<4:
		if cons[s]:
			turtle.pd()
		else:
			turtle.pu()

		sf = endp[s]
		turtle.goto((cp[0]+sf[0], cp[1]+sf[1]))
		s += 1
	
	turtle.pu()
	turtle.goto(cp)
	turtle.pd()
			
def main():
	turtle.goto(0, 0)
	visited = []
	boxD = {1:[0, 1, 1, 0]}
	directs = {-1:[0, 1, 1, 1], 
		   1:[1, 1, 0, 1], 
	          -me**0.5:[1, 1, 1, 0], 
		   me**0.5:[1, 0, 1, 1], 
		   0:[0, 0, 0, 0]}
	s = stack()
	s.push(1)
	prev = 1
	while len(s.l)>0:
		
		c = s.top()
		visited.append(c)
		pd = directs[c - prev]
		boxD[c] = [all((pd[i], boxD[prev][i]))for i in range(4)] if boxD.has_key(c) else pd
		print boxD[c]
		# mkBox(boxD[c])
		
		cr = boardCoords(c)
		# turtle.pu()
		turtle.goto((cr[0]*30), (cr[1]*30))
		turtle.dot(3)
		nb = filter(lambda x: x not in visited, nneighbors(c))
	       	#mkBox([1, 1, 1, 1])
		if len(nb)>0:
			nx = random.choice(nb)
			s.push(nx)

		else:
			q = s.pop()
		
		prev = c

