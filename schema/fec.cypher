CREATE CONSTRAINT ON (n:Candidate) ASSERT n.CAND_ID IS UNIQUE;
CREATE CONSTRAINT ON (n:Committee) ASSERT n.CMTE_ID IS UNIQUE;
CREATE CONSTRAINT ON (n:IndivContrib) ASSERT n.SUB_ID IS UNIQUE;