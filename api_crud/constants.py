from django.db.models import TextChoices
from django.templatetags.static import static

# These are used in the Data Aggregator return case view
# to unverify steps
ACCOUNT_MANAGER_PAGE_ALIASES = (
    ("customer-profile", "Customer Profile"),
    ("company-info", "Company Info"),
    ("covid-19", "COVID-19"),
    ("PPP", "PPP"),
    ("payroll-wages", "Payroll Wages"),
    ("benefits", "Benefits"),
    ("payroll-tax-returns", "Payroll Tax Returns"),
    ("PNL", "PNL"),
)

IR_TO_EY_STATUS = (
    (0, "Passed KYC"),
    (1, "EA signed"),
    (2, "Inactive"),
    (3, "Disengaged"),
    (4, "Terminated"),
    (5, "Pending SoF signature"),
    (6, "Complete"),
    (7, "Audit initiated"),
)

ASURE_TO_IR_STATUS = (
    (0, "Pending Approval"),
    (1, "Error"),
    (2, "Filed"),
    (3, "Completed"),
)


class MobileSteps(TextChoices):
    COMPANIES_LIST = "Companies List"
    COMPANY_PROFILE = "Company Profile 3"
    PPP = "PPP 1"
    COVID_INFO = "Covid Info"
    PAYROLL_WAGES = "Payroll Wages"
    BENEFITS_FILES = "Benefits Files"
    FILES_941 = "941 Files"
    PNL = "Profit and Loss"
    APP_IN_REVIEW = "Application in Review"
    READY_FOR_TAX_PREPARER = "Ready for tax preparer"
    CALC_REFUND = "Calculating your refund"
    READY_FOR_SIGNATURE = "Ready for signature"
    CASE_SENT_IRS = "Case sent to IRS"
    AWAITING_REFUND = "Awaiting refund"
    UPLOAD_CHECKS = "Upload your checks"


DEAL_STEPS = (
    (0, "Companies List"),
    (1, "User Profile 1"),
    (2, "User Profile 2"),
    (3, "Company Profile 1"),
    (4, "Company Profile 2"),
    (5, "Company Profile 3"),
    (6, "PPP 1"),
    (7, "Covid Info"),
    (8, "Payroll Wages"),
    (9, "Benefits Files"),
    (10, "941 Files"),
    (11, "Profit and Loss"),
    (12, "Application in Review"),
    (13, "Application Compiled"),
    (14, "Choose your Tax Attorney"),
    (15, "Calculating your ERC"),
    (16, "Finalize Your Calculation"),
    (17, "Upload 2848"),
    (18, "Awaiting 941x/943x"),
    (19, "Sign Purchase Order"),
    (20, "Check Upload"),
    (21, "PEO"),
    (22, "PPP 2"),
    (23, "Interstitial"),
    (99, "Closed Lost"),
    (100, "Completed"),
)

TODO_STEP_ROUTES = dict(
    {
        "-1": "/docu_upload/",
        "14": "/list_tax_attorney_lawfirm/",
        "17": "/",  # Pending on development
        "18": "/init_2848/",
        "19": "/purchase_order/",
        "20": "/upload_checks/",
    }
)

"""
    #C-Corp
    #S-Corp
    #LLC
    #Sole Proprietorship
    #Partnership
    #501(c) Tax Exempt
"""
FILING_TYPE = (
    (1, "C-Corp"),
    (2, "S-Corp"),
    (3, "LLC"),
    (4, "Sole Proprietorship"),
    (5, "Partnership"),
    (6, "501(c) Tax Exempt"),
)

INCOME_CHOICE = (
    (1, "Less than $1,000,000"),
    (2, "$1,000,000 to $5,000,000"),
    (3, "More than $5,000,000"),
)

REVENUE_CHOICE = (
    (1, "Less than or equal to $1 Million in revenue"),
    (2, "Over $1 Million in revenue"),
)

