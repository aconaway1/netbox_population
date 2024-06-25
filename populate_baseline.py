import yaml
import pynetbox

CREDS_FILE = "creds.yml"
BASELINE_FILE = "baseline.yml"

def load_creds(creds_file):

    with open(creds_file) as file:
        return yaml.safe_load(file)

def load_baseline(baseline_file):

    with open(baseline_file) as file:
        return yaml.safe_load(file)


if __name__ == "__main__":
    creds = load_creds(CREDS_FILE)
    baseline_data = load_baseline(BASELINE_FILE)

    nb_url = f"https://{creds['host']}"
    nb_conn = pynetbox.api(url=nb_url, token=creds['token'])

    # Load the manufacturers
    for manufacturer in baseline_data['manufacturers']:
        if not manufacturer.get('name'):
            print(f"This is wrong: {manufacturer}")
            continue

        man_name = manufacturer['name'].upper()
        man_slug = manufacturer['name'].lower().replace(" ", "")

        queried_man = nb_conn.dcim.manufacturers.get(name=man_name)
        if queried_man:
            print(f"The manufacturer {man_name} already exists. Skipping.")
            continue

        constructed_man = {"name": man_name, "slug": man_slug}
        added_man = nb_conn.dcim.manufacturers.create(constructed_man)

        print(f"{added_man=}")

        # Load the device roles
    for dev_role in baseline_data['device_roles']:
        if not dev_role.get('name'):
            print(f"This is wrong: {dev_role}")
            continue

        dev_role_name = dev_role['name'].upper()
        dev_role_slug = dev_role['name'].lower().replace(" ", "")

        queried_dev_role = nb_conn.dcim.device_roles.get(name=dev_role_name)
        if queried_dev_role:
            print(f"The device role {dev_role} already exists. Skipping.")
            continue

        constructed_dev_role = {"name": dev_role_name, "slug": dev_role_slug}
        added_dev_role = nb_conn.dcim.device_roles.create(constructed_dev_role)

        print(f"{added_dev_role=}")


    for dev_type in baseline_data['device_types']:
        if not dev_type.get('model'):
            print(f"This is wrong: {dev_type}")
            continue

        if not dev_type.get('manufacturer'):
            print(f"Missing a manufacturer: {dev_type}")
            continue

        print(f"Working on {dev_type}")

        dev_type_model = dev_type['model'].upper()
        dev_type_slug = dev_type['model'].lower().replace(" ", "")

        # Get the manufacturer
        queried_man = nb_conn.dcim.manufacturers.get(name=dev_type['manufacturer'].upper())
        if not queried_man:
            print(f"This device type is wrong:\n{dev_type}")
            continue

        queried_dev_type = nb_conn.dcim.device_types.get(model=dev_type_model)
        print(f"{queried_dev_type=}")
        if queried_dev_type:
            print(f"The device type {dev_type} already exists. Skipping.")
            continue

        constructed_dev_type = {"model": dev_type_model, "slug": dev_type_slug, "manufacturer": queried_man.id}
        if dev_type.get("u_height"):
            constructed_dev_type['u_height'] = dev_type['u_height']

        added_dev_type = nb_conn.dcim.device_types.create(constructed_dev_type)


    # Go through sites
    for site in baseline_data['sites']:
        if not site.get('name'):
            print(f"Missing site name: {site}")
            continue

        site_name = site['name'].upper()

        working_site = nb_conn.dcim.sites.get(name=site_name)
        if working_site:
            print(f"Site {site_name} already exists.")
        else:
            site_slug = site['name'].lower()
            constructed_site = {"name": site_name, "slug": site_slug, "status": "active"}
            if site.get('physical_address'):
                constructed_site['physical_address'] = site['physical_address']
            if site.get('description'):
                constructed_site['description'] = site['description']
            working_site = nb_conn.dcim.sites.create(constructed_site)

        if site.get('racks'):
            for rack in site['racks']:
                rack_name = rack['name'].upper()
                working_rack = nb_conn.dcim.racks.get(name=rack['name'])
                if not working_rack:
                    constructed_rack = {"name": rack_name, "site": working_site.id, "status": "active"}
                    if rack.get('u_height'):
                        constructed_rack['u_height'] = rack['u_height']
                    working_rack = nb_conn.dcim.racks.create(constructed_rack)
                    print(f"Added rack {working_rack}")