# Summary
Some scripts to populate Netbox. This is a separate project from the other 84829294 projects I have that do the same thing.

# Prerequisites

```
% .venv/bin/pip freeze
certifi==2024.2.2
charset-normalizer==3.3.2
idna==3.7
packaging==23.2
pynetbox==7.3.3
PyYAML==6.0.1
requests==2.32.3
urllib3==2.2.1
```

You need to generate a file called `creds.yml` and put it in the root of the repo. This will contain the Netbox host 
info and the token used to access it. The contents should look like this.

```
host: <MY_NB_HOSTNAME>
token: <MY_API_TOKEN>
```

You also need to update the `baseline.yml` file with your data. There is some sample date in there to follow. Since one
piece of information depends on others in Netbox, you'll need to make sure you have the low-level stuff created. 
```
manufacturers:
device_roles:
device_types:
sites:
```
See the grander Netbox docs to understand how that works.

Under `sites:`, we have `name`, `description`, and `physical_address`. I think you can figure that part out.

Also under `sites:`, we have `racks:` and `devices:`.

```
...
    racks:
      - name: <RACKNAME>
      - name: <ANOTHER_RACKNAME>
        u_height: <RU_HEIGHT>  *optional*
...
    devices:
      - name: <DEVICENAME>
        role: <DEVICE_ROLE> *see roles section*
        device_type: <DEVICE_TYPE> *see device types section*
        rack:                      -|
          name: <RACKNAME>          |- *optional section*
          position: <RU_POSITION>  -|
```
There's some checking going on, so the whole thing won't crash if you mess up the YAML. Don't take that as a challenge,
please. :)

# Usage

## Loading the baseline
`% .venv/bin/python populate_baseline.py`

This will load in all baseline info from `baseline.yml` and shove it into Netbox using the creds given.