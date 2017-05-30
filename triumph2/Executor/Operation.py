class Operation:
	TAG='Operation'
	def __init__(self,operation,operands):
		self.operation=operation
		self.operands=operands

	def operate(self):	
		from Utils.TriumphKey import TriumphKey
		from Utils.Log import Log
		if self.operation == TriumphKey.Operator.EQUALS:
			if len(self.operands)==2:
				return self.operands[0]==self.operands[1]
			else:
				return False
		elif self.operation == TriumphKey.Operator.LT:
			if len(self.operands)==2:
				return self.operands[0]<self.operands[1]
			else:
				return False
		elif self.operation == TriumphKey.Operator.GT:
			if len(self.operands)==2:
				return self.operands[0]>self.operands[1]
			else:
				return False
		if self.operation == TriumphKey.Operator.LE:
			if len(self.operands)==2:
				return self.operands[0]<=self.operands[1]
			else:
				return False
		elif self.operation == TriumphKey.Operator.GE:
			if len(self.operands)==2:
				return self.operands[0]>=self.operands[1]
			else:
				return False
		elif self.operation == TriumphKey.Operator.NE:
			if len(self.operands)==2:
				return self.operands[0]!=self.operands[1]
			else:
				return False
		elif self.operation == TriumphKey.Operator.AND:
			if len(self.operands)==2:
				return self.operands[0] and self.operands[1]
			else:
				return False
		elif self.operation == TriumphKey.Operator.OR:
			if len(self.operands)==2:
				return self.operands[0] or self.operands[1]
			else:
				return False
		elif self.operation == TriumphKey.Operator.NOT:
			if len(self.operands)==2:
				return self.operands[0] is not None
		elif self.operation == TriumphKey.Operator.PRODUCT:
			product=1
			if len(self.operands)>=2:
				for operand in self.operands:
					product=product*operand
			return product
		else:
			Log.e(Operation.TAG,'Invalid set of inputs'+str(self.operands)+str(self.operation))
			return False
			
