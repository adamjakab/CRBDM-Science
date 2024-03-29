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
received 5 minute apart. The current configuration stores at the same frequency.

![Plot 4](images/hourly_average_client_count_full_period.png?raw=true "Plot 4")

SQL:
```mysql
SELECT 
    v.ts AS TS,
    v.per_minute_count AS CNT_PER_MIN
FROM v__wcb__h__record_counts AS v;
```

Utility:
- each connection payload needs to be identifiable in time so we can establish if a user is present at the institution
or not.


MQTT Batch(mqtt_batch)
----------------------
Description: The payloads come in batches 5 minute apart. Each batch will contain 1 to N connection payloads. This
number serves the purpose to be able to identify the payloads that arrived together in the same batch. The number of 
payloads per batch tells the actual number of connected devices at ITU in a certain point.

![Plot 2](images/plot_2.png?raw=true "Plot 2")
 
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

![Plot 3](images/plot_3.png?raw=true "Plot 3")

SQL:
```mysql
SELECT 
    v.ts AS TS, 
    v.mqtt_count AS BATCH_COUNT 
FROM v__wcb__h__record_counts AS v;
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

![Plot 1](images/plot_1.png?raw=true "Plot 1")

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
```mysql
# SQL for plots:
SELECT DATE_FORMAT(MIN(ts), "%Y-%m-%d %H:00:00")                             AS TS,
       ROUND(COUNT(*) / COUNT(DISTINCT mqtt_batch))                          AS CNT_PER_MIN,
       COUNT(DISTINCT mqtt_batch)                                            AS BN,
       ROUND(SUM(IF(ssid = '5te', 1, 0)) / COUNT(DISTINCT mqtt_batch))       AS CNT_5TE,
       ROUND(SUM(IF(ssid = 'eduroam', 1, 0)) / COUNT(DISTINCT mqtt_batch))   AS CNT_EDUROAM,
       ROUND(SUM(IF(ssid = 'ITU++', 1, 0)) / COUNT(DISTINCT mqtt_batch))     AS CNT_ITU_PLUS,
       ROUND(SUM(IF(ssid = 'ITU-guest', 1, 0)) / COUNT(DISTINCT mqtt_batch)) AS CNT_ITU_GUEST,
       ROUND(SUM(IF(ssid = 'sensors', 1, 0)) / COUNT(DISTINCT mqtt_batch))   AS CNT_SENSORS
FROM wifi_clients
WHERE ts >= "2019-10-23 22:00:00"
GROUP BY YEAR(ts), MONTH(ts), DAY(ts), HOUR(ts)
; 
```

![Plot 5](images/plot_5.png?raw=true "Plot 5")

![Plot 6](images/plot_6.png?raw=true "Plot 6")

Utility:
- Students who use the wi-fi regularly at ITU use either "eduroam" or "ITU++". These networks will also have non-students. 
- Eduroam: We might have external students OR students who are still using previous education assigned credentials.
- We can quite surely exclude "5TE" and "sensors"


Session Start(session_start)
-------
Description: The timestamp when the session started for this client.

Utility:
- Could be used to determine how long a client stays at ITU hence putting together not only if he is present but also 
for how long


User Profile(user_profile)
-------
Description: The type of profile the client has. These types are defined by the infrastructure.
```text
SQL: SELECT DISTINCT(user_profile) FROM wifi_clients'

      user_profile
0    Authenticated
1            Guest
2           Sensor
3  default-profile
4            5te-1
5            5te-3
6            5te-5
7            5te-7
```

![Plot 7](images/plot_7.png?raw=true "Plot 7")

```mysql
# SQL for plots:
SELECT DATE_FORMAT(MIN(ts), "%Y-%m-%d %H:00:00")                                           AS TS,
       ROUND(COUNT(*) / COUNT(DISTINCT mqtt_batch))                                        AS CNT_PER_MIN,
       COUNT(DISTINCT mqtt_batch)                                                          AS BN,
       ROUND(SUM(IF(user_profile = "Authenticated", 1, 0)) / COUNT(DISTINCT mqtt_batch))   AS UP_AUTH,
       ROUND(SUM(IF(user_profile = "Guest", 1, 0)) / COUNT(DISTINCT mqtt_batch))           AS UP_GUEST,
       ROUND(SUM(IF(user_profile = "Sensor", 1, 0)) / COUNT(DISTINCT mqtt_batch))          AS UP_SENSOR,
       ROUND(SUM(IF(user_profile = "default-profile", 1, 0)) / COUNT(DISTINCT mqtt_batch)) AS UP_DEFPROF,
       ROUND(SUM(IF(user_profile = "5te-1", 1, 0)) / COUNT(DISTINCT mqtt_batch))           AS UP_5TE_1,
       ROUND(SUM(IF(user_profile = "5te-3", 1, 0)) / COUNT(DISTINCT mqtt_batch))           AS UP_5TE_3,
       ROUND(SUM(IF(user_profile = "5te-5", 1, 0)) / COUNT(DISTINCT mqtt_batch))           AS UP_5TE_5,
       ROUND(SUM(IF(user_profile = "5te-7", 1, 0)) / COUNT(DISTINCT mqtt_batch))           AS UP_5TE_7
FROM wifi_clients
WHERE ts >= "2019-10-24 22:00:00"
GROUP BY YEAR(ts), MONTH(ts), DAY(ts), HOUR(ts)
; 
```

```text
# DATA EXTRACT:
| TS | CNT\_PER\_MIN | BN | UP\_AUTH | UP\_GUEST | UP\_SENSOR | UP\_DEFPROF | UP\_5TE\_1 | UP\_5TE\_3 | UP\_5TE\_5 | UP\_5TE\_7 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2019-10-25 07:00:00 | 102 | 60 | 85 | 2 | 11 | 0 | 3 | 2 | 0 | 0 |
| 2019-10-25 08:00:00 | 606 | 60 | 568 | 14 | 12 | 0 | 7 | 5 | 0 | 0 |
| 2019-10-25 09:00:00 | 1049 | 59 | 990 | 32 | 11 | 1 | 6 | 9 | 0 | 0 |
| 2019-10-25 10:00:00 | 1311 | 59 | 1242 | 40 | 12 | 0 | 8 | 9 | 0 | 0 |
| 2019-10-25 11:00:00 | 1277 | 59 | 1205 | 45 | 12 | 0 | 6 | 9 | 0 | 0 |
| 2019-10-25 12:00:00 | 1164 | 60 | 1099 | 38 | 11 | 1 | 7 | 9 | 0 | 0 |
| 2019-10-25 13:00:00 | 1100 | 59 | 1043 | 30 | 12 | 0 | 7 | 8 | 0 | 0 |
```

Utility:
- We are most probably need to look at "Authenticated" profiles. Sensors are not useful for us. and the other ones are almost zero.
- The "guest" network might have some first time users... 