# simplified categorization
"""
Agriculture
Business Services
Construction
Consumer Services
Education / Childcare
Electronics
Energy
Engineering
Insurance & Finance
Legal Services
Manufacturing
Medical Services
Non-Profit
Professional Services
Real Estate
Restaurants & Food Services
Retail
Software
Telecommunication
Transportation & Logistics
"""
# industry choices
INDUSTRY = (
    (1, "Agriculture"),
    (2, "Business Services"),
    (3, "Construction"),
    (4, "Consumer Services"),
    (5, "Education / Childcare"),
    (6, "Electronics"),
    (7, "Energy"),
    (8, "Engineering"),
    (9, "Insurance & Finance"),
    (10, "Legal Services"),
    (11, "Medical Services"),
    (12, "Manufacturing"),
    (13, "Non-Profit"),
    (14, "Professional Services"),
    (15, "Real Estate"),
    (16, "Restaurants & Food Services"),
    (17, "Retail"),
    (18, "Software"),
    (19, "Telecommunication"),
    (20, "Transportation & Logistics"),
)

"""
    #How did you hear about us?
    #Sirius XM Radio"
    #Bill Handel - KFI Radio
    #KNX-AM Radio
    #Bank Referral
    #Online Search
    #Friend or Colleague
    #Digital Ad
    #American Recovery Association
    #CURepossession.com
    #Other
    #iHeartRadio
    #Radio
    #Podcast
    #Entrepreneurs' Organization
    #Refer & Earn
"""

COVID_DISRUPTION_DESCRIPTION_MIN_LENGTH = 200
COVID_DISRUPTION_DESCRIPTION_MAX_LENGTH = 1000

IMPACT_CHOICES = (
    (1, "Full shutdown"),
    (2, "Partial shutdown"),
    (3, "Interrupted operations"),
    (4, "Supply chain interruptions"),
    (5, "Inability to access equipment"),
    (6, "Limited capacity to operate"),
    (7, "Inability to work with vendors"),
    (8, "Reduction in services or goods offered to your customers"),
    (10, "Other"),
    (11, "Cutdown in your hours of operation"),
    (12, "Shifting hours to increase sanitation of your facility"),
    (
        13,
        "Employee absences due to quarantining requirements, exposures, or positive COVID cases",
    ),
)

IMPACT_CHOICES_ORDER = (
    (1, 0),
    (2, 1),
    (3, 2),
    (4, 3),
    (5, 4),
    (6, 5),
    (7, 6),
    (8, 7),
    (9, 2),  # Map to Interrupted Operations
    (11, 9),
    (12, 10),
    (13, 11),
    (10, 12),
)

IMPACT_QUARTERS = (
    (1, "2020 Q1"),
    (2, "2020 Q2"),
    (3, "2020 Q3"),
    (4, "2020 Q4"),
    (5, "2021 Q1"),
    (6, "2021 Q2"),
    (7, "2021 Q3"),
    (8, "2021 Q4"),
)

# 941, PnL:
# Q1-Q4 2019
# Q1-Q4 2020
# Q1-Q3 2021
# IF the business started after FEB 15 2020
# THEN we can include Q4 2021 documentation.
PNL_UPLOAD_QUARTERS = (
    (1, "2019 Q1"),
    (2, "2019 Q2"),
    (3, "2019 Q3"),
    (4, "2019 Q4"),
    (5, "2020 Q1"),
    (6, "2020 Q2"),
    (7, "2020 Q3"),
    (8, "2020 Q4"),
    (9, "2021 Q1"),
    (10, "2021 Q2"),
    (11, "2021 Q3"),
    (12, "2021 Q4"),
)

SHORT_MONTHS = (
    (1, "Jan"),
    (2, "Feb"),
    (3, "Mar"),
    (4, "Apr"),
    (5, "May"),
    (6, "Jun"),
    (7, "Jul"),
    (8, "Aug"),
    (9, "Sep"),
    (10, "Oct"),
    (11, "Nov"),
    (12, "Dec"),
)

LONG_MONTHS = (
    (1, "January"),
    (2, "February"),
    (3, "March"),
    (4, "April"),
    (5, "May"),
    (6, "June"),
    (7, "July"),
    (8, "August"),
    (9, "September"),
    (10, "October"),
    (11, "November"),
    (12, "December"),
)

