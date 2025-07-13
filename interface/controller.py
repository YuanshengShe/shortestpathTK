#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2025-07-12 10:02:04
# @Author  : syuansheng (Dalian Maritime University)
from viewer import UI
from model import Model

class Controller:
	"""
	Controller类用于处理用户在视图界面的输入，协调数据模型和视图的交互——更新数据，再根据更新的数据刷新ui
	"""
	def __init__(self):
		self.view = UI(self) # ui对象
		self.model = Model() # datamodel对象

	def readFromFile(self):
		"""
		处理用户在ui中点击读取数据文件的逻辑
		"""
		path = self.view.getfilename()
		# 更新model
		self.model.read_data_from_file(path)
		# 更新view
		self.view.update_data_table(self.model.maparray)
		self.view.update_ax_0(self.model.rsm)
		self.view.update_state_check1()

	def randomData(self):
		self.model.random_data()
		self.view.update_data_table(self.model.maparray)
		self.view.update_ax_0(self.model.rsm)
		self.view.update_state_check1()

	def exportData(self):
		filename = self.view.getfilename()
		self.model.export_data(filename)

	def choose(self):
		self.view.update_state_check3()

	def openurl(self):
		self.view.open_my_github()

	def solve(self):
		"""
		处理用户在ui中点击运行求解算法的逻辑
		"""
		self.view.update_state_check3()
		run_time = self.model.run_algorithm(self.view.rbvar.get())
		self.view.update_ax_1(['dijkstra_gif','astar_gif'][self.view.rbvar.get()-1])
		self.view.update_state_check2(run_time)

	def run(self):
		self.view.mainloop()