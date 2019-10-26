CRBDM
======
Data analysis for CRBDM project.
Below is the description of the attributes of the wifi_clients table.


ID(id)
------
Description: Incremental unique id

Timestamp(ts)
-------------
Description: The timestamp created by the database server when the payload was received. Consecutive timestamps are
received 1 minute apart. The current configuration stores at the same frequency.

Utility:
- each connection payload needs to be identifiable in time so we can establish if a user is present at the institution
or not.

MQTT Batch(mqtt_batch)
----------------------
Description: The payloads come in batches 1 minute apart. Each batch will contain 1 to N connection payloads. This
number serves the purpose to be able to identify the payloads that arrived together in the same batch. The number of 
payloads per batch tells the actual number of connected devices at ITU in a certain point.

![Plot 2](Plots/plot_2.png?raw=true "Plot 2")
 
SQL:
```mysql
SELECT
       mqtt_batch,
       MIN(ts) AS TS,
       COUNT(*) AS CNT
FROM wifi_clients
WHERE ts >= DATE_SUB(NOW(),INTERVAL 1 HOUR)
GROUP BY mqtt_batch
ORDER BY mqtt_batch
```

OS(os)
-------
Description: The Operating System installed on the connected client.

![Plot 1](Plots/plot_1.png?raw=true "Plot 1")

SQL:
```mysql
SELECT DISTINCT(os) AS OS, COUNT(*) AS CNT FROM wifi_clients GROUP BY os ORDER BY CNT DESC
```

Utility:
- none
- needs to be removed

