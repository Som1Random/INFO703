-- Cleaning up some descriptions
set define off
;
-- this is needed for the next function to work (the & character is a special one)

SELECT count(*) FROM nick95.pag WHERE description = '&nbsp;';

UPDATE nick95.pag
SET description = NULL
WHERE description = '&nbsp;'
;


-- Fixing the pager version variable
SELECT count(*) FROM nick95.pag WHERE pager_version = 2 OR pager_version = 3;

UPDATE nick95.pag
SET pager_version = '2.0'
WHERE pager_version = '2'
;

UPDATE nick95.pag
SET pager_version = '3.0'
WHERE pager_version = '3'
;

SELECT pager_version, count(*)
FROM nick95.pag
GROUP BY pager_version
;



-- Removing pag_description if it matches the pag_name column
SELECT count(*) FROM nick95.pag WHERE description = name;

UPDATE nick95.pag
SET description = NULL
WHERE name = description
;



-- Fixing the pubmed_id column (it is inconsistent and should be a numeric column)
SELECT count(*) FROM nick95.pag
WHERE REGEXP_LIKE(pubmed_id, '^\d+$') -- 24,702 are just numeric
;

SELECT count(*) FROM nick95.pag
WHERE NOT REGEXP_LIKE(pubmed_id, '^\d+$') -- 31,629 are not numeric
;

SELECT count(*) FROM nick95.pag
WHERE REGEXP_LIKE(pubmed_id, '^\d+\.0$') -- all 31,629 of these are numeric with a .0 at the end
;

UPDATE nick95.pag 
SET pubmed_id = REPLACE(pubmed_id, '.0', '')
;

SELECT pubmed_id FROM nick95.pag
WHERE REGEXP_LIKE(pubmed_id, '^\d+$') -- now all non-nulls match this so it seems to have worked
;

SELECT count(*) FROM nick95.pag
WHERE pubmed_id IS NULL -- 84,589 are null
;

-- Now to change the column to a numeric one it takes a few steps (because there is already data in it)

ALTER TABLE nick95.pag
ADD pubmed_id1 NUMBER
;

UPDATE nick95.pag
SET pubmed_id1 = pubmed_id
;

update nick95.pag
SET pubmed_id = NULL
;

ALTER TABLE nick95.pag
MODIFY pubmed_id INTEGER
;

UPDATE nick95.pag
SET pubmed_id = pubmed_id1
;

ALTER TABLE nick95.pag
DROP COLUMN pubmed_id1
;
