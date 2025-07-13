#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2025-07-10 23:00:31
# @Author  : syuansheng (Dalian Maritime University)

"""
这个模块实现了dijkstar和astar算法，并且同步保存了求解过程的每一帧图像，用户可以在算法运行结束后使用gifbuilder的generate_gif函数生成动图。
"""

from time import time
from .rasterbuilder import *
from .gifbuilder import *

def dijkstra(maparray,fig,ax,result_dir='result_pic'):
	"""
	dijkstra算法在栅格图上求解最短路，同时对应的更新rastermap并保存图像

	Args：
		maparray(ndarray)
		fig(Figure)
		ax(Axes)
	
	Returns:
		shortest_path_len(float)
	"""
	# 检查放帧文件的目录
	check_dir(result_dir)
	# 创建raster map
	rsm = RasterMap()
	start_point,end_point,obstacle_point_group,all_point_group = rsm.buildMap(maparray) # 转换为Point和PointGroup对象
	rsm.drawMap(ax)
	# 把第一张图保存为cover
	fig.savefig("./cover.png")
	# 算法部分
	inf = float('inf')
	# 初始化cost和parent
	for point in all_point_group:
		if point is start_point:
			point.cost = 0
		else:
			point.cost = inf
		point.parent = None
	to_be_checked_group = PointGroupOrdered("将被检查的节点集合")
	to_be_checked_group.push(start_point)
	already_checked_group = PointGroup("已经被检查的节点的集合")
	while to_be_checked_group:
		print(to_be_checked_group)
		fig.savefig('./{}/{}.png'.format(result_dir,time()))
		current_point = to_be_checked_group.pop() # 取出来cost最小的节点，这个节点已经找到最短路了
		if current_point in already_checked_group:
			# current_point里面可能有冗余，在already_checked_group里面的一定是以及找到最短路的点，并且以及访问过它的邻居节点，直接跳过
			continue
		already_checked_group.append(current_point)
		rsm.updateMap(ax,current_point,"yellow") # 已经找到起点到该点最短路的点颜色改成黄色
		# 上下左右四个方向的邻居
		neighbor_top = all_point_group.getPoint(current_point.x,current_point.y+1)
		neighbor_bottom = all_point_group.getPoint(current_point.x,current_point.y-1)
		neighbor_left = all_point_group.getPoint(current_point.x-1,current_point.y)
		neighbor_right = all_point_group.getPoint(current_point.x+1,current_point.y)
		# 对邻居进行更新
		if neighbor_top and (neighbor_top not in obstacle_point_group) and (neighbor_top not in already_checked_group):
			if current_point.cost+1 < neighbor_top.cost:
				neighbor_top.cost = current_point.cost+1
				neighbor_top.parent = current_point
			to_be_checked_group.push(neighbor_top)
		if neighbor_bottom and (neighbor_bottom not in obstacle_point_group) and (neighbor_bottom not in already_checked_group):
			if current_point.cost+1 < neighbor_bottom.cost:
				neighbor_bottom.cost = current_point.cost+1
				neighbor_bottom.parent = current_point
			to_be_checked_group.push(neighbor_bottom)
		if neighbor_left and (neighbor_left not in obstacle_point_group) and (neighbor_left not in already_checked_group):
			if current_point.cost+1 < neighbor_left.cost:
				neighbor_left.cost = current_point.cost+1
				neighbor_left.parent = current_point
			to_be_checked_group.push(neighbor_left)
		if neighbor_right and (neighbor_right not in obstacle_point_group) and (neighbor_right not in already_checked_group):
			if current_point.cost+1 < neighbor_right.cost:
				neighbor_right.cost = current_point.cost+1
				neighbor_right.parent = current_point
			to_be_checked_group.push(neighbor_right)
	# 从end_point开始回溯parent，找到构成最短路的节点的集合
	shortest_path = PointGroup("构成最短路的节点集合")
	shortest_path.insert(0,end_point)
	flag = False
	while True:
		shortest_path.insert(0,shortest_path[0].parent)
		if flag:
			# 已经把起点加进去了
			break
		if shortest_path[0].parent is start_point:
			flag = True
	for point in shortest_path:
		rsm.updateMap(ax,point,"blue") # 将起点到终点最短路上的点标记未蓝色
		fig.savefig('./{}/{}.png'.format(result_dir,time()))
	print("end_point.cost={}".format(end_point.cost))
	return end_point.cost

