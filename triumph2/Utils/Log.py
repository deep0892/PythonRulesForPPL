class Log:
	from enum import Enum
	class PriorityLevel(Enum):
		VERBOSE=1
		ERROR=2
		DEBUG=3

	class bcolors:
	    HEADER = '\033[95m'
	    OKBLUE = '\033[94m'
	    OKGREEN = '\033[92m'
	    WARNING = '\033[93m'
	    FAIL = '\033[91m'
	    ENDC = '\033[0m'
	    BOLD = '\033[1m'
	    UNDERLINE = '\033[4m'		
	
	#priority level to control under what severity to display the log
	#argTuple in case there are any nested arguments within the log string 
	@classmethod
	def log(cls,tag,msgTxt,argTuple=None,priorityLevel=PriorityLevel.VERBOSE):
		print tag+'  :::  ',
		if argTuple is None:
			print msgTxt
		else:
			print msgTxt%argTuple
	@classmethod
	def v(cls,tag,msgTxt,argTuple=None):
		from colored import fg,bg,attr
		Log.log(tag,fg(63)+str(msgTxt)+attr('reset'),None,Log.PriorityLevel.VERBOSE)

	@classmethod
	def d(cls,tag,msgTxt,argTuple=None):
		from colored import fg,bg,attr
		Log.log(tag,fg(22)+str(msgTxt)+attr('reset'),None,Log.PriorityLevel.DEBUG)
	
	@classmethod
	def e(cls,tag,msgTxt,argTuple=None):
		from colored import fg,bg,attr
		Log.log(tag,fg(52)+str(msgTxt)+attr('reset'),None,Log.PriorityLevel.ERROR)
	
