#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2025-07-11 22:28:33
# @Author  : syuansheng (Dalian Maritime University)
from functools import partial
from weakref import proxy
from tkinter import *
from tkinter.filedialog import askopenfilename,asksaveasfilename
from tkinter.simpledialog import askinteger,askstring
from tkinter.ttk import Notebook,Progressbar
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from PIL import Image, ImageSequence
from pandas import DataFrame
from numpy import array
from pandastable import Table
import webbrowser

class UI(Tk):
	"""
	MVC架构的View部分，纯UI构建，提供视图和视图更新方法，一切控制和交互权力交给controller
	"""
	def __init__(self,controller):
		"""
		初始化根窗口
		"""
		super(UI,self).__init__() # 调用父类的__init__放法完成初始化，self是Tk子类的实例，比Tk更强
		self.geometry("750x400+560+250") # 设置根窗口的宽、高、距离左侧和上侧的距离分别为900、400、450、150
		self.resizable(False,False) # 禁止用户自行调整窗口大小
		self.title('最短路求解器(v1.0.0)') # 设置跟窗口标题
		self.iconbitmap('icon.ico') # 修改根窗口图标
		self._connect_controller(controller) # 建立与controller的双向链接
		self._set_menu() # 设置菜单
		self._set_notebook()
		self._set_frame_solver()
		self._set_frame_table()

	def _connect_controller(self,controller):
		"""
		建立与controler之间的双向引用
		"""
		self.controller = proxy(controller)

	def _set_menu(self):
		"""
		设置根窗口的菜单
		"""
		self.menu = Menu(self)
		self.data_menu = Menu(self.menu,tearoff=False)
		self.data_menu.add_command(label='读取(.xlsx)文件',command=self.controller.readFromFile)
		self.data_menu.add_command(label='随机生成测试栅格',command=self.controller.randomData)
		self.data_menu.add_command(label='将当前算例另存为(.xlsx)文件',command=self.controller.exportData)
		self.menu.add_cascade(label='文件',menu=self.data_menu) # data_menu作为menu的子菜单
		self.menu.add_command(label='使用说明',command=self.controller.openurl)
		self.config(menu=self.menu) # 配置根窗口的菜单

	def _set_notebook(self):
		"""
		设置Notebook组件
		"""
		self.notebook = Notebook(self)
		self.frame_solver = Frame(self.notebook) # 求解界面
		self.frame_table = Frame(self.notebook) # 数据表格界面
		self.notebook.add(self.frame_solver,text='求解窗口')
		self.notebook.add(self.frame_table,text='数据窗口')
		self.notebook.pack(padx=10,pady=10,fill=BOTH,expand=True) # 组件距离左侧和上侧10，组件填充满所分配的空间，如果所在父容器大小变化，该组件同步变化

	def _set_frame_solver(self):
		"""
		设置frame_solver组件内的其它组件
		"""
		self.lf1 = LabelFrame(self.frame_solver,text='算法选择')
		self.lf2 = LabelFrame(self.frame_solver,text='状态检查')
		self.lf3 = LabelFrame(self.frame_solver,text='求解过程回溯')
		self.lf1.grid(row=2,column=0,padx=10,pady=10,stick=W+E+N)
		self.lf2.grid(row=0,column=0,rowspan=2,padx=10,pady=10,sticky=W+E+N+S) 
		self.lf3.grid(row=0,column=1,rowspan=3,columnspan=3,padx=10,pady=10,sticky=W+E+N+S)
		self.frame_solver.grid_rowconfigure(0,weight=1)  # 设置frame内各个组件随着窗口变化等比例缩放
		self.frame_solver.grid_rowconfigure(1,weight=1)
		self.frame_solver.grid_columnconfigure(0,weight=1)
		self.frame_solver.grid_columnconfigure(1,weight=1)

		self.rbvar = IntVar() # 这个变量将存储被选中的项的value值，value相当于将一个选项映射为值
		self.rbvar.set(1)
		self.rb1 = Radiobutton(self.lf1,text='Dijkstra',variable=self.rbvar,value=1,command=self.controller.choose)
		self.rb2 = Radiobutton(self.lf1,text='A Star',variable=self.rbvar,value=2,command=self.controller.choose)
		self.bt = Button(self.lf1,text='Run',bitmap='hourglass',compound='left',relief="flat",command=self.controller.solve)
		self.bt.pack(expand=True,side=BOTTOM,fill=BOTH)
		self.rb1.pack(expand=True,side=LEFT)
		self.rb2.pack(expand=True,side=RIGHT)
		# self.pb = Progressbar(self.lf1,orient=HORIZONTAL,length=100,mode='determinate')
		# self.pb['maximum'] = 100
		# self.pb['value'] = 0
		# self.pb.grid(row=0,column=0,columnspan=2,sticky=W+E+N+S)
		# self.rb1.grid(row=1,column=0,sticky=W+E+N+S)
		# self.rb2.grid(row=1,column=1,sticky=W+E+N+S)
		# self.bt.grid(row=2,column=0,columnspan=2)
		# self.lf1.rowconfigure(0,weight=1)    # grid让子组件完全应用父亲组件的空间
		# self.lf1.rowconfigure(1,weight=1)
		# self.lf1.rowconfigure(2,weight=1)
		# self.lf1.columnconfigure(0,weight=1)
		# self.lf1.columnconfigure(1,weight=1)

		self.lbvar1 = StringVar()
		self.lbvar1.set('Unready')
		Label(self.lf2,text='算例准备').grid(row=0,column=0,sticky=N+S+W+E)
		self.lb1 = Label(self.lf2,textvariable=self.lbvar1,fg='red')
		self.lbvar2 = StringVar()
		self.lbvar2.set('Unknown')
		Label(self.lf2,text='算例规模').grid(row=1,column=0,sticky=N+S+W+E)
		self.lb2 = Label(self.lf2,textvariable=self.lbvar2,fg='red')
		self.lbvar3 = StringVar()
		self.lbvar3.set('Dijkstra')
		Label(self.lf2,text='算法选择').grid(row=2,column=0,sticky=N+S+W+E)
		self.lb3 = Label(self.lf2,textvariable=self.lbvar3,fg='green')		
		self.lbvar4 = StringVar()
		self.lbvar4.set('Unknown')
		Label(self.lf2,text='求解时间(s)').grid(row=3,column=0,sticky=N+S+W+E)
		self.lb4 = Label(self.lf2,textvariable=self.lbvar4,fg='red')
		self.lf2.grid_rowconfigure(0,weight=1)  # 设置lf2内各个组件随着窗口变化等比例缩放
		self.lf2.grid_rowconfigure(1,weight=1)
		self.lf2.grid_rowconfigure(2,weight=1)
		self.lf2.grid_rowconfigure(3,weight=1)
		self.lf2.grid_columnconfigure(0,weight=1)
		self.lf2.grid_columnconfigure(1,weight=1)
		self.lb1.grid(row=0,column=1,sticky=N+S+W+E)
		self.lb2.grid(row=1,column=1,sticky=N+S+W+E)
		self.lb3.grid(row=2,column=1,sticky=N+S+W+E)
		self.lb4.grid(row=3,column=1,sticky=N+S+W+E)

		self.fig,self.ax = plt.subplots(figsize=(6,6),dpi=6,gridspec_kw={"wspace":0.05,"hspace":0.05}) 
		self.fig.subplots_adjust(left=0,right=1,bottom=0,top=1)

		# 隐藏特定边框
		self.ax.spines['top'].set_visible(False)
		self.ax.spines['right'].set_visible(False)
		self.ax.spines['bottom'].set_visible(False)
		self.ax.spines['left'].set_visible(False)	
		# 隐藏刻度
		self.ax.set_xticks([])
		self.ax.set_yticks([])	
		# 创建适配器类
		self.agger = FigureCanvasTkAgg(self.fig,self.lf3)
		self.agger.draw() # 重新渲染figure上的图形到tkinter中
		canvas = self.agger.get_tk_widget() # 返回widget用于布局
		canvas.pack(padx=10,pady=10,fill=BOTH,expand=True)

	def _set_frame_table(self):
		"""
		设置frame_table组件内的其它组件
		"""
		data = {
			"0":{"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0},
			"1":{"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0},
			"2":{"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0},
			"3":{"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0},
			"4":{"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0},
			"5":{"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0},
			"6":{"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0},
			"7":{"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0},
			"8":{"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0},
			"9":{"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0}} # 初始化表格，要更新表格的展示，只需要更新pt的df，然后再redraw一下
		df = DataFrame(data)
		self.pt = Table(self.frame_table, dataframe=df, showtoolbar=False,enable_menus=False,showstatusbar=True)
		self.pt.show()

	def update_ax_0(self,rsm):
		"""
		更新ax，展示当前选择的栅格图
		"""
		self.ax.cla()
		rsm.drawMap(self.ax)
		self.agger.draw()

	def _update(self,frame,frames,img):
		img.set_array(frames[frame])
		return [img]

	def update_ax_1(self,giffilename):
		"""
		更新ax，动态展示寻路过程
		"""
		self.ax.cla()#清空axes
		self.agger.draw()
		gif = Image.open(giffilename+'.gif')
		# 提取所有帧和延迟时间
		frames = []
		delays = []
		for frame in ImageSequence.Iterator(gif):
			# 转换为 RGB 模式
			frame = frame.convert("RGB")
			frames.append(array(frame))
		    # 获取帧延迟（毫秒）
			try:
				delays.append(frame.info['duration'])
			except KeyError:
				delays.append(100)  # 默认延迟 100ms
		img = self.ax.imshow(frames[0])
		# 计算平均帧率（FPS）
		avg_delay = sum(delays) / len(delays)
		fps = 1000 / avg_delay  # 帧/秒
		# 创建动画
		ani = animation.FuncAnimation(
			self.fig, 
			partial(self._update,img=img,frames=frames), 
			frames=len(frames),
			interval=avg_delay,  # 帧间隔（毫秒）
			blit=True
		)
		self.agger.draw() # 在fig上画好后渲染

	def getfilename(self):
		path = askopenfilename(title='请选择后缀为(.xlsx)的数据文件',defaultextension=".xlsx", filetypes=(("Excel files", "*.xlsx"), ("All files", "*.*")))
		return path

	def getoutputfilename(self):
		path = asksaveasfilename(title='输入保存文件名')
		return path

	def update_data_table(self,new_data):
		"""
		根据新的数据更新数据窗口视图
		"""
		self.pt.model.df = DataFrame(new_data)
		self.pt.redraw()

	def update_state_check1(self):
		"""
		更新状态检查中的算例准备lb1和算例规模lb2标签
		"""
		self.lbvar1.set("Ready")
		self.lbvar2.set(str(len(self.pt.model.df)))
		self.lb1.config(fg='green')
		self.lb2.config(fg='green')

	def update_state_check2(self,time):
		self.lbvar4.set(str(time))
		self.lb4.config(fg='green')

	def update_state_check3(self):
		self.lbvar3.set(["Dijkstra",'A star'][self.rbvar.get()-1])

	def open_my_github(self):
		webbrowser.open("https://github.com/YuanshengShe/shortestpathTK")

if __name__ == '__main__':
	# 测试
	view = UI()
	view.mainloop()