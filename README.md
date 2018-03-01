# CodeMapExtractor

## About 
CodeMapExtractor is a simple tool to extract graph from dgml file. dgml is the file extension of CodeMap generated by Visual Studio which is a special kind of XML. CodeMapExtractor is capable of extracting function call graph beyond classes and namespace provided that a correct dgml file is given. 

## For Further Development
CodeMapExtractor stores the call graph of whole project as a adjacency matrix and a networkx object. You can do any experiment on the adjacency matrix. networkx is rich in graph algorithm, most of the famous graph algorithm like BFS, DFS, Floyd-Warshall, Dijkstra etc algorithm can be invoked with a single line change. 

## How to Generate dgml file
#### Step 1: Open a Visual Studio project
#### Step 2: Right Click on the Project Name on the Solution Explorer
#### Step 3: Click on '''Show on CodeMap'''
#### Step 4: After any graphical object with project name is visible, expand all the nodes recursively by clicking on the expand icon of each graphical unit
#### Step 5: When all the graphical nodes are expanded, Press Ctrl+S or Save using file menu. It will take you to file save dialog where you will see the file to be saved is a dgml file. Save it and feed it to the python script

## Some Graphs generated by CodeMapExtractor on Aletheia Project
![Caller Graph](https://github.com/tum-i22/CodeMapExtractor/blob/master/caller_graph.png "Caller Graph")



![Callee Graph](https://github.com/tum-i22/CodeMapExtractor/blob/master/callee_graph.png "Callee Graph")

![Call Graph](https://github.com/tum-i22/CodeMapExtractor/blob/master/call_graph.png "Full Call Graph")
