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


def sumif_withdrawals()->list:
    val_w_data=Data._manipulate_val_w(Data._get_all_val_withdrawals())

    df = pd.DataFrame(val_w_data,columns=['address','block','withdraw_rewards','withdraw_commission'])

    sumif=df.groupby('address')[['withdraw_rewards', 'withdraw_commission']].sum()
    sumif.reset_index(inplace=True)
    sumif_list=sumif.values.tolist()
    return sumif_list


def combine_val_rewards_entry():
    values=[]
    # get the create_val list of vals
    create_val_data=Data._get_create_val_event()
    # get all oustanding delegated rewards
    rewards_data=Data._get_val_outstanding_delegated_rewards()
    # get val_comms_data
    val_comms_data=Data._get_val_outstanding_comms()
    # get all withdrawals sumifed
    val_w_data=sumif_withdrawals()
    # remove last 2 entries of timestamp and block height
    for val_entries in create_val_data:
        val_data=list(val_entries)
        del val_data[3:]
        # append outstanding comms data
        for val_comm_data in val_comms_data:
            if val_comm_data[0]==val_data[0]:
                val_data.append(val_comm_data[1])
            else:
                pass
        # append outstanding rewards
        for reward_data in rewards_data:
            if reward_data[0]==val_data[1]:
                val_data.append(reward_data[1])
            else:
                pass
        # sum withdraw_rewards and append
        for w in val_w_data:
            if w[0]==val_data[0]:
                val_data.append(w[2])
                val_data.append(w[1])
            else:
                pass
        values.append(val_data)

    return values


def add_sum_columns():
    validator_earnings=combine_val_rewards_entry()
    validator_earnings_columns=['address','wallet_address','moniker',"oustanding_commisison","outstanding_rewards","withdrawn_commission","withdrawn_rewards"]
    df0 = pd.DataFrame(validator_earnings,columns=validator_earnings_columns)
    df1=df0.fillna(0)
    
    df1["accumulated_commission"]=df1["oustanding_commisison"]+df1["withdrawn_commission"]
    df1["accumulated_rewards"]=df1["outstanding_rewards"]+df1["withdrawn_rewards"]

    df1["total"]=df1["accumulated_commission"]+df1["accumulated_rewards"]

    file_name=File._generate_file_name("validator_earnings")
    df1.to_csv(file_name)
    
    



def main():


    add_sum_columns()




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