# gross monthly payroll upload
UPLOAD_MONTHS = (
    (1, "2020 Jan"),
    (2, "2020 Feb"),
    (3, "2020 Mar"),
    (4, "2020 Apr"),
    (5, "2020 May"),
    (6, "2020 Jun"),
    (7, "2020 Jul"),
    (8, "2020 Aug"),
    (9, "2020 Sep"),
    (10, "2020 Oct"),
    (11, "2020 Nov"),
    (12, "2020 Dec"),
    (13, "2021 Jan"),
    (14, "2021 Feb"),
    (15, "2021 Mar"),
    (16, "2021 Apr"),
    (17, "2021 May"),
    (18, "2021 Jun"),
    (19, "2021 Jul"),
    (20, "2021 Aug"),
    (21, "2021 Sep"),
    (22, "2021 Oct"),
    (23, "2021 Nov"),
    (24, "2021 Dec"),
)

# PPP loan participate rounds
ROUNDS = ((1, "Round 1"), (2, "Round 2"), (3, "Both"))

PPP_ROUNDS_DICT = {1: "first", 2: "second", 3: "both"}

ROUNDS_SINGLE = ((1, "Round 1"), (2, "Round 2"))

# refund check year
REFUND_YEARS = ((1, "2019"), (2, "2020"), (3, "2021"))

# these are the 50 states
STATES = (
    (1, "Alabama (AL)"),
    (2, "Alaska (AK)"),
    (3, "Arizona (AZ)"),
    (4, "Arkansas (AR)"),
    (5, "California (CA)"),
    (6, "Colorado (CO)"),
    (7, "Connecticut (CT)"),
    (8, "Delaware (DE)"),
    (9, "Washington D.C. (DC)"),
    (10, "Florida (FL)"),
    (11, "Georgia (GA)"),
    (12, "Hawaii (HI)"),
    (13, "Idaho (ID)"),
    (14, "Illinois (IL)"),
    (15, "Indiana (IN)"),
    (16, "Iowa (IA)"),
    (17, "Kansas (KS)"),
    (18, "Kentucky (KY)"),
    (19, "Louisiana (LA)"),
    (20, "Maine (ME)"),
    (21, "Maryland (MD)"),
    (22, "Massachusetts (MA)"),
    (23, "Michigan (MI)"),
    (24, "Minnesota (MN)"),
    (25, "Mississippi (MS)"),
    (26, "Missouri (MO)"),
    (27, "Montana (MT)"),
    (28, "Nebraska (NE)"),
    (29, "Nevada (NV)"),
    (30, "New Hampshire (NH)"),
    (31, "New Jersey (NJ)"),
    (32, "New Mexico (NM)"),
    (33, "New York (NY)"),
    (34, "North Carolina (NC)"),
    (35, "North Dakota (ND)"),
    (36, "Ohio (OH)"),
    (37, "Oklahoma (OK)"),
    (38, "Oregon (OR)"),
    (39, "Pennsylvania (PA)"),
    (40, "Rhode Island (RI)"),
    (41, "South Carolina (SC)"),
    (42, "South Dakota (SD)"),
    (43, "Tennessee (TN)"),
    (44, "Texas (TX)"),
    (45, "Utah (UT)"),
    (46, "Vermont (VT)"),
    (47, "Virginia (VA)"),
    (48, "Washington (WA)"),
    (49, "West Virginia (WV)"),
    (50, "Wisconsin (WI)"),
    (51, "Wyoming (WY)"),
)

# these are the 50 states abbreviation
ABBR_STATES = (
    (1, "AL"),
    (2, "AK"),
    (3, "AZ"),
    (4, "AR"),
    (5, "CA"),
    (6, "CO"),
    (7, "CT"),
    (8, "DE"),
    (9, "DC"),
    (10, "FL"),
    (11, "GA"),
    (12, "HI"),
    (13, "ID"),
    (14, "IL"),
    (15, "IN"),
    (16, "IA"),
    (17, "KS"),
    (18, "KY"),
    (19, "LA"),
    (20, "ME"),
    (21, "MD"),
    (22, "MA"),
    (23, "MI"),
    (24, "MN"),
    (25, "MS"),
    (26, "MO"),
    (27, "MT"),
    (28, "NE"),
    (29, "NV"),
    (30, "NH"),
    (31, "NJ"),
    (32, "NM"),
    (33, "NY"),
    (34, "NC"),
    (35, "ND"),
    (36, "OH"),
    (37, "OK"),
    (38, "OR"),
    (39, "PA"),
    (40, "RI"),
    (41, "SC"),
    (42, "SD"),
    (43, "TN"),
    (44, "TX"),
    (45, "UT"),
    (46, "VT"),
    (47, "VA"),
    (48, "WA"),
    (49, "WV"),
    (50, "WI"),
    (51, "WY"),
)

