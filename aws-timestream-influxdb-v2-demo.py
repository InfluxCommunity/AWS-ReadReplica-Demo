import time
import psutil
from datetime import datetime, timezone
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import threading
import socket

# Configuration AWS TimeStream for InfluxDB
PRIMARY_URL = ""  # Primary InfluxDB Instance
REPLICA_URL = ""  # InfluxDB Replica Instance
INFLUXDB_TOKEN = "" # Same API Token for both primary and replica
ORG = "" # Same organization name for both primary and replica
BUCKET = "" # Same bucket name for both primary and replica

def collect_system_metrics():
    """Collect real system metrics using psutil"""
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "network_sent_bytes": psutil.net_io_counters().bytes_sent,
        "network_recv_bytes": psutil.net_io_counters().bytes_recv
    }

def write_to_primary(metrics):
    """Write system metrics to the primary InfluxDB instance"""
    try:
        with InfluxDBClient(url=PRIMARY_URL, token=INFLUXDB_TOKEN, org=ORG) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            
            point = Point("system_metrics") \
                .tag("host", "local-mbp") \
                .field("cpu_percent", metrics["cpu_percent"]) \
                .field("memory_percent", metrics["memory_percent"]) \
                .field("disk_percent", metrics["disk_percent"]) \
                .field("network_sent_bytes", metrics["network_sent_bytes"]) \
                .field("network_recv_bytes", metrics["network_recv_bytes"]) \
                .time(datetime.now(timezone.utc))
            
            write_api.write(bucket=BUCKET, record=point)
            print(f"Successfully wrote metrics to primary: CPU: {metrics['cpu_percent']}%, RAM: {metrics['memory_percent']}%")
            return True
    except Exception as e:
        print(f"Error writing to primary: {e}")
        return False

def read_from_primary():
    """Read metrics from primary InfluxDB instance"""
    try:
        with InfluxDBClient(url=PRIMARY_URL, token=INFLUXDB_TOKEN, org=ORG) as client:
            query = f'''
            from(bucket: "{BUCKET}")
              |> range(start: -5m)
              |> filter(fn: (r) => r._measurement == "system_metrics")
              |> limit(n: 5)
            '''
            result = client.query_api().query(query=query, org=ORG)
            
            print("\nReading from PRIMARY:")
            for table in result:
                for record in table.records:
                    print(f"  - {record.get_time()}: {record.get_field()}: {record.get_value()}")
            
            return True
    except Exception as e:
        print(f"Error reading from primary: {e}")
        return False

def read_from_replica():
    """Read metrics from AWS replica InfluxDB instance"""
    try:
        with InfluxDBClient(url=REPLICA_URL, token=INFLUXDB_TOKEN, org=ORG) as client:
            # Allow a slight delay for replication to occur
            time.sleep(1)
            
            query = f'''
            from(bucket: "{BUCKET}")
              |> range(start: -5m)
              |> filter(fn: (r) => r._measurement == "system_metrics")
              |> limit(n: 5)
            '''
            result = client.query_api().query(query=query, org=ORG)
            
            print("\nReading from AWS REPLICA:")
            for table in result:
                for record in table.records:
                    print(f"  - {record.get_time()}: {record.get_field()}: {record.get_value()}")
            
            return True
    except Exception as e:
        print(f"Error reading from AWS replica: {e}")
        return False

def main():
    print("Starting InfluxDB AWS Primary/Replica System Metrics Demo")
    print("=======================================================")
    
    # Collect and write system metrics to primary only
    # AWS will handle replication automatically
    for i in range(5):
        metrics = collect_system_metrics()
        write_to_primary(metrics)
        time.sleep(1)  # Wait between measurements
    
    # Read metrics from both primary and replica
    read_from_primary()
    read_from_replica()
    
    print("\nDemo completed")

if __name__ == "__main__":
    main()
