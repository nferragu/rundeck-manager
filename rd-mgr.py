#!/usr/bin/python
# coding: utf-8

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import xml.etree.ElementTree as ET
import time
import json
import sys
import pprint
import getpass
import argparse
import platform
import os
import glob
import textwrap


# Returns the Load Average
def get_system():
    global PROPERTIES
    global HEADERS

    system_info = []
    try:
        url = URL + 'system/info'
        r = requests.get(url, headers=HEADERS, verify=False, timeout=PROPERTIES['TIMEOUT'])
        root=json.loads(r.content)
        print "LoadAverage ",root['system']['stats']['cpu']['loadAverage']['average']

    except:
        print "Problem with system info {0}".format(r)
        pass
    return system_info

# Returns list of all the project names
def get_projects():
    global PROPERTIES
    global HEADERS

    project_names = []
    try:
        url = URL + 'projects'
        r = requests.get(url, headers=HEADERS, verify=False,timeout=PROPERTIES['TIMEOUT'])
        root = json.loads(r.content)
        for p in root:
            project_names.append (p['name'])
    except:
        print "Problem with project listing {0}".format(r)
        pass
    return project_names


# Returns project config
def get_project_config(project_name):
    global PROPERTIES
    global HEADERS
    job_ids = []
    try:
        url = URL + 'project/' + project_name + '/config'
        if PROPERTIES['VERBOSE']:
            print (url)
        r = requests.get(url, headers=HEADERS, verify=False,timeout=PROPERTIES['TIMEOUT'])
        root = json.loads(r.content)
    except:
        print "Problem with get_project_config/loads {0}".format(r.content)
        pass
    try:
        if "resources.source.1.config.format" in root:
		del root["resources.source.1.config.format"]
        root['config-type']='project'
        if PROPERTIES['VERBOSE']:
            print (r.content)
    except:
        print "Problem with get_project_config/del {0}".format(r.content)
        pass
    return root

# Returns project scm export config
def get_project_scm_export_config(project_name,branch,scmkeystore):
    global PROPERTIES
    global HEADERS
    job_ids = []
    try:
        url = URL + 'project/' + project_name + '/scm/export/config'
        if PROPERTIES['VERBOSE']:
            print ('Call '+url)
        headers = {'Accept': 'application/json', 'X-RunDeck-Auth-Token': PROPERTIES['API_KEY']}
        r = requests.get(url, headers=headers, verify=False,timeout=PROPERTIES['TIMEOUT'])
        root = json.loads(r.content)
        if ('error' in root):
            return False
        #anchors pour import fichier
        root['config-type'] = 'scm-export'
        root['project.name'] = root['project']

        #pour modifier la branche par defaut
        #root['config']['branch'] = root['project.name']
        if branch:
            root['config']['branch'] = branch

        #application politique github
	if scmkeystore != "":
            root['config']['sshPrivateKeyPath'] = scmkeystore

        if PROPERTIES['VERBOSE']:
            print ('Response '+r.content)
    except:
        print "Problem with get_project_scm_export_config {0}".format(r.content)
        pass
    if ('error' in root):
        return False
    else:
        return root

# Returns project scm import config
def get_project_scm_import_config(project_name, branch, scmkeystore):
    global PROPERTIES
    global HEADERS
    job_ids = []
    try:
        url = URL + 'project/' + project_name + '/scm/import/config'
        if PROPERTIES['VERBOSE']:
            print ('Call '+url)
        headers = {'Accept': 'application/json', 'X-RunDeck-Auth-Token': PROPERTIES['API_KEY']}
        r = requests.get(url, headers=headers, verify=False,timeout=PROPERTIES['TIMEOUT'])
        root = json.loads(r.content)
        if ('error' in root):
            return False
        # anchors pour import fichier
        root['config-type'] = 'scm-import'
        root['project.name'] = root['project']

        # pour modifier la branche par defaut
        #root['config']['branch'] = root['project.name']
        if branch:
            root['config']['branch'] = branch

        #application politique github
        if scmkeystore != "":
            root['config']['sshPrivateKeyPath'] = scmkeystore

        if PROPERTIES['VERBOSE']:
            print ('Response '+r.content)
    except:
        print "Problem with get_project_scm_import_config {0}".format(r.content)
        pass
    if ('error' in root):
        return False
    else:
        return root

#Project creation
def create_project(config):
    global PROPERTIES
    global HEADERS
    url = URL + 'projects'
    try:
        r = requests.post(url, headers=HEADERS, data=json.dumps(config) , verify=False, timeout=PROPERTIES['DELETE_TIMEOUT'])
        if PROPERTIES['VERBOSE']:
            print (r.content)
        return True
    except:
        print "Problem with execution creation project {0}".format(r)
        return False


