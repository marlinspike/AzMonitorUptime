# AzMonitorUptime
A Python 3 tool to parse **Azure Monitor Activity Logs** to retrieve VM uptime for all VMs during a given month. This is useful for when you either don't have your VMs reporting to a Log Analytics workspace, or they only reported data for a part of the time you want to report on. Another option would be to look at billing data, but that's often previledged information. AzMonitorUptime allows you to derive uptime reports from Actvitity Logs.

## Requirements
- Python 3
- Click 7.0
- PrettyTable 0.7.2
- Download Azure monitor logs, and store them as **QueryResult.csv** in the same folder as azmon-uptime.py

## Install Python packages
pip install -r requirements.txt

## Querying Azure Monitor

**Navigate to Azure Monitor**
![Navigate to Azure Monitor](https://raw.githubusercontent.com/marlinspike/AzMonitorUptime/master/img/0-AzureMonitor.png)

**Select Activity Log**

**Construct the query as such, and Download**
![Create and Download Azure Monitor Query Data](https://raw.githubusercontent.com/marlinspike/AzMonitorUptime/master/img/1-AzMonitorQuery.png)

**Finally, place downloaded file (QueryResult.csv), in the same folder as azmon-uptime.py**

## Usage
**Default Usage**: python azmon-uptime.py init

**Optional Args**: CSVFile, Default Start Time, Default Stop Time - These are the defaults for Start and Stop times for VMs, in case they were Started/Stopped outside the period of monitoring covered in the CSV file. Unless you provide a Start time, the app has no knowledge that the VM was up, so it would otherwise just assume it was turned off!

**Optional Usage**: python azmon-uptime.py init --default_start 2019-10-01 --default_stop 2019-10-31 --file QueryResults.csv

## Sample Output
```
+----+--------------------------+------------------+
| #  | VM Name                  | Runtime          |
+----+--------------------------+------------------+
| 1  | aks-nodepool1-33200514-0 | 19 days, 0:47:23 |
| 2  | aks-nodepool1-33200514-1 | 19 days, 0:47:10 |
| 3  | aks-agentpool-87903270-0 | 19 days, 7:31:36 |
| 4  | aks-agentpool-17932189-0 | 22 days, 3:28:26 |
| 5  | aks-nodepool1-54814196-2 | 24 days, 6:43:43 |
| 6  | aks-nodepool1-54814196-0 | 24 days, 9:39:31 |
| 7  | aks-nodepool1-54814196-1 | 24 days, 9:39:46 |
| 8  | aks-nodepool1-12508969-1 | 24 days, 9:46:58 |
| 9  | u-vm2                    | 25 days, 7:45:34 |
| 10 | u-vm                     | 0:03:25          |
| 11 | win10-vs                 | 35 days, 7:40:27 |
| 12 | win10-vm1                | 26 days, 1:23:09 |
+----+--------------------------+------------------+
```