**A visualization project related to A * and Dijkstra's algorithm.**      

<img width="600" height="350" alt="image" src="https://github.com/user-attachments/assets/14f957eb-e68c-4b6f-99f4-4cdeccd46ed2" />        

In terms of visualization, a RasterMap class is provided, which can quickly generate corresponding raster maps based on the provided matrix according to the following rules:        

    a) 0 represents a regular grid     
    b) 1 represents the starting grid     
    c) 2 represents the final grid     
    d) 3 represents obstacle grid     
    
In addition, a user interface program written using MVC architecture is provided to visualize the running process of the algorithm.    
In terms of algorithms, A * and Dijkstra algorithms have been implemented based on the Point and PointGroup classes defined in the rastermap module. You can directly use this interface to find the shortest path.   

<table>
	<tr>
		<td>
			<center>
				<img src='https://github.com/YuanshengShe/shortestpathTK/blob/main/interface/astar_gif.gif'/>
				Fig1. A star
			</center>
		</td>
		<td>
			<center>
				<img src='https://github.com/YuanshengShe/shortestpathTK/blob/main/interface/dijkstra_gif.gif'/>
				Fig2. Dijkstra
			</center>
		</td>
	</tr>
</table>

<font color='blue'>About how to use</font>：
1. Clone it onto your computer.
```
git clone git@github.com:YuanshengShe/shortestpathTK.git
```
2. Run the main. py file placed in the interface directory.




