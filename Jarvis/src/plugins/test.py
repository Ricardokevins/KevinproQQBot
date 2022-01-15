from nonebot import on_command, require, get_driver
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.message import Message
import nonebot.adapters.cqhttp
import _thread

import paramiko

SERVER_INFO = [
    {'name':"1080ti-4",'ip':"210.28.132.173",'port':22},
    {'name':"1080ti-5",'ip':"210.28.132.174",'port':22},
    {'name':"1080ti-6",'ip':"210.28.132.175",'port':22},
    {'name':"2080ti-1",'ip':"210.28.134.54",'port':22},
    {'name':"TITAN_RTX",'ip':"210.28.134.152",'port':22},
    {'name':"V100-11",'ip':"210.28.133.13",'port':20638},
    {'name':"V100-12",'ip':"210.28.133.13",'port':20658},
    {'name':"V100-13",'ip':"210.28.133.13",'port':20659},
    {'name':"V100-21",'ip':"210.28.133.13",'port':20641},
    {'name':"V100-22",'ip':"210.28.133.13",'port':20644},
    {'name':"V100-23",'ip':"210.28.133.13",'port':20642},
    {'name':"V100-31",'ip':"210.28.133.13",'port':20645},
    {'name':"V100-32",'ip':"210.28.133.13",'port':20646},
    {'name':"V100-33",'ip':"210.28.133.13",'port':20647},
    ]
# 建立连接
PENDING_SERVER = [
    {'name':"2080ti-2",'ip':"210.28.134.55",'port':22}
]
# 建立连接

def parse_using(string):
        using = string[string.index("Processes:"):].split("\\n")[4:-2]
        for i in using:
            print(i)

def parse_GPU(string,server_info = None):
    gpu_index = 0
    GPI_INFO = ""
    for i in string.split("\\n"):
        if "Default" in i:
            info_list = i.split("|")
            GPU_MEMORY = info_list[2]
            USED_GPU_MEMORY = GPU_MEMORY.split("/")[0]
            if(int(USED_GPU_MEMORY.replace("MiB",'')) < 100 ):
                print("GPU {} on {} is Availble".format(gpu_index,server_info['name']))
                GPI_INFO = GPI_INFO + "\n" + "{}  GPU {}".format(server_info['name'],gpu_index)
            gpu_index += 1
    return GPI_INFO.strip()

def check_server(server_info):
    ip = server_info['ip']
    port = server_info['port']
    check_info = ""
    try:
        trans = paramiko.Transport((ip, port))
        trans.connect(username="shesj", password="nlp_shesj")
        ssh = paramiko.SSHClient()
        ssh._transport = trans
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("nvidia-smi")
        string = str(ssh_stdout.read())
        check_info = parse_GPU(string,server_info)
        #parse_using(string)
        # 关闭连接
        trans.close()
        return check_info
    except:
        print("Failed in Server {}".format(server_info['name']))
        return "Failed"

    


scheduler = require('nonebot_plugin_apscheduler').scheduler

@scheduler.scheduled_job('interval', seconds = 1800)
async def demo():
    (bot,) = nonebot.get_bots().values()
    GPU_INFO = "GPU Info: "
    succ = 0
    fail = 0
    for i in SERVER_INFO:
        check_info = check_server(i)
        if check_info != "Failed":
            succ += 1
            if check_info != "":
                GPU_INFO = GPU_INFO + "\n" + check_info  
        else:
            fail +=1
    
    if succ + fail != len(SERVER_INFO):
        print("===================== HIT BUG =====================")

    print("SUCC {} FAIL {}".format(succ, fail))
    if GPU_INFO == "GPU Info: ":
        GPU_INFO = "None Available"
    await bot.send_private_msg(user_id=3121416933,message=GPU_INFO)
    
        