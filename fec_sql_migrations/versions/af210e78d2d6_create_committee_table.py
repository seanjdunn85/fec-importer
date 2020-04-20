"""create committee table

Revision ID: af210e78d2d6
Revises: 
Create Date: 2020-04-19 13:10:17.562249

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'af210e78d2d6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'committees',
        sa.Column('id', sa.Integer, primary_key=True),

        sa.Column('committee_id',
                  sa.VARCHAR(length=9),
                  primary_key=False,
                  nullable=False,
                  comment="""A 9-character alpha-numeric code assigned to a committee by the Federal Election 
                  Commission. Committee IDs are unique and an ID for a specific committee always remains the same.""",
                  index="Unique"),

        sa.Column('name',
                  sa.VARCHAR(200),
                  nullable=True
                  ),

        sa.Column('treasurer_name',
                  sa.VARCHAR(90),
                  nullable=True,
                  comment="""The officially registered treasurer for the committee."""
        ),
        sa.Column('street_one',
                  sa.VARCHAR(length=34),
                  nullable=True),
        sa.Column('street_two',
                  sa.VARCHAR(length=34),
                  nullable=True),
        sa.Column('city',
                  sa.VARCHAR(length=30),
                  nullable=True),
        sa.Column('state',
                  sa.VARCHAR(length =2),
                  nullable=True),
        sa.Column('designation',
                  sa.VARCHAR(length=1),
                  comment="""
                        A = Authorized by a candidate
                        B = Lobbyist/Registrant PAC
                        D = Leadership PAC
                        J = Joint fundraiser
                        P = Principal campaign committee of a candidate
                        U = Unauthorized""",
                  nullable=True),
        sa.Column("committee_type",
                  sa.VARCHAR(length=1),
                  comment="""List of committee type codes: https://www.fec.gov/campaign-finance-data/committee-type
                  -code-descriptions """,
                  nullable=True
                  ),
        sa.Column("party",
                  sa.VARCHAR(length=3),
                  comment=""""List of party codes: https://www.fec.gov/campaign-finance-data/party-code-descriptions""",
                  nullable=True
                  ),
        sa.Column("filing_frequency",
                  sa.VARCHAR(1),
                  comment="""
                    A = Administratively terminated
                    D = Debt
                    M = Monthly filer
                    Q = Quarterly filer
                    T = Terminated
                    W = Waived""",
                  nullable=True),
        sa.Column("organization_type",
                  sa.VARCHAR(length=1),
                  comment="""
                  Interest group category:
                  
                    C = Corporation
                    L = Labor organization
                    M = Membership organization
                    T = Trade association
                    V = Cooperative
                    W = Corporation without capital stock""",
                  nullable=True
                  ),
        sa.Column("connected_organization_name",
                  sa.VARCHAR(length=200),
                  nullable=True
                  ),
        sa.Column("candidate_id",
                  sa.VARCHAR(length=9),
                  comment="""When a committee has a committee type designation of H, S, or P, the candidate's 
                  identification number will be entered in this field""",
                  nullable=True
                  )

    )
    pass


def downgrade():
    op.drop_table("committees")
    pass
