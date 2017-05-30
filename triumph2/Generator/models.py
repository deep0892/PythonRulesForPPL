from django.db import models
from mongoengine import *
from enum import Enum

class Workflow(Document):
	workflowName=StringField(max_length=100,required=True)
	bu=StringField(max_length=50,required=True)
	version=IntField()
	developer=StringField(max_length=50,required=True)
	rules=ListField()

#A feature can be an operand or a rule: it will be a rule when it depends on few other features for value determination and it will always be of allocation type
"""
class Operator(Enum):
                EQUALS='equals'
                LT='lt'
                GT='gt'
                LE='le'
                GE='ge'
                NE='ne'
                AND='and'
                OR='or'
                NOT='not'
                SET='set'
                SUBRULE='subrule'
                FEATURE='feature'
                LOOP='loop'
                ADD='add'
                PRODUCT='product'
                SUBTRACT='subtract'
                DIVIDE='divide'
"""

from Utils.TriumphKey import TriumphKey
class Rule(Document):
	ruleName=StringField(max_length=100)
	OPERATOR_TYPE=(TriumphKey.Operator.EQUALS,TriumphKey.Operator.LT,TriumphKey.Operator.GT,TriumphKey.Operator.LE,TriumphKey.Operator.GE,TriumphKey.Operator.NE,TriumphKey.Operator.AND,TriumphKey.Operator.OR,TriumphKey.Operator.NOT,TriumphKey.Operator.SET,TriumphKey.Operator.SUBRULE,TriumphKey.Operator.FEATURE,TriumphKey.Operator.LOOP,TriumphKey.Operator.ADD,TriumphKey.Operator.PRODUCT,TriumphKey.Operator.SUBTRACT,TriumphKey.Operator.DIVIDE)
	operator=StringField(max_length=20,choices=OPERATOR_TYPE)
	operands=ListField()
	preUtils=ListField()	
	index=IntField()
	depth=IntField()
	nextRuleIndex=IntField()
	trueRuleIndex=IntField()
	falseRuleIndex=IntField()

class Operand(Document):
	OPERAND_TYPE=('literal','var','feature','operation')
	opType=StringField(max_length=20,choices=OPERAND_TYPE)
	opTag=StringField(max_length=100)
	subRule=ListField()
	subRuleOps=ListField()

class Util(Document):
	util=StringField(max_length=100)
	data=ListField()
	keys=ListField()

class UtilKey(Document):
	tag=StringField(max_length=100)
	ORDER=('ASC','DESC')
	order=StringField(max_length=10,choices=ORDER)	
