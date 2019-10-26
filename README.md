# AzMonitorUptime
A Python 3 tool to parse Azure Monitor logs to retrieve VM uptime for all VMs during a given month

## Requirements
- Python 3
- Download Azure monitor logs, and store them as **QueryResult.csv** in the same folder as azmon-uptime.py

## Querying Azure Monitor

**Navigate to Azure Monitor**
![Navigate to Azure Monitor](https://raw.githubusercontent.com/marlinspike/AzMonitorUptime/master/img/0-AzureMonitor.png)

**Construct the query as such, and Download**
![Create and Download Azure Monitor Query Data](https://raw.githubusercontent.com/marlinspike/AzMonitorUptime/master/img/1-AzMonitorQuery.png)

**Finally, place downloaded file (QueryResult.csv), in the same folder as azmon-uptime.py**

## Usage
python azmon-uptime.py


## Sample Output
```
-------- VM Runtime --------
aks-nodepool1-33200514-0 - 19 days, 0:47:23
aks-nodepool1-33200514-1 - 19 days, 0:47:10
aks-agentpool-87903270-0 - 19 days, 7:31:36
aks-agentpool-17932189-0 - 22 days, 3:28:26
aks-nodepool1-54814196-2 - 24 days, 6:43:43
aks-nodepool1-54814196-0 - 24 days, 9:39:31
aks-nodepool1-54814196-1 - 24 days, 9:39:46
aks-nodepool1-12508969-1 - 24 days, 9:46:58
u-vm2 - 25 days, 7:45:34
u-vm - 0:03:25
win10-vs - 35 days, 7:40:27
win10-vm1 - 26 days, 1:23:09
----------------------------
```