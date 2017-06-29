import copy

class graph:
	"""A representation of a bayesian network.
	
	This gives a representation of a bayesian network. Note that it
	will initialize with the edges between the attribute whose 
	probability we seek and every other attribute.
	
	Attributes:
		labels: A list containing the names of all nodes on the graph
		edges: a dictionary whose keys are the labels of the nodes and
				whose corresponding values are a list of all node that
				have edges such that the key is a parent of the node
		primary: the attribute whose probability we sekk
	"""	
	def __init__(self, labs, primary = None, edges = {}):
		"""Initializes the network
		
		If no primary node is specified it selects the first node in the list
		of labels (and raises a ValueError if the primary node is specified to 
		something not in the graph), and if edges are specified it is assumed
		that the edges between the primary node all other nodes are already given.
		"""
		if primary == None:
			primary = labs[0]
		if primary not in labs:
			raise ValueError("Primary value must be in the graph")
		self.labels = labs
		self.primary = primary
		self.edges = edges
		if self.edges == {}:
			for vertex in self.labels:
				self.edges[vertex] = []
			for vertex in self.edges:
				if vertex != primary:
					self.edges[primary].append(vertex)
	
	def addEdge(self, parent, child):
		"""Adds and edge to the Bayesisan network.
		
		Args:
			parent: the proposed parent vertex
			child: the proposed child vertex
		
		Raises:
			ValueError: If one of either the parent or the child is not
						in the graph or if the proposed parent is a child
						of the proposed child.
	"""
		if (parent in self.labels) and (child in self.labels):
			if parent not in self.edges[child]:
				self.edges[parent].append(child)
			else:
				raise ValueError("Parent cannot be the child of the child")
		else:
			raise ValueError("Parent or Child is not in the graph")
			
	def printGraph(self, filename=None):
		"""Outputs the graph
		
		Args:
			filename: The file to output the graph to, will print to screen
						if not specified
		"""
		out = []
		for parent in self.edges:
			for child in self.edges[parent]:
				out.append("{} \t -> \t {}".format(parent, child))
		if filename is not None:
			file = open(filename, 'w')
			for line in out:
				file.write(line)
		else:
			for line in out:
				print(line)
	
	def copyGraph(self):
		"""Creates a graph that's a copy of the current graph
		
		Returns:
			temp: A graph that's a copy of the current graph (note, the new graph
					is a copy such that the attributes do NOT point to the same values.)
		"""
		temp = graph(copy.deepcopy(self.labels), primary = self.primary, edges = copy.deepcopy(self.edges))
		return temp