FINCH_TABLE_COLUMNS = {
    "2020": [
        "January",
        "February",
        "March",
        "Q1",
        "April",
        "May",
        "June",
        "Q2",
        "July",
        "August",
        "September",
        "Q3",
        "October",
        "November",
        "December",
        "Q4",
    ],
    "2021": [
        "January",
        "February",
        "March",
        "Q1",
        "April",
        "May",
        "June",
        "Q2",
        "July",
        "August",
        "September",
        "Q3",
    ],
}

PNL_TABLE_COLUMNS = (
    "Income",
    "Cost Of Sales",
    "Gross Profit",
    "Expenses",
    "Net Operating Profit",
    "Other Expenses",
    "Other Income",
    "Net Other Income",
    "Net Profit",
)

INCOME_TABLE_COLUMNS = ("Income", "2019 Q Income", "2019 Q Change", "Last Q Change")
INCOME_TABLE_QUARTERS = (
    (6, "2020 Q2", 2),
    (7, "2020 Q3", 3),
    (8, "2020 Q4", 4),
    (9, "2021 Q1", 1),
    (10, "2021 Q2", 2),
    (11, "2021 Q3", 3),
)

# THESE ARE FOR TEMPLATE RENDERING OF FILE UPLOAD FIELDS
MONTHLY_GROSS_MONTHS = {
    "2020": [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ],
    "2021": [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
    ],
}

EBF_MONTHS = {
    "2020": [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ],
    "2021": [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
    ],
}

PNL_QUARTERS = {
    "2019": ["Q1", "Q2", "Q3", "Q4"],
    "2020": ["Q1", "Q2", "Q3", "Q4"],
    "2021": ["Q1", "Q2", "Q3"],
}

UPLOAD_CHECK_QUARTERS = {
    "2020": ["Q1", "Q2", "Q3", "Q4"],
    "2021": ["Q1", "Q2", "Q3", "Q4"],
}

PAYROLL_QUARTERS = {
    "2019": ["Q1", "Q2", "Q3", "Q4"],
    "2020": ["Q1", "Q2", "Q3", "Q4"],
    "2021": ["Q1", "Q2", "Q3"],
}

IMPROVE_PRODUCT_CHOICES = (
    (1, "Concepts"),
    (2, "Equipment"),
    (3, "Formulas"),
    (4, "Hardware"),
    (5, "Internal or External Processes"),
    (6, "Manufacturing Design or Processes"),
    (7, "Prototypes or Models"),
    (8, "Software"),
    (9, "Testing or Training"),
)

OPTIONS_941 = ((1, "Quarterly 941"), (2, "Annual 943"))

UPLOAD_YEARS = ((1, "2019"), (2, "2020"), (3, "2021"))

UPLOAD_YEARS1 = (("2019"), ("2020"), ("2021"))

