import subprocess
import json
import csv
from csv import DictWriter
import datetime
import pandas as pd
import Cmd
import Data
from Report import Report
import File




def main():


    Data.val_earnings_w_sum_columns()



    dataframe=Data.get_val_token_info()
    dataframe.to_csv(File._generate_file_name("fxcored_status"), index=False)

if __name__ == '__main__':
    main()
