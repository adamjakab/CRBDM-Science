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

