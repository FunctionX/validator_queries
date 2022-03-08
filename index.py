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
    val_w_data=Data._manipulate_val_w(Data._get_all_val_withdrawals())
    w_columns=['address','block','withdraw_rewards','withdraw_commission']
    val_w_report=Report("Validator_withdrawals",val_w_data,"csv",w_columns)
    val_w_report.write_to_file()


    val_comms_data=Data._get_val_outstanding_comms()
    comms_columns=['address','commission']
    val_comms_report=Report("Validator_commission",val_comms_data,"csv",comms_columns)
    val_comms_report.write_to_file()

    rewards_data=Data._get_val_outstanding_delegated_rewards()
    rewards_columns=['wallet_address','delegated_rewards']
    rewards_report=Report("Val_self_del_rewards",rewards_data,"csv",rewards_columns)
    rewards_report.write_to_file()

    create_val_data=Data._get_create_val_event()
    create_val_columns=["address","wallet_address","moniker","height","timestamp"]
    create_val_report=Report("Create_val",create_val_data,"csv",create_val_columns)
    create_val_report.write_to_file()


    raw=Data._get_val_fxcored_status()
    dataframe = Data.create_dataframe(data=raw["validators"])
    dataframe.rename(columns={
        "consensus_pubkey.@type": "@type",
        "consensus_pubkey.key": "key",
        "description.moniker": "moniker",
        "description.identity": "identity",
        "description.website": "website",
        "description.security_contact": "security_contact",
        "description.details": "details",
        "commission.update_time": "update_time",
        "commission.commission_rates.rate": "rate",
        "commission.commission_rates.max_rate": "max_rate",
        "commission.commission_rates.max_change_rate": "max_change_rate"
    }, inplace=True)
    dataframe=Data._manipulate_fxcored_status_data(dataframe)
    dataframe.to_csv(File._generate_file_name("fxcored_status"), index=False)

if __name__ == '__main__':
    main()
