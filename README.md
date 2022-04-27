to run this script:
1. have python3 installed
2. install requirements by running the following commands: pip install requirements.txt
3. run fxcored config output json 
4. run the command to generate the reports: python3 index.py
5. oh did i mention you also need to have fxcore CLI installed

structure of the reports (if you want to plug in other reports):
1. add in the fxcore CLI command in the "cmd_list.json" file as per the template
2. the Cmd.py module is where all reading of commands and creating message strings and returning the raw_data for running th CLI OS commands from the "cmd_list.json" file
3. Data.py module is where all the various data is generated from. And also where data is being manipulated
4. the Report class in Report.py is where the blueprint of a report object is stored. it will be initialized with REPORT_NAME, file_type, data and other information
5. index.py is where Report objects are being initialized and run
6. all you have to do is run python3 index.py to generate the reports