# FINCH_PROVIDERS = ((PROVIDER_NAME, PROVIDER_ID, PROVIDER_IMAGE))
FINCH_PROVIDERS = (
    ("BambooHR", "bamboo_hr", static("application/img/finch_providers/bamboohr.svg")),
    ("bob", "bob", static("application/img/finch_providers/bob.png")),
    ("Gusto", "gusto", static("application/img/finch_providers/gusto.svg")),
    ("Humaans", "humaans", static("application/img/finch_providers/humaans.png")),
    ("Insperity", "insperity", static("application/img/finch_providers/insperity.svg")),
    ("Justworks", "justworks", static("application/img/finch_providers/justworks.png")),
    ("Namely", "namely", static("application/img/finch_providers/namely.svg")),
    (
        "Paychex Flex",
        "paychex_flex",
        static("application/img/finch_providers/paychex.svg"),
    ),
    ("Paycom", "paycom", static("application/img/finch_providers/paycom.png")),
    ("Paylocity", "paylocity", static("application/img/finch_providers/paylocity.png")),
    ("Personio", "personio", static("application/img/finch_providers/personio.svg")),
    (
        "QuickBooks Payroll",
        "quickbooks",
        static("application/img/finch_providers/quickbooks.png"),
    ),
    ("Rippling", "rippling", static("application/img/finch_providers/rippling.png")),
    (
        "Run Powered by ADP",
        "adp_run",
        static("application/img/finch_providers/adp_run.png"),
    ),
    ("Sage HR", "sage_hr", static("application/img/finch_providers/sage.png")),
    ("Sapling", "sapling", static("application/img/finch_providers/sapling.svg")),
    (
        "Sequoia One",
        "sequoia_one",
        static("application/img/finch_providers/sequoia.png"),
    ),
    (
        "Square Payroll",
        "square_payroll",
        static("application/img/finch_providers/square.png"),
    ),
    ("TriNet", "trinet", static("application/img/finch_providers/trinet.svg")),
    (
        "UltiPro (UKG Pro)",
        "ulti_pro",
        static("application/img/finch_providers/ukg.png"),
    ),
    ("Wave", "wave", static("application/img/finch_providers/wave.svg")),
    ("Workday", "workday", static("application/img/finch_providers/workday.png")),
    ("Zenefits", "zenefits", static("application/img/finch_providers/zenefits.svg")),
)

CODAT_PROVIDERS = (
    ("Clear Books", "jhch"),
    ("Kash Flow", "wvzu"),
    ("Sand Box", "mqjo"),
    ("Sage 50", "hbql"),
    ("Quick Books", "pqsw"),
    ("Oracle Netsuite", "akxx"),
)

FILE_STATUS = ((1, "Pending Review"), (2, "Approved"), (3, "Rejected"), (4, "Flagged"))

REJECT_REASONS = (
    (1, "It looks like this document is for the incorrect year"),
    (2, "It looks like this document is for the incorrect quarter"),
    (3, "It looks like this document is for the incorrect month"),
    (4, "This document cannot be read. Please try again."),
    (5, "We are unable to open this document"),
    (6, "It looks like this is the incorrect document"),
    (7, "This document is missing required information"),
    (8, "It looks like you’ve already submitted this document"),
    (9, "Please separate this document into quarter/month format"),
    (10, "File invalidation e.g. file in wrong format")
)

TAX_ASSOCIATIONS = (
    (1, "None"),
    (2, "2020 Q1 941x"),
    (3, "2020 Q2 941x"),
    (4, "2020 Q3 941x"),
    (5, "2020 Q4 941x"),
    (6, "2021 Q1 941x"),
    (7, "2021 Q2 941x"),
    (8, "2021 Q3 941x"),
    (9, "2021 Q4 941x"),
)

# here are the groups for login permission
GROUPS = (
    (1, "Customer"),
    (2, "CSC User"),
    (3, "CSC Team Lead"),
    (4, "CSC Manager"),
    (5, "Data Aggregator"),
    (6, "Data Aggregator Manager"),
    (7, "CPA"),
    (8, "Super Admin"),
    (9, "Executive"),
    (10, "Law Admin"),
)

DEAL_CLOSED_CATEGORIES = (
    (1, "Client passed away"),
    (2, "Spam lead"),
    (3, "Disqualified"),
    (4, "No recovery"),
    (5, "Client's CPA killed the contract"),
    (6, "Client isn't responding to communication"),
    (7, "Client chose competitor"),
    (8, "ERC already collected by client"),
    (9, "Client no longer responding to AM"),
    (10, "AM judgement call"),
    (11, "Client unwilling to pay fee"),
    (12, "QC rejected"),
    (13, "Client was discovered to be a bad actor"),
    (14, "Rejected by tax attorney"),
    (15, "Test application"),
)

