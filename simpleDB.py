class Stack:
	def __init__(self):
		self.items = []

	def isEmpty(self):
		return self.items == []

	def push(self, item):
		self.items.append(item)

	def pop(self):
		return self.items.pop()

db = {}
valDict = {}
db_Stack = Stack()
val_Stack = Stack()

currentInput = ""

def databaseCommands(dataBase, valuesDict, dbStack, valuesStack):
	global currentInput
	
	while currentInput != None:

		currentInput = raw_input()

		dbCommand = currentInput.split(" ")

		if dbCommand[0] == "SET":
			name = dbCommand[1] 
			value = dbCommand[2] 
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
			## search values dict
			value = dbCommand[1]

			if value in valuesDict:
				print "%d" % valuesDict[value]
			else:
				print "0"

		elif dbCommand[0] == "END":
			currentInput = None
			
		else:
			transactionCommands(dbCommand[0], dataBase, valuesDict, dbStack, valuesStack)

def transactionCommands(transactionInput, dataBase, valuesDict, dbStack, valuesStack):

	if transactionInput == "BEGIN":
		## Opens a new transaction block
		## Transaction blocks can be nested

		# previous db and values is pushed onto the stack
		# saved in case of a rollback
		dbStack.push(dataBase.copy())
		valuesStack.push(valuesDict.copy())
		
		databaseCommands(dataBase, valuesDict, dbStack, valuesStack) 
		
	elif transactionInput == "ROLLBACK":
		## Undo all of the commands issued in the most recent transaction block
		## and close the block. Print Nothing if successful, or print "NO TRANSACTION"
		## if no transaction is in progress

		if dbStack.isEmpty() or valuesStack.isEmpty():
			print "NO TRANSACTION"
		else:
			# revive last db and values from stack
			dataBase = dbStack.pop() # not popping the right database
			valuesDict = valuesStack.pop() 	

		databaseCommands(dataBase, valuesDict, dbStack, valuesStack)

	elif transactionInput == "COMMIT":
		## Close all open transaction blocks, permanently 
		##    applying the changes made in them. 
		## Print nothing if successful, or 
		##    print NO TRANSACTION if no transaction is in progress.

		if dbStack.isEmpty() or valuesStack.isEmpty():
			print "NO TRANSACTION"
			databaseCommands(dataBase, valuesDict, dbStack, valuesStack)
		else:
			# empty both stacks, 
			#  new database and values have been committed
			dbStack = Stack()
        	valuesStack = Stack()

        	databaseCommands(dataBase, valuesDict, dbStack, valuesStack)
	
	else:
		print "INVALID INPUT"

databaseCommands(db, valDict, db_Stack, val_Stack)


