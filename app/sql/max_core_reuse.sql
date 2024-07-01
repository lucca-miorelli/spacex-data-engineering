SELECT
    "cores.core",
    COUNT(DISTINCT id) AS core_usages
FROM
    launches
WHERE
    "cores.core" IS NOT NULL
GROUP BY
    "cores.core"
ORDER BY
    COUNT(DISTINCT id) DESC
LIMIT
    1