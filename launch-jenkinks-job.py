#!/usr/bin/env python
import sys
import jenkinsapi
from jenkinsapi.jenkins import Jenkins
import time
import yaml

config = yaml.load(file('/etc/launch-jenkinks.yml'))

jenkins_url = config['jenkins_url']
jenkins_user = config['jenkins_user']
jenkins_token = config['jenkins_token']

def get_server_instance():
    server = Jenkins(jenkins_url, username = jenkins_user, password = jenkins_token)
    return server

def wait_job(jobname):
    server = get_server_instance()
    job = server.get_job(jobname)
    build = job.invoke()
    print "Launch build %s" % build.job.name
    build.block_until_not_queued(1200, 2)
    print "Build %s #%s in progress" % (build.job.name, build.get_build_number())
    build.block_until_completed(1200, 2)
    status = build.job.get_build(build.build_number).get_status()
    if status == 'SUCCESS':
        print status
	return 0
    else:
        print status
	return 1

if __name__ == '__main__':
	project = sys.argv[1]
	sys.exit(wait_job(project))