def astar(maparray,fig,ax,result_dir='result_pic'):
	"""
	astar算法在栅格图上求解最短路，同时对应的更新rastermap并保存图像

	Args：
		maparray(ndarray)
		fig(Figure)
		ax(Axes)
	
	Returns:
		shortest_path_len(float)
	"""
	check_dir(result_dir)
	rsm = RasterMap()
	start_point,end_point,obstacle_point_group,all_point_group = rsm.buildMap(maparray) # 转换为Point和PointGroup对象
	rsm.drawMap(ax)
	# 把第一张图保存为cover
	fig.savefig("./cover.png")
	# 算法部分
	# 因为咱们规定只能上下左右移动，所以曼哈顿距离一定满足 \hat{h} \le h.所以咱们的h就用曼哈顿距离估计了
	hath = lambda point:abs(point.x-end_point.x)+abs(point.y-end_point.y) 
	# 先给每个Point对象新增gcost和hcost属性,再初始化
	inf = float('inf')
	for point in all_point_group:
		if point is start_point:
			point.gcost = 0
		elif point is end_point:
			point.gcost = inf
		else:
			point.gcost = inf
		point.hcost = hath(point)
		point.cost = point.gcost+point.hcost
		point.parent = None
	to_be_checked_group = PointGroupOrdered("将被检查的节点集合")
	to_be_checked_group.push(start_point)
	# a star中再already_checked_group里不一定保证以及找到了从起点到该点的最短路，当能找到更短时还得重新提到to_be_checked_group中去。
	# already_checked_group再a star中只起到跳过to_be_checked_group点的作用
	already_checked_group = PointGroup("已经被检查的节点的集合") 
	while to_be_checked_group:
		print(to_be_checked_group,"不能反应算法合适结束，因为算法可能通过if条件提前终止!")
		fig.savefig('./{}/{}.png'.format(result_dir,time()))
		current_point = to_be_checked_group.pop() # 取出f最小也就是cost最小的点
		if current_point in already_checked_group:
			# current_point里面可能有冗余，在already_checked_group里面的一定是以及找到最短路的点，并且以及访问过它的邻居节点，直接跳过
			continue
		already_checked_group.append(current_point)
		rsm.updateMap(ax,current_point,"yellow")
		# 已经找到起点到终点的最短路了，结束
		if current_point is end_point:
			# 从end_point开始回溯parent，找到构成最短路的节点的集合
			shortest_path = PointGroup("构成最短路的节点集合")
			shortest_path.insert(0,end_point)
			flag = False
			while True:
				shortest_path.insert(0,shortest_path[0].parent)
				if flag:
					# 已经把起点加进去了
					break
				if shortest_path[0].parent is start_point:
					flag = True
			for point in shortest_path:
				rsm.updateMap(ax,point,"blue") # 将起点到终点最短路上的点标记未蓝色
				fig.savefig('./{}/{}.png'.format(result_dir,time()))
			print("end_point.cost={}".format(end_point.cost))
			return end_point.cost
		# 上下左右四个方向的邻居
		neighbor_top = all_point_group.getPoint(current_point.x,current_point.y+1)
		neighbor_bottom = all_point_group.getPoint(current_point.x,current_point.y-1)
		neighbor_left = all_point_group.getPoint(current_point.x-1,current_point.y)
		neighbor_right = all_point_group.getPoint(current_point.x+1,current_point.y)
		# 更新邻居,注意看这块条件和dijkstar的区别
		if neighbor_top and (neighbor_top not in obstacle_point_group):
			# 更新gcost和parent
			if current_point.gcost+1<neighbor_top.gcost:
				neighbor_top.gcost = current_point.gcost+1
				neighbor_top.parent = current_point
			if (neighbor_top in already_checked_group) and (neighbor_top.gcost+neighbor_top.hcost < neighbor_top.cost):
				# 把neibor_top从already_checked_group中删除来
				already_checked_group.delPoint(neighbor_top.x,neighbor_top.y)
			neighbor_top.cost = neighbor_top.gcost+neighbor_top.hcost
			if neighbor_top not in already_checked_group:
				to_be_checked_group.push(neighbor_top)
		if neighbor_bottom and (neighbor_bottom not in obstacle_point_group):
			if current_point.gcost+1<neighbor_bottom.gcost:
				neighbor_bottom.gcost = current_point.gcost+1
				neighbor_bottom.parent = current_point
			if (neighbor_bottom in already_checked_group) and (neighbor_bottom.gcost+neighbor_bottom.hcost)<neighbor_bottom.cost:
				already_checked_group.delPoint(neighbor_bottom.x,neighbor_bottom.y)
			neighbor_bottom.cost = neighbor_bottom.gcost+neighbor_bottom.hcost
			if neighbor_bottom not in already_checked_group:
				to_be_checked_group.push(neighbor_bottom)
		if neighbor_left and (neighbor_left not in obstacle_point_group):
			if current_point.gcost+1<neighbor_left.gcost:
				neighbor_left.gcost = current_point.gcost+1
				neighbor_left.parent = current_point
			if (neighbor_left in already_checked_group) and (neighbor_left.gcost+neighbor_left.hcost)<neighbor_left.cost:
				already_checked_group.delPoint(neighbor_left.x,neighbor_left.y)
			neighbor_left.cost = neighbor_left.gcost+neighbor_left.hcost
			if neighbor_left not in already_checked_group:
				to_be_checked_group.push(neighbor_left)
		if neighbor_right and (neighbor_right not in obstacle_point_group):
			if current_point.gcost+1<neighbor_right.gcost:
				neighbor_right.gcost = current_point.gcost+1
				neighbor_right.parent = current_point
			if (neighbor_right in already_checked_group) and (neighbor_right.gcost+neighbor_right.hcost)<neighbor_right.cost:
				already_checked_group.delPoint(neighbor_right.x,neighbor_right.y)
			neighbor_right.cost = neighbor_right.gcost+neighbor_right.hcost
			if neighbor_right not in already_checked_group:
				to_be_checked_group.push(neighbor_right) 
		# 未来优化：这里打断类似结构的if实际上可单独写个函数，方便复用。

__all__ = ['dijkstra','astar']
