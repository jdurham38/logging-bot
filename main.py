import base64
import subprocess
import os
import sys 
import time
import logging
import platform


from email import errors
from email.mime.text import MIMEText
from re import split
from multiprocessing import Process


def get_pings(ip):
    print(os.system(f'ping {ip} -c 3'))

def ping(host):
  
    ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"
    args = "ping " + " " + ping_str + " " + host
    need_sh = False if  platform.system().lower()=="windows" else True

    return subprocess.call(args, shell=need_sh) == 0


def handle_data(name, recieved, sent):
    THRESHOLDS = {
        "Bytes": [2000000000, 3500000000],
        "Unicast packets": [300000, 2000000],
        "Non-unicast packets": [15000, 90000],
        "Discards": [3, 5],
        "Errors": [2, 5]
    }

    if THRESHOLDS[name][0] < int(recieved) or THRESHOLDS[name][1] < int(sent):
        if name == "Errors" or name == "Discards":
            message = build.email("csaragon1941@eagle.fgcu.edu","sysadmin@gmail.com",
                f"Problem with {name} on server", 
                f"Warning {name}: Sent or Recieved too large at (r,s) {recieved}, {sent}")
            send_email("fake",message)
        print(f"Warning {name}: Sent or Recieved too large at (r,s) {recieved}, {sent}")

    else:
       print(f"Good {name} at (r,s) {recieved}, {sent}")

def build_email(to, subject, message):
    message = MIMEText(message)
    message['to'] = to
    message['from'] = "fakeemail@gmail.com"
    message['subject'] = "subject"
    return {'raw': base64.urlsafe_b64encode(message.es_string())}

def send_email(service, message):
    try:
        message = (service.users()
            .messages()
            .send(userID="fakeemail@gmail.com", body=message)
            .execute())
        print(f"message ID: {message['id']}")
        return message
    except errors.httpError as err:
        print(f"an error has occurred {err}")

def stuff_function(somelist):
    logging.info(f', ' .join([str(i) for i in somelist]))



if __name__ == "__main__":
    start = time.time()
    PERIOD_OF_TIME = 7200 # 120 min

while True :
    try:
        logfile = sys.argv[1]
    except IndexError:
        logfile = "standardlog.log"

    proto_stats = subprocess.run(["netstat", "-m"], text=True, capture_output = True)

    logging.basicConfig(format="%(asctime)s: %(message)s", level = logging.INFO, 
    datefmt="%d/%m/%Y %H: %M: %S:", filename=logfile)

    logging.info("starting")
    ctr = 1
    for ip in sys.argv[1:]:
        Process(target=get_pings, args=(ip,)).start()
        print(ping('example.com'))
        if ctr < 5:
            ctr += 1
            continue
        else:
            print("ping attempt failed")


    ctr2 = 1
    if proto_stats.returncode == 0 :
        for line in proto_stats.stdout.splitlines() or ip:
            if ctr2 < 5:
                ctr2 += 1
                continue


            raw = split('\s\W+', line)
            print(raw)
            print(Process())
            
                
    else:
        print("command failed")

    logging.info("complete")
    if time.time() > start + PERIOD_OF_TIME : break


 
    
