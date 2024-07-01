WITH
    unique_core_usages AS (
        SELECT DISTINCT
            flight_number,
            "cores.core",
            date_utc
        FROM
            launches
    ),
    cores_date_diff AS (
        SELECT
            flight_number,
            "cores.core",
            date_utc,
            date_utc - LAG (date_utc) OVER (
                PARTITION BY
                    "cores.core"
                ORDER BY
                    date_utc
            ) AS date_diff
        FROM
            unique_core_usages
        WHERE
            "cores.core" IS NOT NULL
        ORDER BY
            "cores.core",
            date_utc DESC
    )
SELECT
    *
FROM
    cores_date_diff
WHERE
    date_diff < INTERVAL '50 days'