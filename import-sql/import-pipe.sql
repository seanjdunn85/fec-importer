LOAD DATA INFILE 'itcont'
INTO TABLE `indiv`
FIELDS TERMINATED BY '|'
LINES TERMINATED BY '\n'

(
`CMTE_ID`,
`AMNDT_IND`,
`RPT_TP`,
`TRANSACTION_PGI`,
`IMAGE_NUM`,
`TRANSACTION_TP`,
`ENTITY_TP`	,
`NAME`,
`CITY`,
`STATE`,
`ZIP_CODE`,
`EMPLOYER`,
`OCCUPATION`,
`TRANSACTION_DT`,
`TRANSACTION_AMT`,
`OTHER_ID`	,
`TRAN_ID`	,
`FILE_NUM`	,
`MEMO_CD`	,
`MEMO_TEXT`	,
`SUB_ID`
);