#Project scm export creation
def create_project_scm_export(config):
    # type: (object) -> object
    global PROPERTIES
    global HEADERS

    url = URL + 'project/' + config['project.name'] + '/scm/export/plugin/git-export/setup'
    if PROPERTIES['VERBOSE']==2:
        print (json.dumps({'config': config['config']}))
    try:
        r = requests.post(url, headers=HEADERS, data=json.dumps({'config': config['config']}), verify=False, timeout=PROPERTIES['DELETE_TIMEOUT'])
        root=json.loads(r.content)
        if PROPERTIES['VERBOSE']:
            pprint.pprint (root)
            print ('Success status :'+root['success'])
    except:
        print "Problem with create_project_scm_export {0}".format(r)
        pprint.pprint(r.content)
        root = json.loads(r.content)
        if PROPERTIES['VERBOSE']:
            pprint.pprint(root)
            print ('Success status :' + str(root['success']))

    if (root['success']):
        return True
    else:
        print ('Error : '+root['message'])
        return False

#Project scm import creation
def create_project_scm_import(config):
    # type: (object) -> object
    global PROPERTIES
    global HEADERS

    url = URL + 'project/' + config['project.name'] + '/scm/import/plugin/git-import/setup'
    if PROPERTIES['VERBOSE']==2:
        print (json.dumps({'config': config['config']}))
    try:
        r = requests.post(url, headers=HEADERS, data=json.dumps({'config': config['config']}), verify=False, timeout=PROPERTIES['DELETE_TIMEOUT'])
        root=json.loads(r.content)
        if PROPERTIES['VERBOSE']:
            pprint.pprint (root)
    except:
        print "Problem with create_project_scm_import {0}".format(r)
        pprint.pprint(r.content)
        root = json.loads(r.content)
        if PROPERTIES['VERBOSE']:
            pprint.pprint(root)
            print ('Success status :' + str(root['success']))

    if (root['success']):
        return True
    else:
        print ('Error : '+root['message'])
        return False

#Project delete
def delete_project(project):
    global PROPERTIES
    global HEADERS

    url = URL + 'project/'+project
    try:
        r = requests.delete(url, headers=HEADERS, verify=False, timeout=PROPERTIES['DELETE_TIMEOUT'])
        if PROPERTIES['VERBOSE']:
            print ("Reponse request.delete : "+r.content)
    except:
        print "Problem with execution deletion project {0}".format(r)
    if (r.status_code==204):
        return True
    else:
        return False

#
# Main
#

