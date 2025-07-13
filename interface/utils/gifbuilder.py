#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2025-07-10 22:59:44
# @Author  : syuansheng (Dalian Maritime University)

from functools import partial
from os import mkdir,listdir
from os.path import isdir,join
from shutil import rmtree
from numpy import array
from PIL import Image
from matplotlib.animation import FuncAnimation,PillowWriter


def check_dir(result_dir:str):
	"""
	创建名为result_dir的目录，如果存在就先删除再创建（始终确保该目录为空）
	"""
	if isdir(result_dir):
		rmtree(result_dir)
	mkdir(result_dir)

# 定义如何获取每一帧 ,这个函数用户不要自己调用
def _update(frame,im,result_dir,frame_files):
    img = Image.open(join(result_dir, frame_files[frame]))
    im.set_array(array(img))
    # # 添加帧数文本（可选）
    # ax.set_title(f"Frame: {frame+1}/{len(frame_files)}", fontsize=12)
    return im,

def generate_gif(result_dir,output_name,fig,ax,FPS=24,DPI=100):
	"""
	将指定文件夹中的每一帧图像组合成gif

	Args:
		result_dir(str)：存放帧图像的文件夹的名字，必须是当前目录的子文件夹哦
		output_name(str)：生成的gif图像的名称
		FPS：每秒帧数，这个数值越高，gif就越流畅，但文件也就越大
		DPI：清晰度
		ax: 指定的axes对象
		fig: 指定的fig对象

	"""
	ax.axis('off')  # 关闭坐标轴，因为是展示图片，所以关闭刻度用处不大
	frame_files = sorted([f for f in listdir(result_dir) if f.endswith('.png')], 
                    key=lambda x: int(x.split('.')[0])) # 按顺序读取每一帧文件的文件名
	first_frame = Image.open(join(result_dir,frame_files[0])) # 将第一帧率图片读取为Image类对象，这个对象有__array__方法可以转换为数组
	im = ax.imshow(array(first_frame), animated=True) # 现在ax上把第一帧画出来
	# 创建动画
	ani = FuncAnimation(
	    fig, 
	    partial(_update,im=im,result_dir=result_dir,frame_files=frame_files), 
	    frames=len(frame_files),
	    interval=1000/FPS,  # 帧间隔(ms)
	    blit=True,          # 使用blitting优化性能
	    repeat=True,         # 循环播放
	)
	# 保存为GIF（使用PillowWriter）
	writer = PillowWriter(fps=FPS)
	ani.save(output_name+'.gif', writer=writer, dpi=DPI)
	print("动画已保存至: {}".format(output_name+'.gif'))

__all__ = ['check_dir','generate_gif']