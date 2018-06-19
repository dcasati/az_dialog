#! /usr/bin/env python3

import json
import locale
import string
import subprocess

from dialog import Dialog

def pctvalue(part, whole):
    """ Return a value in percentage
    
    :param int part: the position of this task (e.g.: 3rd out of 10)
    :param int whole: total amount of tasks (e.g.: 10 tasks)
    :return: an integer with the relative value (e.g.: 3/10)
    """
    return int(100 * part/whole)

def get_resource_groups(az_dialog):
    """ Retrieves the resource groups for the current subscription
    
    :param str az_dialog: a :class:`Dialog` instance
    :return: Returns the resource groups formated as json as `rg_as_json`
    :rtype: str
    """

    az_dialog.infobox("Fetching the resource groups ...")

    try:
        az_resource_group = subprocess.Popen(["az group list -o json"], shell=True, stdout=subprocess.PIPE)
    except:
        az_dialog.infobox("Unexpected error: " + az_resource_group.errors)
        
    jsonS,_ = az_resource_group.communicate()
    rg_as_json = json.loads(jsonS)

    return rg_as_json

def action_list_rg(az_dialog):
    """List Resource Groups
    
    :param str az_dialog: a :class:`Dialog` instance
    
    """

    my_list = []

    rg_as_json = get_resource_groups(az_dialog)

    # Initialize gauge
    az_dialog.gauge_start("Progress", percent=0)

    for line in range(0, len(rg_as_json)):
        az_dialog.gauge_update(line)
        this_item = rg_as_json[line]['properties']['provisioningState'] + "\t" + rg_as_json[line]['name']
        my_list.append(this_item)

    az_dialog.gauge_stop()

    # Sort the state of the Resource Groups
    my_list.sort()

    header = "State Name\n" + "-" * 50
    my_list.insert(0, header)

    rg_as_string = '\n'.join(my_list)
    az_dialog.msgbox(rg_as_string)

def action_delete_rg(az_dialog):
    """ 
    Delete Resource Group
    This will iterate over the Resource Groups selected by the user and will delete them.

    :param str az_dialog: a :class:`Dialog` instance
    
    """

    cleanup_list = []
    resource_groups = get_resource_groups(az_dialog)

    az_dialog.gauge_start("Progress", percent=0)
    
    for rg in range(0, len(resource_groups)):
        az_dialog.gauge_update(rg)
        this_item = (resource_groups[rg]['name'], "", False)
        cleanup_list.append(this_item)

    az_dialog.gauge_stop()

    code, tags = az_dialog.checklist("What Resource Groups do you want to delete?", 
        choices=cleanup_list)

    if code == az_dialog.OK and len(tags) > 0:
        if az_dialog.yesno("Are you sure you want to delete your Resource Groups?") == az_dialog.OK:
            az_dialog.gauge_start("Deleting", percent=0)
            for tag in range(0,len(tags)):
                az_dialog.gauge_update(percent=pctvalue(tag, len(tags)), 
                    text="Deleting " + tags[tag], 
                    update_text=True)
                
                subprocess.Popen(["az group delete  -y --no-wait -g " + tags[tag]], 
                    shell=True, 
                    stdout=subprocess.PIPE)

            az_dialog.gauge_update(percent=100, text="Complete!", update_text=True)
            az_dialog.gauge_stop()

            az_dialog.infobox("Removal of the Resource Groups is now underway")
    
        if code == az_dialog.CANCEL:
            return


def main():
    locale.setlocale(locale.LC_ALL, '')

    az_dialog = Dialog(dialog="dialog", autowidgetsize=True)
    az_dialog.set_background_title("Resource Group Cleaner")

    while True:
        _, tag = az_dialog.menu("Basic Commands:",
            choices=[("(1)", "Delete Resource Groups"),
                        ("(2)", "List Resource Groups")])
        if tag == "(1)":
            action_delete_rg(az_dialog)
            continue
        if tag == "(2)":
            action_list_rg(az_dialog)
            continue
        if az_dialog.CANCEL:
            break

if __name__ == "__main__":
    main()
