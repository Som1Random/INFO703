-- The goal of this code is to create a cleaned up version of PAGER that has a strict relational database schema, as Jake detailed in his lectures
-- I will aim to just make a cleaned up human only version, as it simplifies the keys
-- This will involve the following tables: 
-- PAG, containing descriptions of each PAG ID (including SOURCE and TYPE as foreign keys)
-- GENE, containing descriptions of each human GENE ID including symbol etc.
-- PAG_TO_GENE, containing the genes within each PAG (essentially mapping PAG_ID to GENE_ID)
-- SOURCE, containing a description of each source with a source primary key that maps to the PAG table
-- TYPE, containing a description of each type of PAG with a type primary key that maps to the PAG table
-- PAG_TO_PAG_M, containing information on all m-type PAG to PAG relationships
-- PAG_TO_PAG_R, containing information on all r-type PAG to PAG relationships
-- GENE_TO_GENE, containing gene regulatory relationships

-- First, making the PAG table itself
CREATE TABLE nick95.pag_to_source
AS(SELECT gs_id, source
FROM nick95.ds_gs_all_source)
;

CREATE TABLE nick95.pag_temp
AS (SELECT gs_id pag_id, name, gs_size pag_size, coco_v2 nCoCo, description, original_id, link url, reference, pubmed_id, contributed_by, curator, curator_contact, record_date, version pager_version
FROM nick95.ds_gs_all
WHERE organism = 'Homo sapiens')
;

CREATE TABLE nick95.pag_temp2
AS (SELECT * 
FROM nick95.pag_temp a, nick95.pag_to_source b
WHERE a.pag_id = b.gs_id)
;

CREATE TABLE nick95.pag_to_type
AS(SELECT gs_id, type
FROM nick95.ds_gs_all_type)
;

ALTER TABLE nick95.pag_temp2
DROP COLUMN gs_id
;

CREATE TABLE nick95.pag_temp3
AS (SELECT * 
FROM nick95.pag_temp2 a, nick95.pag_to_type b
WHERE a.pag_id = b.gs_id)
;

ALTER TABLE nick95.pag
DROP COLUMN gs_id
;

DROP TABLE pag_temp
;

DROP TABLE pag_temp2
;

DROP TABLE pag_to_type
;

DROP TABLE pag_to_source
;

CREATE TABLE nick95.pag
AS(SELECT pag_id, name, pag_size, nCoCo, type, description, source, original_id, url, reference, pubmed_id, contributed_by, curator, curator_contact, record_date, pager_version
FROM nick95.pag_temp3)
;

DROP TABLE pag_temp3
;

CREATE TABLE nick95.pag_coco
AS (SELECT * FROM PAGER3.ds_gs_all_coco_v2)
;

-- Next, making GENE table, need to add RP-score to this (which needs to be calculated for all new entries (currently has 7.3m out of 9.4m))
CREATE TABLE nick95.gene
AS (SELECT geneid AS entrez_id, symbol, description, synonyms, other_designations, type_of_gene, feature_type, chromosome, map_location, dbxrefs, modification_date
FROM nick95.gene_human
WHERE tax_id = 9606)
;

CREATE TABLE nick95.gene_score
AS (SELECT * FROM PAGER3.ds_gs_all_gene_score)
;

-- PAG_TO_GENE
CREATE TABLE nick95.pag_to_gene
AS(SELECT gs_id AS pag_id, gene_id AS entrez_id
FROM nick95.ds_gs_all_gene)
;

-- SOURCE
CREATE TABLE nick95.source
(source varchar(100),
description varchar(1000),
primary key(source)
)
;

INSERT INTO nick95.source VALUES ('BioCarta', 'Curated protein pathways');

INSERT INTO nick95.source VALUES ('Cell', 'Gene reported in articles published in Cell');

INSERT INTO nick95.source VALUES ('CellMarker', 'Cell marker database for human and mouse cell types');

INSERT INTO nick95.source VALUES ('DSigDB', 'Drugs/compounds and their target genes');

INSERT INTO nick95.source VALUES ('GAD', 'Genetic association data from complex diseases and disorders');

INSERT INTO nick95.source VALUES ('GOA', 'Functional gene annotations');

INSERT INTO nick95.source VALUES ('GOA_EXCL', 'Functional gene annotations (excluded)');

INSERT INTO nick95.source VALUES ('GTEx', 'Tissue specific gene expression data linked to genotype data');

INSERT INTO nick95.source VALUES ('GWAS Catalog', 'Variant-trait associations in humans');

INSERT INTO nick95.source VALUES ('GeneSigDB', 'Gene expression signatures from literatur');

INSERT INTO nick95.source VALUES ('Genome Data', 'Database of Genes. (Reference only not PAG)');

