#! /usr/bin/python
'''
Created on 2015-1-13

@author: XuXinkun

This script is used to tar the files under /export to /export_package.tar and remove /export.  
'''
import logging
import os
import sys

logging.basicConfig(filename=('/tmp/pack_docker.log'), level=logging.DEBUG, \
                    format="%(asctime)s [%(name)s] %(levelname)s %(module)s %(funcName)s %(message)s", \
                    datefmt="%d %b %Y %H:%M:%S")
logger = logging.getLogger(__name__)

def perform(command, path=None):
    if path:
        logger.debug("path is %s" % path)
    if command:
        import subprocess
        if logger.isEnabledFor(logging.INFO):
            logger.info("========perform command %s =========" % command)
        tmpfile = open("/tmp/output.log", "w")
        p = subprocess.Popen(command, shell=True, close_fds=True, \
#                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT,\
                             stdout=tmpfile, stderr=subprocess.STDOUT, \
                             cwd=path)
        p.wait()
        tmpfile.close()
        status = p.returncode  
        p.stdout = open("/tmp/output.log", "r")
        out = ""
        curline = p.stdout.readline()
        while curline:
            out = out + curline
            curline = p.stdout.readline() 
                    
        logger.debug("result status is %s,output is %s" % (status, out))
        return status , out

        
def pack_docker():
    current_dir = sys.path[0]
    rpm_source = os.path.join(current_dir, "rpmbuild", "SOURCES")
    rpm_buildroot = os.path.join(current_dir, "rpmbuild", "BUILDROOT")
    perform("rm -rf %s" % rpm_buildroot)
    rpm_build = os.path.join(current_dir, "rpmbuild", "BUILD")
    perform("rm -rf %s" % rpm_build)
    docker_src_base_dir = os.path.dirname(os.path.dirname(current_dir))
    status, version = perform("cat %s" % os.path.join(docker_src_base_dir,"VERSION"))
    if status != 0:
        return
    version = version.strip()
    temp_dir = 'docker-%s' % version
    src_package = 'v%s.tar.gz' % version
    if os.path.exists("/tmp/%s" % temp_dir):
        perform("rm -rf %s" % temp_dir)
    perform("mkdir -p /tmp/%s" % temp_dir)
    perform("cp -r * /tmp/%s" % temp_dir, path=docker_src_base_dir)
    perform('find . -type d -name ".svn"|xargs rm -rf', path = "/tmp/%s" % temp_dir)
    perform('find . -type d -name ".git"|xargs rm -rf', path = "/tmp/%s" % temp_dir)
    perform("tar czvf %s %s" % (src_package, temp_dir), path = "/tmp")
    perform("mv -f %s %s" % (src_package, rpm_source), path = "/tmp")
    perform("rm -rf /tmp/%s" % temp_dir)
    
    docker_spec = os.path.join(current_dir, "rpmbuild", "SPECS", "docker-io.spec") 
    perform('sed -i  "/^Version/c Version:    %s" %s' % (version, docker_spec))
            
if __name__ == '__main__':
    pack_docker()