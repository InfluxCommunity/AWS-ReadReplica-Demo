## AWS TimeStream for InfluxDB (2.x) with Read Replica

This repository has a python program that acts as a demo for showcasing Read Replica feature of InfluxDB within AWS TimeSteam.

![Python Program Flow](https://github.com/InfluxCommunity/AWS-ReadReplica-Demo/blob/main/Program-visualization.png)

### Steps to run: [Video tutorial](https://youtu.be/jLZK5KiL3ZA)

1. Have an AWS Account and setup TimeSeries for INfluxDB - Cluster with read replica. Make sure it has an IP address
2. Login to InfluxDB via UI for both primary and replica instance and get the URL for the same. Create an API Token and Bucket and note the URL and Org name.
3. Download & Install InfluxDB v3 Python client SDK `pip install influxdb3-python`
4. Download/Clone this repo and edit the confoguration
   ```python
   # Configuration AWS TimeStream for InfluxDB
  PRIMARY_URL = ""  # Primary InfluxDB Instance
  REPLICA_URL = ""  # InfluxDB Replica Instance
  INFLUXDB_TOKEN = "" # Same API Token for both primary and replica
  ORG = "" # Same organization name for both primary and replica
  BUCKET = "" # Same bucket name for both primary and replica
```
5. Run the program `python aws-timestream-influxdb-v2-demo.py` and see the output in console logs
6. Open UI and navigate to Data Explorer for both Primary and Replica instances of InfluxDB and notice the same data being replicated.
