# AzMonitorUptime
A Python 3 tool to parse Azure Monitor logs to retrieve VM uptime for all VMs during a given month

## Requirements
- Python 3
- Download Azure monitor logs, and store them as **QueryResult.csv** in the same folder as azmon-uptime.py

## Querying Azure Monitor

** Navigate to Azure Monitor**
![Navigate to Azure Monitor](https://raw.githubusercontent.com/marlinspike/AzMonitorUptime/master/img/0-AzureMonitor.png)

** Construct the query as such, and Download **
![Create and Download Azure Monitor Query Data](https://raw.githubusercontent.com/marlinspike/AzMonitorUptime/master/img/1-AzMonitorQuery.png)

** Finally, place downloaded file (QueryResult.csv), in the same folder as azmon-uptime.py

## Usage
python azmon-uptime.py


## Sample Output
```
-------- VM Runtime --------
u-vm - 0:11:29
win10-vs - 26 days, 1:19:12
----------------------------
```