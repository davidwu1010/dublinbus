SELECT *
INTO OUTFILE '/tmp/Jan_Sections.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
ESCAPED BY '\\'
LINES TERMINATED BY '\n'
FROM dublinbus.Jan_Sections;