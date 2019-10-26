# Record Count by day
SELECT
       CONCAT(YEAR(ts), "-", MONTH(ts), "-", DAY(ts)) AS YMD,
       COUNT(*) AS CNT
FROM wifi_clients
GROUP BY CONCAT(YEAR(ts), "-", MONTH(ts), "-", DAY(ts));

# Record Count by day/hour
SELECT
       CONCAT(YEAR(ts), "-", MONTH(ts), "-", DAY(ts)) AS YMD,
       HOUR(ts) AS H,
       COUNT(*) AS CNT
FROM wifi_clients
GROUP BY
         CONCAT(YEAR(ts), "-", MONTH(ts), "-", DAY(ts)),
         HOUR(ts)
;

# Plot#6 - Clients per hour
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