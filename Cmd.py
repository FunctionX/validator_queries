import subprocess
import json



def _filter_cmd(cmd_name,cmd_list):
    cmd_list=json.load(open(cmd_list))
    cmd=cmd_list[cmd_name]
    return cmd


def _get_raw_data(cmd):
    """
    CLI command to return raw_data output
    """
    data=subprocess.run(cmd,stdout=subprocess.PIPE)
    # change byte to string
    data_decode=data.stdout.decode('utf-8')
    dict_data=json.loads(data_decode)
    return dict_data


def _create_msg_string(val_add:str,msg_action:str):
    """
    takes in validator address and msg action string
    """
    msg_string=f"message.sender={val_add}&message.action={msg_action}"
    return msg_string

def _q_tx_events(msg):
    """
    takes in the msg to say withdraw_validator commission and fill the rest of the flags and commands and pass it into the CLI
    """
    # fxcored query txs --events 'message.sender=fxvaloper1c4glwxgvs5vjx9j2w4ef7r4480cfs2dkv7h8u2&message.action=withdraw_validator_commission' --node https://fx-json.functionx.io:26657
    raw_data=subprocess.run(["fxcored","q","txs","--events",msg,"--node=https://fx-json.functionx.io:26657"],stdout=subprocess.PIPE)
    return raw_data