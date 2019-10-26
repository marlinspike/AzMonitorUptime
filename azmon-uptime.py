import csv
from collections import defaultdict
import datetime
import time
from time import mktime


def get_elapsed_time(start:datetime, stop:datetime) -> datetime:
    diff =  datetime.datetime.fromtimestamp(mktime(stop)) - datetime.datetime.fromtimestamp(mktime(start))
    return diff

def get_vm_name_from_resource(resource:str) -> str:
    idx = resource.rindex("/") + 1
    return resource[idx:len(resource)]

def print_vm_runtime(oDict):
    print("-------- VM Runtime --------")
    for vm, runtime in oDict.items():
        print(f"{vm} - {runtime[0]}")
    print("----------------------------")

with open('QueryResult.csv', mode='r') as f:
    csv_reader = csv.DictReader(f)
    line_count = 0
    vm_count = 0
    SEARCH_TERM = "Microsoft.Compute/virtualMachines"
    EVENT_CAT = "Administrative"
    STATUS = "Succeeded"
    OPERATIONS = ["Deallocate Virtual Machine", "Start Virtual Machine"]
    vm = defaultdict(list)
    vm_run_list = defaultdict(list)
    DEFAULT_STOP_TIME = "2019-10-31T23:59:00.839Z"
    DEFAULT_START_TIME = "2019-10-1T0:0:00.839Z"

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
            if(azvm["Operation name"] == "Start Virtual Machine"):
                start_time = azvm["Time"]
            elif(azvm["Operation name"] == "Deallocate Virtual Machine"):
                stop_time = azvm["Time"]
            
            #Make sure we have a default start and stop time
            if ((len(vm_status_list) == status_list_count+1) and stop_time == None):
                stop_time = DEFAULT_STOP_TIME
            if ((len(vm_status_list) == status_list_count+1) and start_time == None):
                start_time = DEFAULT_START_TIME
            

            #See if we have both a start and end time
            if (start_time != None and stop_time != None):
                runtime = get_elapsed_time(time.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%fZ"), time.strptime(stop_time, "%Y-%m-%dT%H:%M:%S.%fZ"))
                vm_run_list[get_vm_name_from_resource(azvm["Resource"])].append(runtime)
    
    print_vm_runtime(vm_run_list)