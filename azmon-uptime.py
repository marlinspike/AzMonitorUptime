'''
    File name: azmon-uptime.py
    Author/Maintainer: Reuben Cleetus
    email:reuben@cleet.us
    2019
    License: GPL 3.0
    Python Version:3.8
'''
import csv
from collections import defaultdict
import datetime
import time
from time import mktime
import click
import calendar
from prettytable import PrettyTable



SEARCH_TERM = "Microsoft.Compute/virtualMachines"
EVENT_CAT = "Administrative"
STATUS = "Succeeded"
OPERATIONS = ["Deallocate Virtual Machine", "Start Virtual Machine", "Create or Update Virtual Machine", "Restart Virtual Machine"]
START_OPERATIONS = ["Start Virtual Machine", "Create or Update Virtual Machine", "Restart Virtual Machine"]
#DEFAULT_STOP_TIME = "2019-10-31T23:59:00.000Z"
#DEFAULT_START_TIME = "2019-10-1T0:0:00.000Z"

@click.group()
def main():
    pass


@main.command()
@click.option('--default_start', default=f"{datetime.date.today().year}-{datetime.date.today().month}-01", help='Start Date: YYYY-MM-DD')
@click.option('--default_stop', default=f"{datetime.date.today().year}-{datetime.date.today().month}-{calendar.monthrange(datetime.date.today().year,datetime.date.today().month)[1]}", help='End Date: YYYY-MM-DD')
@click.option('--file', default="QueryResult.csv", help='Azure Monitor Query Results file. Defaults to [QueryResults.csv]')
def init(default_start:str, default_stop:str, file:str):
    default_start = default_start if validate_date(default_start) else f"{datetime.date.today().year}-{datetime.date.today().month}-01"
    default_stop = default_stop if validate_date(default_stop) else f"{datetime.date.today().year}-{datetime.date.today().month}-{calendar.monthrange(datetime.date.today().year,datetime.date.today().month)[1]}"

    if(validate_date(default_start)):
        default_start += "T23:59:00.000Z"
    if(validate_date(default_stop)):
        default_stop += "T23:59:00.000Z"

    with open(file, mode='r') as f:
        csv_reader = csv.DictReader(f)
        line_count = 0
        vm_count = 0

        vm = defaultdict(list)
        vm_run_list = defaultdict(list)


        for row in csv_reader:
            if (line_count == 0):
                pass #print(f"Read Columns: {', '.join(row)}")
            else:
                #Make sure we only get VMs with the right Event and Status
                if (row["Resource type"] == SEARCH_TERM and row["Event category"] == EVENT_CAT and row["Status"] == STATUS):
                    idx = row["Resource"].rindex("/") + 1
                    #Make sure we only get the Start and Stop operations
                    if (row["Operation name"] in OPERATIONS):
                        #vm[(str(row["Resource"])[idx:len(row["Resource"])])].append(row)
                        vm[get_vm_name_from_resource(row["Resource"])].append(row)
                        vm_count += 1
            line_count += 1

        print(f"Found {vm_count} VMs")
        print(f"Processed {line_count} lines")

        #for each VM
        for vm_name, vm_status_list in vm.items():
            start_time:datetime = None
            stop_time:datetime = None
            runtime:datetime = None
            status_list_count = -1        

            #for each status
            for azvm in vm_status_list:
                status_list_count += 1
                if(azvm["Operation name"] in START_OPERATIONS):
                    start_time = azvm["Time"]
                elif(azvm["Operation name"] == "Deallocate Virtual Machine"):
                    stop_time = azvm["Time"]
                
                #Make sure we have a default start and stop time
                if ((len(vm_status_list) == status_list_count+1) and stop_time == None):
                    stop_time = default_stop #DEFAULT_STOP_TIME
                if ((len(vm_status_list) == status_list_count+1) and start_time == None):
                    start_time = default_start #DEFAULT_START_TIME
                
                #See if we have both a start and end time
                if (start_time != None and stop_time != None):
                    if (runtime == None):
                        runtime = get_elapsed_time(time.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%fZ"), time.strptime(stop_time, "%Y-%m-%dT%H:%M:%S.%fZ"))
                    else:
                        runtime = runtime + get_elapsed_time(time.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%fZ"), time.strptime(stop_time, "%Y-%m-%dT%H:%M:%S.%fZ"))
                    vm_run_list[get_vm_name_from_resource(azvm["Resource"])].append(runtime)
                    start_time = None
                    stop_time = None
        
        printOutputTable(vm_run_list)


###
# Validates given date
def validate_date(date_text:str) -> bool:
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return False
    return True

###
# Returns elapsed time between start and end times
def get_elapsed_time(start:datetime, stop:datetime) -> datetime:
    diff =  datetime.datetime.fromtimestamp(mktime(stop)) - datetime.datetime.fromtimestamp(mktime(start))
    return diff

###
# Returns a VM name from resource name
def get_vm_name_from_resource(resource:str) -> str:
    idx = resource.rindex("/") + 1
    return resource[idx:len(resource)]

###
# Deprecated. Prints output based on the vm data passed
def print_vm_runtime(oDict):
    print("-------- VM Runtime --------")
    for vm, runtime in oDict.items():
        print(f"{vm} - {runtime[0]}")
    print("----------------------------")

###
# Prints output based on the vm data passed
def printOutputTable(oDict):
    row:int = 0
    table = PrettyTable(['#','VM Name', 'Runtime'])
    table.title = f"AzMon v0.90"
    table.align['#'] = "l"
    table.align['VM Name'] = "l"
    table.align['Runtime'] = "l"
    for vm, runtime in oDict.items():
        row += 1
        table.add_row([row, vm, runtime[0]])
    print(f"\n\n{table}\n")


if __name__ == '__main__':
    main()