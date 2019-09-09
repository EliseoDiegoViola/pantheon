
class CriticalExportException(Exception):
    def __init__(self, file, error, details):

        # Call the base class constructor with the parameters it needs
        super(CriticalExportException, self).__init__(error)

        # Now for your custom code...
        self.errorFile = file
        self.errormessage = error
        self.errorDetails = details