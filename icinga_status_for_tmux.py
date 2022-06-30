#!/usr/bin/python2
import time
import json
import os
import psutil
import sys
from tempfile import NamedTemporaryFile
from pynag.Parsers import status
import paramiko
import yaml
import random

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from pushbullet import Pushbullet

def get_statusfile(label, host, remote_statusfile):
    # ssh to each server in the config, grab the status.dat
    tf = NamedTemporaryFile(prefix='icingastatus-', delete=False)
    tempfilename = tf.name
    tf.close()
    paramiko.util.log_to_file ('paramiko.log')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, timeout=10, port=22)
    ftp = ssh.open_sftp()
    ftp.get(remote_statusfile, tempfilename)
    ftp.close()
    ssh.close()
    return tempfilename

def parse_status(tempfile):
    # parse the status.dat files listed in the config
    # return the status of the servers in a hash
    warning = 0
    critical = 0
    unknown = 0
    color = "#00ff00" # green
    s = status(tempfile)
    s.parse()

    critical_msg = ""

    for service in s.data.get('servicestatus', []):
        if (int(service.get('scheduled_downtime_depth', None)) == 0
                and int(service.get('problem_has_been_acknowledged',
                                    None)) == 0):
            # get all the 'not OK' services
            if (int(service.get('current_state', None)) == 1):
                warning += 1
            elif (int(service.get('current_state', None)) == 2):
                critical += 1
                if (int(service.get('notifications_enabled', None)) == 1):
                    critical_msg = (critical_msg + service.get('host_name') + "\n" +
                                    service.get('service_description') + " \n" +
                                    service.get('plugin_output', None) + "\n\n")

            elif (int(service.get('current_state', None)) == 3):
                unknown += 1
        if critical > 0:
            color = "#ff0000" # red
        elif warning > 0:
            color = "#ffff00"# yellow
    return {'warning': warning, 'critical': critical, 'unknown': unknown, 'color': color}, critical_msg

statusfile = "/var/lib/icinga/status.dat"
regions = [{'label': 'NZ-PPD-1', 'host': 'cc-ppd1-mon0'},
           {'label': 'NZ_WLG_2', 'host': 'cat-wgtn-mon0'},
           {'label': 'NZ-POR-1', 'host': 'cat-por-mon0'},
           {'label': 'NZ-HLZ-1', 'host': 'cat-hlz-mon0'}
          ]


if __name__ == "__main__":

    has_alerted = False

    for region in regions:
        try:
            status_file = get_statusfile(region['label'], region['host'], statusfile)
        except:
            continue

        servicestatus, critical_msg = parse_status(status_file)
        if status_file.startswith('/tmp/icingastatus'):
            os.unlink(status_file)
        text = "{}: #[fg={}]Warn: {} Crit: {}#[fg=default]".format(    #[fg={}] is for setting color in tmux configuration
            region['label'],
            servicestatus['color'],
            servicestatus['warning'],
            servicestatus['critical'])
        print text + " |",
        sys.stdout.flush()

        # send out notification
        if (region['label'] != "Prepro" and critical_msg and ("sleep 60" not in os.popen("ps -Af").read()[:])):
            #pb.push_note("Critical in " + region['label'], critical_msg)
            has_alerted = True

    if has_alerted:
        os.system('sleep 60 &')

    time.sleep(5)

