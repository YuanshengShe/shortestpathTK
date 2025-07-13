#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2025-07-10 21:54:17
# @Author  : syuansheng (Dalian Maritime University)

"""raster map generation tool

This module provides RasterMap objects for quickly creating raster maps, 
as well as Point, PointGroup, and PointGroupOdered objects, making it very
convenient for users to access the blocks in the created raster map!

Usage:
from rasterbuilder import *
from matplotlib.pyplot import subplots,show
from pandas import  read_excel
fig,ax = subplots(figsize=(6,6),dpi=100)
rsm = RasterMap()
start_point,end_point,obstacle_point_group,all_point_group = rsm.buildMap(read_excel('./rasterbuilder_test_data.xlsx',header=None).values)
rsm.drawMap(ax)
show()

About the maparray:
RasterMap depends on the array maparray, which is defined as follows:
	- 0 represents a general block.
	- 1 represents the starting block.
	- 2 represents the endpoint block.
	- 3 represents obstacle blocks.
I recommend using Excel to generate a maparray, RasterMap can ensure the accuracy
The raster map looks the same as your maparray.You can refer to the provided test maparray file
rasterbuilder_test_data.xlsx to learn how to get a valid maparray.

If you have any questions about the use of this module or would like it to 
provide some new features, please feel free to contact me at any time.
"""
from heapq import heapify,heappush,heappop
from numpy import ndarray
from matplotlib.patches import Rectangle

class Point:
	"""
	A Point object uniquely corresponds to a block in the raster map, where the
	attributes x and y represent the anchor point at the lower-left corner of 
	the block. The facecolor and edgecolor attributes are typically not accessed, 
	but when implementing algorithms such as Dijkstra or A*, you may frequently 
	access the cost and parent attributes. In these algorithms, we traditionally
	maintained two tables: one to store the shortest path lengths from the starting
	point to each point, and another to track the previous point on the shortest 
	path to each point from the starting point. With the cost and parent attributes,
	we can now eliminate the need for these two tables.

	In addition, the cost values can be directly compared between any two Point objects
	(a common operation in Dijkstar and A-star algorithms) without the need to first 
	read the cost values of the Point objects before comparing the sizes.
	"""

	def __init__(self,anchor_x,anchor_y):
		self.x = anchor_x
		self.y = anchor_y
		self.facecolor = None 
		self.edgecolor = None 
		self.cost = None
		self.parent = None

	def __eq__(self,other):
		assert isinstance(other,Point),"Both ends of the relational operation must be of type Point!"
		return self.cost == other.cost

	def __lt__(self,other):
		assert isinstance(other,Point),"Both ends of the relational operation must be of type Point!"
		return self.cost < other.cost

	def __le__(self,other):
		assert isinstance(other,Point),"Both ends of the relational operation must be of type Point!"
		return self.cost <= other.cost

	def __str__(self):
		return "<Point({},{}),cost={}>".format(self.x,self.y,self.cost)

class PointGroup(list):
	"""
	The PointGroup object is an object similar to a list in Python, used to manage a collection of Point objects. 
	Unlike directly using a list for management, the PointGroup object allows the use of the in operator to check
	whether a Point object is in the collection. At the same time, the corresponding Point object can be directly 
	obtained through the x and y properties of the Point object (which is very convenient when implementing 
	algorithms such as Dijkstar and A-star to obtain neighboring blocks of a block).
	"""

	def __init__(self,name,iterable=[]):
		super(PointGroup,self).__init__(iterable)
		self.name = name

	def __str__(self):
		return "<PointGroup named {} with {} Points in it>".format(self.name,len(self))

	def __contains__(self,item):
		return (item.x,item.y) in [(point.x,point.y) for point in self]

	def getPoint(self,x,y):
		for point in self:
			if (point.x==x) and (point.y==y):
				return point
		else:
			return # 没找到

	def delPoint(self,x,y):
		for i,point in enumerate(self):
			if (point.x==x) and (point.y==y):
				self.pop(i) # 从中剔除这个Point对象

class PointGroupOrdered(PointGroup):
	"""
	The PointGroupOrdered object is similar to a heap object, managing Point objects through the same behavior
	as a heap. (When implementing algorithms such as Dijkstar and A-star, we often need to obtain the Point 
	with the minimum current cost. In this case, maintaining it through the PointGroupOrdered object can bring a lot of convenience.)
	"""

	def __init__(self,name,iterable=[]):
		heapify(iterable)
		super(PointGroupOrdered,self).__init__(iterable)
		self.name = name

	def push(self,point):
		# 将point放入组中，保持顺序
		heappush(self,point)

	def pop(self):
		# 将组中最小的point弹出来
		return heappop(self)

	def __str__(self):
		return "<PointGroupOrdered named {} with {} Points in it>".format(self.name,len(self))

class RasterMap:
	"""
	The RasterMap class is the core class of the Rasterbuider module, which provides the following functions:
	1. Convert the array maparray to Point, PointGroup objects, which also uniquely correspond to a raster map.
	2. Draw the raster map defined using Point and PointGroup objects onto the specified Axes.
	3. Update the color of the specified block on the raster map drawn on the specified Axes.
	"""

	def __init__(self):
		self.start_point = None
		self.end_point = None
		self.obstacle_point_group = PointGroup("obstacle")
		self.all_point_group = PointGroup("all")

	def buildMap(self,maparray:ndarray):
		self.size = maparray.shape
		for i in range(maparray.shape[0]):
			for j in range(maparray.shape[1]):
				point = Point(maparray.shape[0]-i-1,j)
				if maparray[i,j] == 1:
					point.facecolor='green'
					point.edgecolor='gray'
					self.start_point = point
				elif maparray[i,j] == 2:
					point.facecolor='red'
					point.edgecolor='gray'
					self.end_point = point
				elif maparray[i,j] == 3:
					point.facecolor='black'
					point.edgecolor='gray'
					self.obstacle_point_group.append(point)
				else:
					point.facecolor='white'
					point.edgecolor='gray'
				self.all_point_group.append(point)
		return self.start_point,self.end_point,self.obstacle_point_group,self.all_point_group

	def drawMap(self,ax):
		try:
			ax.set_xlim([0,self.size[0]])
			ax.set_ylim([0,self.size[1]])
			ax.set_xticks([])
			ax.set_yticks([])
			for point in self.all_point_group:
				ax.add_patch(Rectangle((point.x,point.y),width=1,height=1,facecolor=point.facecolor,edgecolor=point.edgecolor))
		except Exception as e:
			print("Please first use maparray to create a map!")

	def updateMap(self,ax,point,facecolor):
		ax.add_patch(Rectangle((point.x,point.y),width=1,height=1,facecolor=facecolor,edgecolor=point.edgecolor,alpha=0.4))

__all__ = ['Point','PointGroup','PointGroupOrdered','RasterMap']


