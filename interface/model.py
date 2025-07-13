#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2025-07-12 15:36:00
# @Author  : syuansheng (Dalian Maritime University)
from pandas import read_excel,DataFrame
from matplotlib.pyplot import subplots
from utils.rasterbuilder import RasterMap
from utils.easypathfinder import dijkstra,astar
from utils.gifbuilder import generate_gif
from random import random
from time import time
from numpy import zeros

class Model:
	"""
	管理数据和业务逻辑
	"""
	def __init__(self):
		self.maparray = None
		self.rsm = RasterMap()

	def read_data_from_file(self,path):
		"""
		从excel中读取数据
		"""
		self.maparray = read_excel(path,header=None).values
		self.rsm.buildMap(self.maparray)

	def random_data(self):
		self.maparray = zeros((20,20))
		for i in range(self.maparray.shape[0]):
			for j in range(self.maparray.shape[1]):
				if i==19 and j ==0:
					self.maparray[i,j] = 1
				elif i==0 and j==19:
					self.maparray[i,j]=2
				else:
					if random() < 0.05:
						self.maparray[i,j] = 3
		self.rsm.buildMap(self.maparray)

	def export_data(self,filename):
		df = DataFrame(self.maparray)
		df.to_excel(filename,index=False,header=None)


	def run_algorithm(self,type):
		# 运行求解算法，求解过程的gif生成出来
		fig,ax = subplots(figsize=(6,6),dpi=100)
		fig.tight_layout(pad=0.9)
		if type == 1:
			# 运行dijkstra
			st = time()
			dijkstra(self.maparray,fig,ax,"dijkstra_frame_dir")
			fig,ax = subplots(figsize=(6,6),dpi=100)
			fig.tight_layout(pad=0.05)
			generate_gif("dijkstra_frame_dir","dijkstra_gif",fig,ax)
			return round(time()-st)
		elif type==2:
			# 运行astar
			st = time()
			astar(self.maparray,fig,ax,"astar_frame_dir")
			fig,ax = subplots(figsize=(6,6),dpi=100)
			fig.tight_layout(pad=0.2)
			generate_gif("astar_frame_dir","astar_gif",fig,ax)
			return round(time()-st)


