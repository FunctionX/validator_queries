import Data
import File

class Report:

    def __init__(self,REPORT_NAME,data,file_type, columns=[]):
        """
        takes in manipulated data and report name 
        """
        self.REPORT_NAME=REPORT_NAME
        self.data=data
        self.file_type=file_type
        self.file_name=File._generate_file_name(self.REPORT_NAME)
        self.columns=columns
    
    def write_to_file(self):
        if self.file_type=="json":
            File._write_to_json(self.data,self.file_name)
        elif self.file_type=="csv":
            File._write_to_csv(self.data,self.file_name,self.columns)

