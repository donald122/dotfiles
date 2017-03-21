#!/usr/bin/python
from time import time
import json
import os
import sys
from tempfile import NamedTemporaryFile
from pynag.Parsers import status
import paramiko
import yaml

def get_statusfile(label, host, username, remote_statusfile):
    # ssh to each server in the config, grab the status.dat
    tf = NamedTemporaryFile(prefix='icingastatus-', delete=False)
    tempfilename = tf.name
    tf.close()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, timeout=10, port=22)
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
    color = "green"
    s = status(tempfile)
    s.parse()
    for service in s.data.get('servicestatus', []):
        if (int(service.get('scheduled_downtime_depth', None)) == 0
                and int(service.get('problem_has_been_acknowledged',
                                    None)) == 0):
            # get all the 'not OK' services
            if (int(service.get('current_state', None)) == 1):
                warning += 1
            elif (int(service.get('current_state', None)) == 2):
                critical += 1
            elif (int(service.get('current_state', None)) == 3):
                unknown += 1
        if critical > 0:
            color = "red"
        elif warning > 0:
            color = "yellow"
    return {'warning': warning, 'critical': critical, 'unknown': unknown, 'color': color}

statusfile = "/var/lib/icinga/status.dat"
username = "donaldleung"
regions = [{'label': 'Prepro', 'host': 'tst-wgtn-mon0'},
           {'label': 'NZ_WLG_2', 'host': 'cat-wgtn-mon0'},
           {'label': 'NZ-POR-1', 'host': 'cat-por-mon0'},
           {'label': 'NZ_HLZ-1', 'host': 'cat-hlz-mon0'},
          ]

if __name__ == "__main__":

    for region in regions:
        status_file = get_statusfile(region['label'], region['host'], username, statusfile)
        servicestatus = parse_status(status_file)
        if status_file.startswith('/tmp/icingastatus'):
            os.unlink(status_file)
        text = "{}: #[fg={}]Warn: {} Crit: {}#[fg=default]".format(    #[fg={}] is for setting color in tmux configuretion
            region['label'],
            servicestatus['color'],
            servicestatus['warning'],
            servicestatus['critical'])
        print text + " |",

