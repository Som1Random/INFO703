CREATE TABLE nick95.ds_gs_all
AS (SELECT * FROM PAGER3.ds_gs_all)
;

CREATE TABLE nick95.ds_gs_all_gene
AS (SELECT * FROM PAGER3.ds_gs_all_gene)
;

CREATE TABLE nick95.ds_gs_all_type
AS (SELECT * FROM PAGER3.ds_gs_all_type)
;

CREATE TABLE nick95.ds_gs_all_source
AS (SELECT * FROM PAGER3.ds_gs_all_source)
;

CREATE TABLE nick95.gene_human
AS (SELECT * FROM PAGER3.gene_human)
;

-- Updating ds_gs_all original_id column to more bytes (for inserting SIGNOR data)

ALTER TABLE nick95.ds_gs_all
ADD original_id1 VARCHAR(100)
;

UPDATE nick95.ds_gs_all
SET original_id1 = original_id
;

update nick95.ds_gs_all
SET original_id = NULL
;

ALTER TABLE nick95.ds_gs_all
MODIFY original_id VARCHAR(100)
;

UPDATE nick95.ds_gs_all
SET original_id = original_id1
;

ALTER TABLE nick95.ds_gs_all
DROP COLUMN original_id1
;