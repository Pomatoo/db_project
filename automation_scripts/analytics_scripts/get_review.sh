#!/usr/bin/env bash


SELECT 'id', 'first_name', 'last_name'
UNION ALL
SELECT id, first_name, last_name
FROM customer
INTO OUTFILE '/temp/myoutput.txt'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';