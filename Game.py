##########################################
# AUTHOR		: ADIL TANVEER
# LANGUAGE		: PYTHON3
# DESCRIPTION	: This module simulates the Game of Life
#				  For details of the game refer https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#Rules

# MODULE_DESCRIPTION("My kernel module - mykmod");
# MODULE_AUTHOR("es17btech11026 [at] gmail.com");
# MODULE_LICENSE("GPL")

###########################################
# LIBRARIES USED IN THIS MODULE

import getopt
import sys
import numpy as np
import matplotlib.animation as animation

from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

############################################

def about():
	percentSign = "%"
	print("DESCRIPTION :")
	print("1. This module simulates the Game of Life")
	print("2. For details of the rules of the game refer https://en.wikipedia.org/wiki/Conway" \
				+ percentSign + "27s_Game_of_Life#Rules")
	print("3. The initial state of the universe is either random or has to be given as an input in a text file (only)")
	print("4. The input file should only contain a 2D matrix of space separated integers with rows being separated by a newline")
	print("5. For knowing the details of execution and operation of the module type the command:\n\tpython3 <filename> --usage")

def usageManual(height, width, fps):
	print("USAGE MANUAL\n")

	print("SYNTAX:\npython3 <filename> [OPTION1][ARGUMENT1] [OPTION2][ARGUMENT2] ...\n")

	print("OPTIONS:")
	print("1. -h <height : type = int>")
	print("Eg: python3 <filename> -h 10\n")

	print("2. -w <width : type = int>")
	print("Eg: python3 <filename> -w 10\n")

	print("3. -f <fps : type = int>")
	print("Eg: python3 <filename> -f 5\n")	

	print("LONG OPTIONS:")
	print("1. --usage")
	print("Eg: python3 <filename> --usage\n")
	
	print("2. --file <filename : type = string>\t (Note : File must be text file)")
	print("Eg: python3 <filename> --file input.txt\t (Note : File must be present in the working directory)\n")

	print("3. --help")
	print("Eg: python3 <filename> --help\n")

	print("4. --about")
	print("Eg: python3 <filename> --about\n")

	print("EXAMPLE EXECUTION :\npython3 <filename> -h 10 -w 10 -f 5 --file data.txt\n")

	print("DEFAULT OPTIONS: ")
	print("Default height = %d"%(height))
	print("Default width = %d"%(width))
	print("Default fps = %d"%(fps))
	print("Default input is a randomly generated matrix of dimension: height x width\n")

	print("OPERATION:")
	print("Step 1: Execute the MODULE from the CLI using the above instructions")
	print("Step 2: A window will open with the initial configuration of the universe")
	print("Step 3: Press Start button at the bottom to start the animation")
	print("Step 4 (optional) : Press Stop to pause the animation at any point of time")
	print("Step 5: Click the cross icon to close the window and exit the module")

def readInput():
	
	global height
	global width
	global fps
	global readFlag

	try: 
		# Parsing argument 
		arguments, values = getopt.getopt(argumentList, options, longOptions) 

		# checking each argument 
		for currentArgument, currentValue in arguments: 

			if currentArgument == "-h":
				height = int(currentValue) 

			elif currentArgument == "-w": 
				width = int(currentValue) 

			elif currentArgument == "-f": 
				fps = int(currentValue) 

			elif currentArgument == "--usage":
				usageManual(height, width, fps)
				exit(0)

			elif currentArgument == "--file":
				fileName = str(currentValue)
				readFlag = True

			elif currentArgument == "--help":
				print("For usage of this module type the command :\npython3 <filename> --usage\n")
				print("For description of this module type the command :\npython3 <filename> --about")
				exit(0)

			elif currentArgument == "--about":
				about()
				exit(0)	

	except getopt.error as err:
		print ("Error: Invalid input\nPlease read the usage of this module")
		print("Command: \npython3 <filename> --usage")
		exit(1)

	if readFlag == True:
		try:
			inputUniverse = np.loadtxt(fileName, dtype = int)
			height = np.size(inputUniverse,0)
			width = np.size(inputUniverse,1)
		except:
			print("Error:\nFile not found")
			exit(1)	
	else:
		inputUniverse = np.random.randint(2, size = (height, width))

	return inputUniverse	

