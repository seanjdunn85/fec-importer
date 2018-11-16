# FEC Import

The fec-importer downloads and imports FEC disclosures into Neo4j. Follow the money!

## Getting Started

Install Neo4j (https://neo4j.com/download/) and create a database named "fec". Neo4j Desktop appears to run only one database at a time and therefor doesn't require a database name when executing queries, but for future development we will name our MySQL database "fec" and the Neo4j database has the same name.

Rename the file `fec.config.local.json` to `fec.config.json` and change the Neo4j credentials and port for your environment.


### Python Dependecies
Install these guys:
`termcolor`
`py2neo`

### Neo4j Configurations

You must create a symlink in the Neo4j database's `import` directory. The symlink must be named `fec` and point to the the `zips` directory in this project.

The indices used for varius node types are created on each call to update the database.

### Directory Structure
Directories will be created on the first execution of update.py.  Executing the script with the argument ``--update-current-year`` or `-U` will overwrite the current election cycle datadumps, but none of the past election cycle dumps.

### The Disclosure Types

#### Individual contributions

Individuals contributions are made by either people, organizations, or PACs. Only PACs are easily identifiable by a serial number. The people and organizations are identified only by text names, which of course are not unique and also are not normalized. Including a person's middle initial initial or title/honorific such as Mr, Mrs, Dr, Esq., PhD, etc for example, would make a ``GROUP BY `name` `` SQL query fail to aggregate donations properly.

For example Thomas Steyer donated \$163,837,644 under "STEYER, THOMAS F." and another \$5,431,007 under "STEYER, THOMAS". To complicate things much further, families are among the top donors. George Soros, for example, donated $26,223,011 during one election cycle according to an unnormalized name query, while it appears several members of his family also made the list of the top 1,000 donors during that election cycle, under different name permutations.

### Candidates
Candidates are given Candidate IDs that correspond the type of seat the individual is running for. One person can have more than one Candidate ID. For example, Hillary Clinton has two. One for her Senate seate (S0NY00188) and one for her Presidential runs in both 2008 and 2016 (P00003392).

### Committees

Committees are essentially Political Action Comittees. They can be either linked to a particular candidate or be independent of any particular candidate. Committees are identifiable by a unique number known as a C-number. 

### Candidate-Committee Linkages
Denotes to which candidate a committee belongs, if it belongs to any. These are edges only (not nodes) in Neo4j.

### Candidate Contributions from Committees
These contributions are from PACs to particular candidate. 

### Inter-Committee Contributions
These are contributions from one committee to another committee.
