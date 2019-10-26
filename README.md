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

![Plot 4](Plots/plot_4.png?raw=true "Plot 4")

SQL:
```mysql
SELECT
       DATE_FORMAT(MIN(ts), "%Y-%m-%d %H:00:00") AS TS,
       ROUND(COUNT(*) / COUNT(DISTINCT mqtt_batch)) AS CNT_PER_MIN
FROM wifi_clients
WHERE ts >= "2019-10-10 00:00:00"
GROUP BY YEAR(ts), MONTH(ts), DAY(ts), HOUR(ts)
;
```

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

![Plot 3](Plots/plot_3.png?raw=true "Plot 3")

SQL:
```mysql
SELECT
       DATE_FORMAT(MIN(ts), "%Y-%m-%d %H:00:00") AS TS,
       COUNT(DISTINCT mqtt_batch) AS BATCH_COUNT
FROM wifi_clients
WHERE ts >= "2019-10-10 00:00:00"
GROUP BY YEAR(ts), MONTH(ts), DAY(ts), HOUR(ts)
;
```

Client ID(client_id)
--------------------
Description: A ?unique? ID attributed to the client terminal. 
```text
SQL: SELECT DISTINCT(client_id) FROM wifi_clients'

       client_id
0     8589943108
1     8589942875
2     8589942903
3     8589947885
4     8589943750
...          ...
8483  8589958022
8484  8589958218
8485  8589957743
8486  8589958225
8487  8589958239
```

Utility:
- To have an idea of how many unique devices circulate at ITU 
- Could be used to exclude devices that are present at all times or during non-normal hours.


Client MAC(client_mac)
---------------------
Description: Hashed mac address of the client terminal. 
```text
SQL: SELECT DISTINCT(client_mac) FROM wifi_clients'

                            client_mac
0     SGdKaEplYi94MUdobUc4VjdiM3B3QT09
1     RFcwYnBXYTBoWVduOVRsUjJRNk52UT09
2     THR6T3V0a0JvcG0wRkd1RXBEY0h1dz09
3     bGhaeU5wNFVxNTZiUWthMXJuMGNFZz09
4     U3JOM0VUam1uYkc1OCtnazExWjZFUT09
...                                ...
5847  VlJaMHd6Vm10V3pUeXU1ZklNQjU0UT09
5848  d05zaTdveXh0WlY3T0hIdW9mNGdVZz09
5849  V0NnUWNmZ09kTTVuWkZneTJqQ2RZUT09
5850  VzFUUEYrbkxtRjVDMVhmOUNndWF0dz09
5851  Y01UdEVzTkRnUmtiei83NDhnYXpMQT09

[5852 rows x 1 columns]

```

Utility:
- To have an idea of how many unique devices circulate at ITU (probably more accurate than client_id)
- Could be used to see if client_id can change over time


Device ID(device_id)
---------------------
Description: Unique ID of the access point to which the client is connected. 
```text
SQL: SELECT DISTINCT(device_id) FROM wifi_clients'

      device_id
0    8589943112
1    8589943617
2    8589943623
3    8589943629
4    8589944537
..          ...
275  8589939705
276  8589939726
277  8589939617
278  8589939734
279  8589939688

[280 rows x 1 columns]

```

Utility:
- The devices are located in physical locations. Could be used to determine more precise location of the device.
- Could be used to track movements and patterns




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

