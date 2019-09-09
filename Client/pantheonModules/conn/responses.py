

class ServerResponse():

	def __init__(self,head = None,body = None,returnCode = 0,errorCode = 0,errorMessage = None):
		self.header = head
		self.body = body
		self.returnCode = returnCode
		self.errorCode = errorCode
		self.errorMessage = errorMessage

		self.objects = None


	def __repr__(self):
		 returnString = ""
		 returnString = returnString + "Header > {0} \n".format(self.header)
		 returnString = returnString + "Body > {0} \n".format(self.body)
		 returnString = returnString + "Return Code > {0} \n".format(self.returnCode)
		 returnString = returnString + "Error Code > {0} \n".format(self.errorCode)
		 returnString = returnString + "Error Message > {0} \n".format(self.errorMessage)
		 return returnString