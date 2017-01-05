# rundeck-manager
Tool to manage projects from one to another Rundeck server (export and import json definitions).

# inline help
```
usage: rd-mgr.py [-h] [--config CONFIG] [--username USERNAME]
                 [--password PASSWORD] [--server SERVER] [--port PORT]
                 [--ssl SSL] [--key KEY] [--api API]
                 [--register [REGISTER [REGISTER ...]]]
                 [--save [SAVE [SAVE ...]]] [--branch BRANCH]
                 [--scmkeystore SCMKEYSTORE] [--dir DIRECTORY] [--list]
                 [--delete [DELETE [DELETE ...]]] [--confirm] [-v]

Tools to export/import projects and SCM associated configurations

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Configuration file. Options overrides it.
  --username USERNAME   Account Username for Rundeck Login
  --password PASSWORD   Account Password for Rundeck Login
  --server SERVER       Rundeck server address
  --port PORT           Rundeck server port
  --ssl SSL             Rundeck server is in https ?
  --key KEY             API token key
  --api API             API version to deal with
  --register [REGISTER [REGISTER ...]]
                        Register config file
  --save [SAVE [SAVE ...]]
                        Get config projects A B C.. Keyword all for all.
  --branch BRANCH       Override branch on save
  --scmkeystore SCMKEYSTORE
                        Path to ssh priv key for SCM on save
  --dir DIRECTORY       Destination directory for saved files
  --list                List projects
  --delete [DELETE [DELETE ...]]
                        Delete projects A B C.. Keyword all for all.
  --confirm             Yes I really do want to del it.
  -v                    verbose mode

Exemples :
            ./rd-mgr.py --config newprop.json --register t/*.json
            ./rd-mgr.py --config newprop.json --delete --confirm
            ./rd-mgr.py --save all --dir t

```
# basic usages
# extraction des projets
```
rd-mgr.py --config <hostname.json> --save all --dir <dir> --branch <hostname>
```

# lets push on another server
```
rd-mgr.py --register --config <hostname.json> --register <dir>/*.json
```

# hostname.json format
```
{
        "RUNDECKSERVER": "rundeck.fqdn.com",
        "PORT": 4443,
        "SSL": true,
        "API_KEY": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxyyy",
        "API_VERSION": "15",
        "VERBOSE": false
}
```