INSERT INTO nick95.source VALUES ('GeoMx Cancer Transcriptome Atlas', 'Gene expression in cancers');

INSERT INTO nick95.source VALUES ('HPA-CellAtlas', 'Gene expression in subcellular locations');

INSERT INTO nick95.source VALUES ('HPA-FANTOM5', 'Cell type specific gene expression profiles');

INSERT INTO nick95.source VALUES ('HPA-GTEx', 'Tissue specific gene expression data linked to genotype data - seems to have been done independent of GTEx');

INSERT INTO nick95.source VALUES ('HPA-PathologyAtlas', 'RNA expression profiles in different cancer types');

INSERT INTO nick95.source VALUES ('HPA-RNAcon', 'RNA expression profiles in different tissue types - consensus');

INSERT INTO nick95.source VALUES ('HPA-TCGA', 'Gene expression data from cancer');

INSERT INTO nick95.source VALUES ('HPA-normProtein', 'Protein expression profiles in different cell types');

INSERT INTO nick95.source VALUES ('HPA-normRNA', 'RNA expression profiles in different tissue types');

INSERT INTO nick95.source VALUES ('I2D', 'Protein-protein interactions');

INSERT INTO nick95.source VALUES ('Isozyme', 'Gene expression from Bulent et al., 2014');

INSERT INTO nick95.source VALUES ('KEGG', 'Sets of proteins participating in pathways');

INSERT INTO nick95.source VALUES ('KEGG_2021_HUMAN', 'Sets of proteins participating in pathways');

INSERT INTO nick95.source VALUES ('MSigDB', 'Curated gene sets (based on expression signatures) and regulatory target gene sets (based on miRNA and TF target sites in promotors and 3-UTRs), Curated gene sets from pathway databases (including BIOCARTA, KEGG, REACTOME, WikiPathways), Computational gene sets based on cancer-related microarray data, and Immunologic signature gene sets');

INSERT INTO nick95.source VALUES ('Microcosm Targets', 'miRNA-target interaction database');

INSERT INTO nick95.source VALUES ('NCI-Nature Curated', 'Pathway interaction database');

INSERT INTO nick95.source VALUES ('NGS Catalog', 'Next-generation sequencing database');

INSERT INTO nick95.source VALUES ('Pfam', 'Protein family database');

INSERT INTO nick95.source VALUES ('PharmGKB', 'Pharmacogenomics database');

INSERT INTO nick95.source VALUES ('PheWAS', 'Phenome wide association study');

INSERT INTO nick95.source VALUES ('Protein Lounge', 'siRNA target database, a complete Peptide-Antigen target database and a Kinase-Phosphatase database');

INSERT INTO nick95.source VALUES ('Reactome', 'Sets of proteins participating in pathways');

INSERT INTO nick95.source VALUES ('Reactome_2021', 'Sets of proteins participating in pathways');

INSERT INTO nick95.source VALUES ('SIGNOR', 'Proteins involved in pathways with known chemical relationships');

INSERT INTO nick95.source VALUES ('Spike', 'Curated human signaling pathways');

INSERT INTO nick95.source VALUES ('TargetScan', 'Target genes of microRNAs predicted by searching genes for sites matching miRNA seed regions');

INSERT INTO nick95.source VALUES ('WikiPathway', 'Sets of proteins participating in pathways');

INSERT INTO nick95.source VALUES ('WikiPathway_2021', 'Sets of proteins participating in pathways');

INSERT INTO nick95.source VALUES ('mirTARbase', 'miRNA-target interaction database');

-- TYPE
CREATE TABLE nick95.type
(type varchar(10),
description varchar(1000),
primary key(type)
)
;

INSERT INTO nick95.type 
VALUES ('P', 'PAG containing pathway information, requiring evidence for direct interaction or regulation of genes within it')
;

INSERT INTO nick95.type 
VALUES ('A', 'PAG containing genes that share an annotation')
;

INSERT INTO nick95.type 
VALUES ('G', 'PAG containing genes that were identified from a large-scale experiment such as GWAS or RNA-seq')
;

-- GENE_TO_GENE
CREATE TABLE nick95.gene_to_gene
AS (SELECT * FROM PAGER3.ds_gr_all_human)
;

CREATE TABLE nick95.gene_to_gene2
AS (SELECT * FROM PAGER3.happi2_3star_sort)
;



-- PAG_TO_PAG
CREATE TABLE nick95.pag_to_pag_m
AS (SELECT * FROM pager3.ds_gs_all_overlap_v2)
;

CREATE TABLE nick95.pag_to_pag_r
AS (SELECT * FROM pager3.ds_gs_all_reg_v2)
;
