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
u-vm - -9 days, 7:50:27
win10-vs - 26 days, 1:19:12
win10-vm1 - 30 days, 23:59:00
u-vm2 - 30 days, 23:59:00
aks-nodepool1-12508969-1 - 30 days, 23:59:00
aks-nodepool1-54814196-1 - 30 days, 23:59:00
aks-nodepool1-54814196-0 - 30 days, 23:59:00
aks-nodepool1-54814196-2 - 30 days, 23:59:00
aks-agentpool-17932189-0 - 30 days, 23:59:00
aks-agentpool-87903270-0 - 30 days, 23:59:00
aks-nodepool1-33200514-0 - 30 days, 23:59:00
aks-nodepool1-33200514-1 - 30 days, 23:59:00
----------------------------
```