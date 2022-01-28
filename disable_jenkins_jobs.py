#!/usr/bin/python
# author: Shubham Setia
# description: This script alerts for all disabled autoscaling jobs on jenkins
import requests
import json
import sys
import argparse

## Global Variables
jenkins_autoscaling_jobs = "https://jenkins.example.com/view/Autoscaling%20Jobs/api/json"
jenkins_job_url_prefix = "https://jenkins.example.com/job/"
jenkins_job_url_suffix = "/api/json"

def parse_args():
    """
        Script to check all disabled autoscaling jobs on jenkins
        This script takes two arguments i.e. username and apitoken
        -u or --username and -t or --token as an argument
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', '-u', help='Jenkins username', required=True)
    parser.add_argument('--token', '-t', help='Jenkins user api token', required=True)
    args = parser.parse_args()
    return args

def connect(username, token):
    session = requests.Session()
    session.auth = (username, token)
    return session

def get_job_name(endpoint, username, token):
    get_all_jobs = connect(username, token).get(endpoint)
    result = get_all_jobs.json()
    return result

def main():
    exitcode = 0
    args = parse_args()
    result = get_job_name(jenkins_autoscaling_jobs, args.username, args.token)
    disabled_jobs = []

    for job in result['jobs']:
        job_name = job['name']
        url_endpoint = jenkins_job_url_prefix + job_name + jenkins_job_url_suffix
        get_job_data = connect(args.username, args.token).get(url_endpoint)
        JOB_RESULT = get_job_data.json()
        if not JOB_RESULT['buildable']:
            disabled_jobs.append(job_name)
            exitcode =2
    if exitcode == 2:
        print "CRITICAL: Following autoscaling jobs are disabled:\n", disabled_jobs
    else:
        print "OK: no autoscaling jobs are disabled."
    sys.exit(exitcode)

if __name__ == '__main__':
    main()

