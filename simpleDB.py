###############
# Calvin Chan #
###############

# Thumbtack coding challenge

# Stack ADT is to hold the DB and Values (for NUMEQUALTO)
class Stack:
	def __init__(self):
		self.items = []

	def isEmpty(self):
		return self.items == []

	def push(self, item):
		self.items.append(item)

	def pop(self):
		return self.items.pop()

# db holds all the values from SET
db = {}

# This holds the frequency of each variable, for NUMEQUALTO
valDict = {}

# These stacks hold the dbs and valDicts during the transactions
db_Stack = Stack()
val_Stack = Stack()

# Switch for loops
currentInput = ""

def databaseCommands(dataBase, valuesDict, dbStack, valuesStack):
	global currentInput
	
	while currentInput != None:
		currentInput = raw_input()

		# Splits the commands into parts
		dbCommand = currentInput.split(" ")

		if dbCommand[0] == "SET":
			name = dbCommand[1] 
			value = dbCommand[2] 

			# If the item is already in the database,
			# set is mutating this value - thus decrementing
			# the value in valuesDict is necessary
			if dataBase.get(name, 0) != 0:
				currentValue = dataBase[name]
				valuesDict[currentValue] -= 1

			dataBase[name] = value

			if value in valuesDict:
				valuesDict[value] += 1
			else:
				valuesDict[value] = 1

		elif dbCommand[0] == "GET":
		    name = dbCommand[1]

		    if name in dataBase:
		    	print "%s" % dataBase[name]
		    else:
		    	print "NULL"

		elif dbCommand[0] == "UNSET":
			name = dbCommand[1]
			value = dataBase[name]

			del dataBase[name]

			if value in valuesDict:
				valuesDict[value] -= 1

		elif dbCommand[0] == "NUMEQUALTO":
			value = dbCommand[1]

			if value in valuesDict:
				print "%d" % valuesDict[value]
			else:
				print "0"

		elif dbCommand[0] == "END":
			currentInput = None
			
		else:
			# input doesn't correspond to data commands, 
			# it can either be transactional or invalid
			transactionCommands(dbCommand[0], dataBase, valuesDict, dbStack, valuesStack)

def transactionCommands(transactionInput, dataBase, valuesDict, dbStack, valuesStack):

	if transactionInput == "BEGIN":
		# Existing database & valueDict is pushed onto 
		#  the stack for future ROLLBACK reference
		dbStack.push(dataBase.copy())
		valuesStack.push(valuesDict.copy())
		
		databaseCommands(dataBase, valuesDict, dbStack, valuesStack) 
		
	elif transactionInput == "ROLLBACK":
		if dbStack.isEmpty() or valuesStack.isEmpty():
			print "NO TRANSACTION"
		else:
			# Pops off the top of the stack and reinstates the 
			#  dataBase and valuesDict as the previous db/valDict
			dataBase = dbStack.pop() 
			valuesDict = valuesStack.pop() 	

		databaseCommands(dataBase, valuesDict, dbStack, valuesStack)

	elif transactionInput == "COMMIT":
		# Empties the stack, thus committing all the 
		#   changes by erasing the previous dbs and 
		#   valDicts if they are non-empty		
		if dbStack.isEmpty() or valuesStack.isEmpty():
			print "NO TRANSACTION"
			databaseCommands(dataBase, valuesDict, dbStack, valuesStack)
		else:
			dbStack = Stack()
        	valuesStack = Stack()

        	databaseCommands(dataBase, valuesDict, dbStack, valuesStack)

	else:
		print "INVALID INPUT"

databaseCommands(db, valDict, db_Stack, val_Stack)