class Game:
	
	# INIT FUNCTION

	def __init__(self, inputRoot, inputUniverse, inputFps):
		
		
		#  Setup required for built-in logic
		self.pause = True		# For pausing the animation whenever required
		self.universe = inputUniverse
		self.AliveCells = []
		
		# Display parameters
		self.fps = inputFps
		
		# Initialize the AliveCells list
		self.whoAllAreAlive()

		# Root Setup
		self.root = inputRoot
		self.root.title("Game Of Life")

		# Setup for animation
		self.fig = Figure()
		self.label = Label(root, text = 'Game of Life Simulation', font = ('Verdana', 15))\
																			.pack(side = TOP, pady = 10) 		
		self.canvas = FigureCanvasTkAgg(self.fig, master = self.root)
		self.canvas.get_tk_widget().pack(side = TOP, fill = BOTH, expand = 1)
		self.ax = self.fig.add_subplot(111)
		self.im = self.ax.imshow(inputUniverse, interpolation = 'none')

		# Animation
		self.anim = animation.FuncAnimation(self.fig, self.animateFunc, interval = 1000 / self.fps,)


		# Start and Stop Buttons
		self.stopButton = ttk.Button(self.root, text="Stop", \
							command=lambda: self.stopButtonPress()).pack(side=BOTTOM, fill=BOTH,\
																		 padx=5, pady=5, expand=1)		
		self.startButton = ttk.Button(self.root, text="Start", \
							command=lambda: self.startButtonPress()).pack(side=BOTTOM, fill=BOTH,\
																			 padx=5, pady=5, expand=1)	


	#########################################################
	# CORE LOGIC 

	def whoAllAreAlive(self):
		AliveCells = []
		
		rowRange = range(0,np.size(self.universe,0))
		colRange = range(0,np.size(self.universe,1))

		for rowInd in rowRange:
			for columnInd in colRange:
				if self.universe[rowInd][columnInd] == 1:
					indexTuple = tuple([rowInd,columnInd])
					AliveCells.append(indexTuple)

		self.AliveCells = AliveCells

	def getNbrs(self, cell):
		Nbrs = []

		rowBound = np.size(self.universe,0)
		colBound = np.size(self.universe,1)

		for i in range(max(0, cell[0] - 1), min(rowBound, cell[0] + 2)):
			for j in range(max(0, cell[1] - 1), min(colBound, cell[1] + 2)):
				if (i, j) != cell:
					Nbrs.append(tuple([i,j]))           									
		return Nbrs

	def fate(self, cell, Nbrs):
		countOfAliveNbrs = 0
		
		for nbr in Nbrs:
			if self.universe[nbr[0]][nbr[1]] == 1 :
				countOfAliveNbrs += 1

		if self.universe[cell[0]][cell[1]] == 1 and countOfAliveNbrs in [2,3]:
			retValue = 1
		elif self.universe[cell[0]][cell[1]] == 1 and countOfAliveNbrs not in [2,3]:
			retValue = 0
		elif self.universe[cell[0]][cell[1]] == 0 and countOfAliveNbrs == 3:
			retValue = 1
		else:
			retValue = 0

		return retValue

	def transition(self):
		DeadCellsExplored = {}
		NextGenAliveCells = []

		for cell in self.AliveCells:
			Nbrs = self.getNbrs(cell)

			for nbr in Nbrs:
				if self.universe[nbr[0]][nbr[1]] == 0 and nbr not in DeadCellsExplored:
					nbrNbrs = self.getNbrs(nbr)
					NextGenFate = self.fate(nbr, nbrNbrs)
					DeadCellsExplored[nbr] = NextGenFate
					if NextGenFate == 1:
						NextGenAliveCells.append(nbr)

			cellFate = self.fate(cell, Nbrs)
			if cellFate == 1:
				NextGenAliveCells.append(cell)
		self.AliveCells = NextGenAliveCells
	
	def updateUniverse(self):
		rowBound = np.size(self.universe,0)
		colBound = np.size(self.universe,1)

		newUniverse = np.zeros((rowBound, colBound))
		
		for cell in self.AliveCells:
			newUniverse[cell[0]][cell[1]] = 1

		self.universe = newUniverse

	# END OF CORE LOGIC
	##########################################################

	# Animation Function
	def animateFunc(self, i):
		if not self.pause:
			self.transition()
			self.updateUniverse()
			self.im.set_array(self.universe)
		return [self.im]


	# Defining Action when corresponding buttons are pressed
	def startButtonPress(self):
		self.pause = False

	def stopButtonPress(self):
		self.pause = True

############################################
# Driver Code

# INPUT PARAMETERS
argumentList = sys.argv[1:]
options = "h:w:f:"
longOptions = ["usage", "help", "about", "file="]

# Default Values
height 	= 15
width 	= 15
fps 	= 3
readFlag = False

# Read input
inputUniverse = readInput()
# print("INPUT:\n",inputUniverse)

# Run the simulation
root = Tk()
game = Game(root, inputUniverse, fps)
root.mainloop()

# END OF DRIVER CODE
#############################################