if __name__ == "__main__":
        parser = argparse.ArgumentParser(description="Tools to export/import projects and SCM associated configurations",
                                         formatter_class=argparse.RawDescriptionHelpFormatter,
                                         epilog=textwrap.dedent('''Exemples :
            ./rd-mgr.py --config newprop.json --register t/*.json
            ./rd-mgr.py --config newprop.json --delete --confirm
            ./rd-mgr.py --save all --dir t'''))
        parser.add_argument('--config', dest="config", help="Configuration file. Options overrides it.")
        parser.add_argument('--username', dest="username", help="Account Username for Rundeck Login")
        parser.add_argument('--password', dest="password", help="Account Password for Rundeck Login")
        parser.add_argument('--server', dest="server", help="Rundeck server address")
        parser.add_argument('--port', dest="port", help="Rundeck server port")
        parser.add_argument('--ssl', dest="ssl", action='count', help="set it if Rundeck server is in https")
        parser.add_argument('--key', dest="key", help="API token key")
        parser.add_argument('--api', dest="api", help="API version to deal with")
        parser.add_argument('--register', dest="register", nargs="*", help="Register config file")
        parser.add_argument('--save', dest="save", nargs="*", help="Get config projects A B C.. Keyword all for all.")
        parser.add_argument('--branch', dest="branch", help="Override branch on save")
        parser.add_argument('--scmkeystore', dest="scmkeystore", default="", help="Path to ssh priv key for SCM on save")
        parser.add_argument('--dir', dest="directory", help="Destination directory for saved files")
        parser.add_argument('--list', dest="list", action='count', help="List projects")
        parser.add_argument('--delete', dest="delete", nargs="*", help="Delete projects A B C.. Keyword all for all.")
        parser.add_argument('--confirm', dest="confirm", action='count', help="Yes I really do want to del it.")
        parser.add_argument('-v', dest="verbose", action='count', help="verbose mode")


        options = parser.parse_args()

        # si fichier de config specifie
        if options.config:
            setting_filename = options.config
        else:
            setting_filename = 'properties.json'

        # valorisation PROPERTIES
        try:
            with open(setting_filename, 'r') as props_file:
                PROPERTIES = json.load(props_file)
        except:
            print ("Error : no configuration file found")
            exit(1)

        # Override with options
        if ((options.username) and (options.password)):
            # todo : get APIkey
            print "API Key creation not implemented yet. Sorry. Ignoring user/password"
        if options.server:
            PROPERTIES['RUNDECKSERVER']=options.server
        if options.port:
            PROPERTIES['PORT']=options.port
        if options.ssl>0:
            PROPERTIES['SSL']=True
        if options.key:
            PROPERTIES['API_KEY']=options.key
        if options.api:
            PROPERTIES['API_VERSION']=options.api
        if options.verbose:
            PROPERTIES['VERBOSE']=True

        if PROPERTIES['VERBOSE']:
            print "Mode verbeux"
            pprint.pprint (PROPERTIES)

        protocol='http'
        if PROPERTIES['SSL']:
            protocol='https'
            # disable warnings about unverified https connections
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        URL = '{0}://{1}:{2}/api/{3}/'.format(protocol,PROPERTIES['RUNDECKSERVER'],PROPERTIES['PORT'],PROPERTIES['API_VERSION'])
        HEADERS = {'Content-Type': 'application/json', 'Accept': 'application/json', 'X-RunDeck-Auth-Token': PROPERTIES['API_KEY'] }

        TODAY = int(round(time.time() * 1000))

        if PROPERTIES['VERBOSE']:
            get_system()

       # pprint.pprint (options)

        if (options.list>0):
            if PROPERTIES['VERBOSE']:
                print ('Listing from '+PROPERTIES['RUNDECKSERVER'])
            for project in get_projects():
                print(project)

        if (options.save!=None):
            if PROPERTIES['VERBOSE']:
                print ('Saving from '+PROPERTIES['RUNDECKSERVER'])

            if (options.save[0]=='all'):
                options.save=get_projects()
            for project in options.save:
                print("Saving "+project)
		if os.path.isdir(options.directory):
                    with open(options.directory+'/'+project+'.project.json','w') as outfile:
                        json.dump(get_project_config(project), outfile)
                    outfile.close()
                    with open(options.directory+'/'+project+'.scm.export.json','w') as outfile:
                        json.dump(get_project_scm_export_config(project,options.branch,options.scmkeystore), outfile)
                    outfile.close()
                    with open(options.directory+'/'+project+'.scm.import.json','w') as outfile:
                        json.dump(get_project_scm_import_config(project,options.branch,options.scmkeystore), outfile)
                    outfile.close()
                else:
                    print (" No dir "+options.directory+". Aborted")
                    exit (1)
            exit(0)

        if (options.register!=None):
            if PROPERTIES['VERBOSE']:
                print ('Registering to '+PROPERTIES['RUNDECKSERVER'])
            for i in options.register:
                print ('Register '+ i),
                with open(i) as infile:
                    data=json.load(infile)
                    if PROPERTIES['VERBOSE']:
                        pprint.pprint (data)
                    if (data == False):
                        print ('Nothing to deal with')
                        continue
                    project_name=data['project.name']
                    config_type=data['config-type']
                    del data['config-type']
                    if (config_type=='project'):
                        config = {'name' : project_name,'config' : data }
                        if PROPERTIES['VERBOSE']:
                            print ('Project ')
                            pprint.pprint(config)
                        if(create_project(config)):
                            print ('Done')
                        else:
                            print ('Error')
                    elif (config_type == 'scm-export'):
                        config=data
                        if PROPERTIES['VERBOSE']:
                            print ('scm-export ')
                            pprint.pprint(config)
                        if (create_project_scm_export(config)):
                            print ('Done')
                        else:
                            print ('Error')
                    elif (config_type == 'scm-import'):
                        config=data
                        if PROPERTIES['VERBOSE']:
                            print ('scm-import ')
                            pprint.pprint(config)
                        if (create_project_scm_import(config)):
                            print ('Done')
                        else:
                            print ('Error')
                infile.close()

            exit(0)

        if (options.delete!=None):
            if PROPERTIES['VERBOSE']:
                print ('Deleting from '+PROPERTIES['RUNDECKSERVER'])
            if (options.confirm==None):
                print ('Please ensure what you are doing with --confirm option.')
                print ('Deletion aborted.')
                exit(1)
            if (options.delete[0]=='all'):
                options.delete=get_projects()
            for i in options.delete:
                print ('Delete '+i),
                if delete_project(i):
                    print ("Done")
                else:
                    print ('Erreur. Quit.')
                    exit(1)



