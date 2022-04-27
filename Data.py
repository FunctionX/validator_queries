import Cmd
import requests
import json
import utils
import pandas as pd


def _get_val_list()->list:
    """
    create a list of validator addresses with prefix fxvaloper
    """
    cmd=Cmd._filter_cmd("validator_info","cmd_list.json")
    data=Cmd._get_raw_data(cmd)
    val_add_list=[]
    for d in data["validators"]:
        val_add_list.append(d["operator_address"])
    return val_add_list

# ---------------birthday and corresponding addresses for validators---------

def _get_create_val_event():
    """
    get all validator birthdate and corresponding wallet address
    """
    # ---------------for validators created after genesis---------
    validators=[]
    cmd=Cmd._filter_cmd("create_val","cmd_list.json")
    data=Cmd._get_raw_data(cmd)
    for create_val in data["txs"]:
        address=create_val["logs"][0]["events"][0]["attributes"][0]["value"]
        wallet_address=create_val["logs"][0]["events"][1]["attributes"][2]["value"]
        moniker=create_val["tx"]["body"]["messages"][0]["description"]["moniker"]
        height=create_val["height"]
        timestamp=create_val["timestamp"]
        validators.append((address,wallet_address,moniker,height,timestamp))
    #----------------for genesis----------------------------- 
    f = open('genesis.json')
    data = json.load(f)
    for i in data['data']:
        address=i[2]
        wallet_address=i[1]
        moniker=i[0]
        height=0
        timestamp="2021-07-05T04:00:00Z"
        validators.append((address,wallet_address,moniker,height,timestamp))

    return validators

#------------------validator rewards-----------------------------
def _get_val_outstanding_comms():
    """
    get outstanding comms for validator
    """
    values=[]
    val_list=_get_val_list()
    for val in val_list:
        cmd=Cmd._filter_cmd("val_outstanding_comms","cmd_list.json")
        cmd[4]=val
        commission_data=Cmd._get_raw_data(cmd)
        if len(commission_data["commission"])>0:
            commission=float(commission_data["commission"][0]["amount"])/10**18
        else:
            commission=0
        values.append((val,commission))
    return values

def _get_val_outstanding_delegated_rewards():
    """
    get delegated rewards
    """
    values=[]
    val_info=_get_create_val_event()
    for v in val_info:
        wallet_address=v[1]
        cmd=Cmd._filter_cmd("delegator_rewards","cmd_list.json")
        cmd[4]=wallet_address
        
        rewards_data=Cmd._get_raw_data(cmd)
        if len(rewards_data["rewards"])>0:
            rewards=float(rewards_data["total"][0]["amount"])/10**18
        else:
            commission=0
        values.append((wallet_address,rewards))
    return values

# _get_val_outstanding_delegated_rewards()


def _get_all_val_withdrawals():
    """
    filters out all validator withdrawals "withdraw_rewards" & "withdraw_commission" and returns it in a dictionary with the following format:
      [
      {
        "fxvaloper1u2736s9hm43ds6xxje0d2qhhy2m56akaf8up7t": {
            "3159434": {
                "withdraw_rewards": "11552361789042999846400FX",
                "withdraw_commission": "23699689167352852164225FX"
            }
        }
    },
    {
        "fxvaloper1umj9xqdv7q2quvtks8j66mwrj9wcfqp4486qgn": {
            "2681576": {
                "withdraw_rewards": "350840103035052000FX",
                "withdraw_commission": "1403062229124345928FX"
            },
            "2897873": {
                "withdraw_rewards": "5199425185789476500FX",
                "withdraw_commission": "32675461989113084503FX"
            },
            "2948881": {
                "withdraw_rewards": "9656169816245352000FX",
                "withdraw_commission": "38899317032588483569FX"
            },
            "3120109": {
                "withdraw_rewards": "32454562953435984000FX",
                "withdraw_commission": "116041948186529137740FX"
            },
            "3328120": {
                "withdraw_rewards": "1853210859617480FX",
                "withdraw_commission": "198871256725641601371FX"
            }
        }
        ]
    """
    val_list=_get_val_list()
    msg_action="withdraw_validator_commission"
    all_val_withdrawals=[]
    for val in val_list:
        val_withdrawals={}
        msg=Cmd._create_msg_string(val,msg_action)
        cmd=Cmd._filter_cmd("val_withdrawals","cmd_list.json")
        cmd[4]=msg
        withdraw_events=Cmd._get_raw_data(cmd)
        withdrawals={}
        for tx in withdraw_events["txs"]:
            withdrawals[tx["height"]]={}
            for log in tx["logs"]:
                for event in log["events"]:
                    if event["type"]=="withdraw_rewards":
                        for attribute in event["attributes"]:
                            if attribute["key"]=='amount':
                                withdrawals[tx["height"]]["withdraw_rewards"]=attribute['value']
                    if event["type"]=="withdraw_commission":
                        withdrawals[tx["height"]]["withdraw_commission"]=event["attributes"][0]["value"]
                    else:
                        pass

        val_withdrawals[val]=withdrawals
        all_val_withdrawals.append(val_withdrawals)
    return all_val_withdrawals

def _manipulate_val_w(all_val_withdrawals:dict):
    all_withdrawals=all_val_withdrawals
    values=[]
    for dictionary in all_withdrawals:
        for address, blocks in dictionary.items():
            for block_height, block in blocks.items():
                withdraw_rewards = block["withdraw_rewards"][0:-2]
                withdraw_commission = block["withdraw_commission"][0:-2]
                withdraw_rewards=utils._convert_value_into_human_readable(withdraw_rewards)
                withdraw_commission=utils._convert_value_into_human_readable(withdraw_commission)
                values.append((address, block_height, withdraw_rewards, withdraw_commission))
    return values


#-------------------------validator status--------------------------------

def _get_val_fxcored_status()->dict:
    """
    query all status for validators
    """
    cmd=Cmd._filter_cmd("validator_info","cmd_list.json")
    data=Cmd._get_raw_data(cmd)
    return data

def create_dataframe(data: list) -> pd.DataFrame:
  
    # Declare an empty dataframe to append records
    dataframe = pd.DataFrame()
  
    # Looping through each record
    for d in data:
          
        # Normalize the column levels
        record = pd.json_normalize(d)
          
        # Append it to the dataframe 
        dataframe = dataframe.append(record, ignore_index=True)
  
    return dataframe

def _manipulate_fxcored_status_data(data:pd.DataFrame):
    df=data
    del df['@type']
    df['tokens']= df["tokens"].astype(float)
    df['tokens']=df['tokens']/(10**18)
  
    df['delegator_shares']= df["delegator_shares"].astype(float)
    df['delegator_shares']=df['delegator_shares']/(10**18)
   

    df['min_self_delegation']= df["min_self_delegation"].astype(float)
    df['min_self_delegation']=df['min_self_delegation']/(10**18)
    
    del df['identity']

    df[['rate',"max_rate","max_change_rate"]]= df[['rate',"max_rate","max_change_rate"]].apply(pd.to_numeric)
    df[['rate',"max_rate","max_change_rate"]]=df[['rate',"max_rate","max_change_rate"]]*100

    return df