# role list for admin members
MEMBER_GROUPS = (
    (2, "CSC User"),
    (3, "CSC Team Lead"),
    (4, "CSC Manager"),
    (5, "Data Aggregator"),
    (6, "Data Aggregator Manager"),
    (7, "CPA"),
    (8, "Super Admin"),
    (9, "Executive"),
    (10, "Law Admin"),
)

ASSOCIATIONS = (
    (1, "None"),
    (2, "2019 941 Q1"),
    (3, "2019 941 Q2"),
    (4, "2019 941 Q3"),
    (5, "2019 941 Q4"),
    (6, "2020 941 Q1"),
    (7, "2020 941 Q2"),
    (8, "2020 941 Q3"),
    (9, "2020 941 Q4"),
    (10, "2021 941 Q1"),
    (11, "2021 941 Q2"),
    (12, "2021 941 Q3"),
    (13, "2021 941 Q4"),
    (16, "2019 943"),
    (17, "2020 943"),
    (18, "2021 943"),
    (20, "2020 Payroll January"),
    (21, "2020 Payroll February"),
    (22, "2020 Payroll March"),
    (23, "2020 Payroll April"),
    (24, "2020 Payroll May"),
    (25, "2020 Payroll June"),
    (26, "2020 Payroll July"),
    (27, "2020 Payroll August"),
    (28, "2020 Payroll September"),
    (29, "2020 Payroll October"),
    (30, "2020 Payroll November"),
    (31, "2020 Payroll December"),
    (32, "2021 Payroll January"),
    (33, "2021 Payroll February"),
    (34, "2021 Payroll March"),
    (35, "2021 Payroll April"),
    (36, "2021 Payroll May"),
    (37, "2021 Payroll June"),
    (38, "2021 Payroll July"),
    (39, "2021 Payroll August"),
    (40, "2021 Payroll September"),
    (41, "2021 Payroll October"),
    (42, "2021 Payroll November"),
    (43, "2021 Payroll December"),
    (50, "2020 Employer Benefit January"),
    (51, "2020 Employer Benefit February"),
    (52, "2020 Employer Benefit March"),
    (53, "2020 Employer Benefit April"),
    (54, "2020 Employer Benefit May"),
    (55, "2020 Employer Benefit June"),
    (56, "2020 Employer Benefit July"),
    (57, "2020 Employer Benefit August"),
    (58, "2020 Employer Benefit September"),
    (59, "2020 Employer Benefit October"),
    (60, "2020 Employer Benefit November"),
    (61, "2020 Employer Benefit December"),
    (62, "2021 Employer Benefit January"),
    (63, "2021 Employer Benefit February"),
    (64, "2021 Employer Benefit March"),
    (65, "2021 Employer Benefit April"),
    (66, "2021 Employer Benefit May"),
    (67, "2021 Employer Benefit June"),
    (68, "2021 Employer Benefit July"),
    (69, "2021 Employer Benefit August"),
    (70, "2021 Employer Benefit September"),
    (71, "2021 Employer Benefit October"),
    (72, "2021 Employer Benefit November"),
    (73, "2021 Employer Benefit December"),
    (80, "2019 Profit-Loss Q1"),
    (81, "2019 Profit-Loss Q2"),
    (82, "2019 Profit-Loss Q3"),
    (83, "2019 Profit-Loss Q4"),
    (84, "2020 Profit-Loss Q1"),
    (85, "2020 Profit-Loss Q2"),
    (86, "2020 Profit-Loss Q3"),
    (87, "2020 Profit-Loss Q4"),
    (88, "2021 Profit-Loss Q1"),
    (89, "2021 Profit-Loss Q2"),
    (90, "2021 Profit-Loss Q3"),
    (91, "2021 Profit-Loss Q4"),
    (100, "PPP Round 1"),
    (101, "PPP Round 2"),
    (110, "Engagement Agreement"),
    (111, "Tax Calculation"),
    (112, "Statement Of Fact"),
    (113, "Attorney Requested Document"),
    (114, "Bank Statements"),
    (115, "Income Statements"),
    (116, "941s"),
    (117, "Payroll Information"),
    (118, "Benefit Information"),
    (119, "PPP Information"),
    (120, "Other"),
)

