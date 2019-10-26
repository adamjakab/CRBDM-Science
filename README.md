CRBDM
======
Data analysis for CRBDM project...

OS(os)
-------
![Plot 1](Plots/plot_1.png?raw=true "Plot 1")

SQL:
```mysql
SELECT DISTINCT(os) AS OS, COUNT(*) AS CNT FROM wifi_clients GROUP BY os ORDER BY CNT DESC
```

Utility:
- none
- needs to be removed

MQTT Batch(mqtt_batch)
----------------------
