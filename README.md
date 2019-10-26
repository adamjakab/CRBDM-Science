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


Host Name(host_name)
---------------------
Description: Don't really know. Hashed host name of ???
```text
SQL: SELECT DISTINCT(host_name) FROM wifi_clients'

                                              host_name
0                      RGR4V0JTWXA4YjJUMzJ4VStNU3kwUT09
1                      N0QwSkRRY1VVdmNIYi9QZ3BuRHpRQT09
2                      d2tRQ1JmcmlkS2RlVHBxYURteDFKUT09
3                      eXZubzMxRGRNMDhjK2xpVFNlMFdhZz09
4                      anptR0pzWjgwdVBWd1VIVjlna3VHQT09
...                                                 ...
4518  Um1hNytJd3JXckRUV0ZRWTRvRmpnSHQzOE03b1IvdjFRY2...
4519                   bG80bitnaWxrQkpGWE1nbzZoQy9SQT09
4520                   MmQrWXR6Ly9Nb2JjV3dYQUlHWnFBdz09
4521  aUJtZjhYV21qUlE1VFdZTFM2MFcvVDQyZnV3bnhNdEVDSn...
4522                   V0xMTndYZjJWT0NsL1hHaXNldE5qZz09

[4523 rows x 1 columns]
```

Utility:
- Dubious


IP(ip)
------
Description: Don't really know. Ip address of ???
```text
SQL: SELECT DISTINCT(host_name) FROM wifi_clients'

                ip
0      10.28.2.158
1      10.28.2.198
2       10.28.2.65
3      10.28.2.115
4        10.28.2.7
...            ...
10931  10.26.36.55
10932   10.26.4.25
10933  10.29.0.225
10934  10.29.0.226
10935  10.28.40.76

[10936 rows x 1 columns]
```

Utility:
- Dubious


User Name(user_name)
---------------------
Description: Hashed username used to authenticate to get access to the wifi.
```text
SQL: SELECT DISTINCT(user_name) FROM wifi_clients'

                                              user_name
0                      a00zd3RIckJzTXdUZXRZSFExT0FTZz09
1                      a0dTZFhFSUJxZFQ3NTV1TjJlc0svUT09
2                      a0dYTHBqa3VSYmk0cmFEQ2EyRWNFUT09
3     a0gwTnF3T1drN2ZyNWY2SCtVZEswSnQ4b0lqTURUMGhMTW...
4                      a0JHMjlIYjhMelZFUjZsRVJ0bDhzUT09
...                                                 ...
4087                   ZzFKdHhOamxkQWJkTlluaTR4eHlndz09
4088                   ZzluUlN3WGQreEI0NDlGaThZMEU1dz09
4089                   ZzRheHFaZEk4NGlMR2d3OHVtbVJGQT09
4090                   ZzYyL3gwQ0g5U3NrelpxdzFFd3Uxdz09
4091                   ZzZJb3VNdmJNTytlcSsyTDVDdFJWQT09

[4092 rows x 1 columns]
```

Utility:
- Pseudonymised ITU username making a natural person identifiable
- Could be present multiple times in batches if user has multiple devices


OS(os)
-------
Description: The Operating System installed on the connected client.

![Plot 1](Plots/plot_1.png?raw=true "Plot 1")

SQL:
```mysql
SELECT DISTINCT(os) AS OS, COUNT(*) AS CNT FROM wifi_clients GROUP BY os ORDER BY CNT DESC
```

Utility:
- none? Could be used for statistical purposes
- needs to be removed


Wifi Usage(wifi_usage)
-------
Description: The number of bytes transferred during the session (in/out?).
```text
SQL: SELECT DISTINCT(wifi_usage) FROM wifi_clients'

         wifi_usage
count  3.752750e+05
mean   2.724465e+07
std    1.955823e+08
min    0.000000e+00
25%    1.755155e+05
50%    1.322009e+06
75%    8.359870e+06
max    1.109595e+10

mean: 27244650 -> 25Mb
max: ~10.33Gb
```

Utility:
- Could be used to trigger a warning on abnormal usage
- Also to detect idle (unused device) left at the university


SSID(ssid)
-------
Description: The name of the wi-fi network the client is connected to.
```text
SQL: SELECT DISTINCT(ssid) FROM wifi_clients ORDER BY ssid'

             ssid
0             5te
1         eduroam
2           ITU++
3       ITU-guest
4  ITU-guest-test
5         sensors
```

![Plot 5](Plots/plot_5.png?raw=true "Plot 5")

![Plot 6](Plots/plot_6.png?raw=true "Plot 6")

Utility:
- Students who use the wi-fi regularly at ITU use either "eduroam" or "ITU++". These networks will also have non-students. 
- Eduroam: We might have external students OR students who are still using previous education assigned credentials.
- We can quite surely exclude "5TE" and "sensors"