# These need to match up with their counterparts in the associations list :/
REQUEST_DOCUMENTS = (
    (114, "Bank Statements"),
    (115, "Income Statements"),
    (116, "941s"),
    (117, "Payroll Information"),
    (118, "Benefit Information"),
    (119, "PPP Information"),
    (120, "Other"),
)

ROLE_GROUPS = ((1, "Deal Owner"), (2, "CSC Owner"))

DA_STATUS = ((1, "N/A"), (2, "Rejected"), (3, "Approved"))

CPA_STATUS = ((1, "N/A"), (2, "Open"), (3, "Closed"))

BUSINESS_OWNER_STATUS = (
    (1, "I am a business owner"),
    (2, "I am representing a buisness owner"),
    (3, "I am an individual employee"),
)

PAYROLL_941_DOCS = "PAYROLL941DOCS"
PAYROLL_DOCS = "PAYROLLDOCS"
PPP_LOAN_DOCS = "PPPLOANDOCS"
PNL_DOCS = "PNLDOCS"
EBC_DOCS = "EBCDOCS"
APPLICATON_STEPS = [
    {"title": "Application Submitted"},
    {"title": "Application in Review"},
    {"title": "Application Compiled"},
    # { "title": "Choose your Tax Attorney"},
    {"title": "Calculating your ERC"},
    {"title": "Finalize Your Calculation"},
    {"title": "Submit To IRS"},
    {"title": "Upload Checks"},
]

QUARTER_MAP = (
    (1, "Q1"),
    (2, "Q2"),
    (3, "Q3"),
    (4, "Q4"),
)

QUARTERS = {
    "2019": ["Q1", "Q2", "Q3", "Q4"],
    "2020": ["Q1", "Q2", "Q3", "Q4"],
    "2021": ["Q1", "Q2", "Q3"],
}

MONTHS = {
    "2020": [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ],
    "2021": [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
    ],
}

# these status are just base upon DEAL_STEPS
APPLICATION_STATUS = {
    "11": "Please complete your application.",
    "12": "Our team is reviewing your documents, we'll notify you of any changes.",
    "13": "Your application complied.",
    "14": "Pick from our vetted selection of tax attorneys to prepare your 941x.",
    "15": "Your tax attorney is preparing your tax packet and is expected to finish in 2-3 days.",
    "15b": "Your tax attorney needs additional documents to complete proccesing of your 941x.",
    "16": "Your tax attorney has completed your packet and needs to have it reviewed and approved by you before sending to the IRS.",
    "17": "Awaiting upload of 2848.",
    "18": "Awaiting final confirmation from your tax attorney.",
    "19": "Pending final agreement that allows Innovation Refunds to submit to the IRS.",
    "20": "Your check will arrive soon. Remember to upload when it does!",
}

TODO_STEP_STATUS = {
    "submitted": "Please complete your application.",
    "completed": "Our team is reviewing your documents. We'll notify you of any changes.",
    "tax-attorney": "You've been matched with a tax firm to process your refund. Confirm your tax preparer to continue.",
    "calculating-refund": "Your tax preparer is filling out the tax forms to calculate your final refund amount.",
    "signature": "Review and sign the Service Agreement, so we can send your case to the IRS.",
    "case-sent-irs": "We'll let you know as soon as we've sent your case.",
    "awaiting-refund": "Waiting for the IRS to confirm receipt.",
    "upload-checks": "Upload your refund checks now that you've got them!",
}

RELATIONSHIP = (
    (1, "Child or descendant of a child"),
    (2, "Sibling or step-sibling"),
    (3, "Father, mother, or an ancestor of either"),
    (4, "Stepfather or stepmother"),
    (5, "Niece or nephew"),
    (6, "Aunt or uncle"),
    (7, "In-law (mother, father, sister, or brother)"),
    (8, "Spouse"),
)

DATETIME_STANDARD_FORMAT = "%Y-%m-%d"
DATETIME_VERIFICATION_FORMAT = "%b %d, %Y (%I:%M %p)"
DATE_VERIFICATION_FORMAT = "%b %d, %Y"

AFFECTED_YEARS = (2019, 2020, 2021)
