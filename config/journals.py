"""
FT50 and UTD24 Journal Definitions

Each journal entry contains:
- name: Full journal name
- abbr: Common abbreviation
- issn: ISSN(s) for API queries
- category: Research domain
- in_ft50: Whether it's in the FT50 list
- in_utd24: Whether it's in the UTD24 list
- innovation_relevance: Relevance to innovation & entrepreneurship (high/medium/low)
- tags: Semantic tags for flexible filtering (e.g., --mode innovation)
"""

JOURNALS = [
    # ============================================================
    # Entrepreneurship & Innovation (Core - FT50)
    # ============================================================
    {
        "name": "Entrepreneurship Theory and Practice",
        "abbr": "ETP",
        "issn": ["1042-2587", "1540-6520"],
        "category": "Entrepreneurship",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "high",
        "tags": ["entrepreneurship", "innovation", "new-ventures"],
    },
    {
        "name": "Journal of Business Venturing",
        "abbr": "JBV",
        "issn": ["0883-9026"],
        "category": "Entrepreneurship",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "high",
        "tags": ["entrepreneurship", "innovation", "venture-capital", "new-ventures"],
    },
    {
        "name": "Strategic Entrepreneurship Journal",
        "abbr": "SEJ",
        "issn": ["1932-4391", "1932-443X"],
        "category": "Entrepreneurship",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "high",
        "tags": ["entrepreneurship", "innovation", "strategy"],
    },
    {
        "name": "Research Policy",
        "abbr": "RP",
        "issn": ["0048-7333"],
        "category": "Innovation & Technology Policy",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "high",
        "tags": ["innovation", "technology-policy", "r-and-d"],
    },

    # ============================================================
    # Management & Strategy (FT50 + UTD24)
    # ============================================================
    {
        "name": "Academy of Management Journal",
        "abbr": "AMJ",
        "issn": ["0001-4273", "1948-0989"],
        "category": "Management",
        "in_ft50": True,
        "in_utd24": True,
        "innovation_relevance": "high",
        "tags": ["management", "innovation", "entrepreneurship", "organization"],
    },
    {
        "name": "Academy of Management Review",
        "abbr": "AMR",
        "issn": ["0363-7425", "1930-3807"],
        "category": "Management",
        "in_ft50": True,
        "in_utd24": True,
        "innovation_relevance": "high",
        "tags": ["management", "innovation", "theory"],
    },
    {
        "name": "Administrative Science Quarterly",
        "abbr": "ASQ",
        "issn": ["0001-8392", "1930-3815"],
        "category": "Management",
        "in_ft50": True,
        "in_utd24": True,
        "innovation_relevance": "high",
        "tags": ["management", "innovation", "organization"],
    },
    {
        "name": "Strategic Management Journal",
        "abbr": "SMJ",
        "issn": ["0143-2095", "1097-0266"],
        "category": "Strategy",
        "in_ft50": True,
        "in_utd24": True,
        "innovation_relevance": "high",
        "tags": ["strategy", "innovation", "entrepreneurship", "competitive-advantage"],
    },
    {
        "name": "Organization Science",
        "abbr": "OrgSci",
        "issn": ["1047-7039", "1526-5455"],
        "category": "Organization",
        "in_ft50": True,
        "in_utd24": True,
        "innovation_relevance": "high",
        "tags": ["organization", "innovation", "management"],
    },
    {
        "name": "Management Science",
        "abbr": "MS",
        "issn": ["0025-1909", "1526-5501"],
        "category": "Management Science",
        "in_ft50": True,
        "in_utd24": True,
        "innovation_relevance": "medium",
        "tags": ["management", "decision-science", "operations"],
    },
    {
        "name": "Journal of International Business Studies",
        "abbr": "JIBS",
        "issn": ["0047-2506", "1478-6990"],
        "category": "International Business",
        "in_ft50": True,
        "in_utd24": True,
        "innovation_relevance": "medium",
        "tags": ["international-business", "strategy", "entrepreneurship"],
    },
    {
        "name": "Journal of Management",
        "abbr": "JOM",
        "issn": ["0149-2063", "1557-1211"],
        "category": "Management",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "high",
        "tags": ["management", "innovation", "entrepreneurship", "organization"],
    },
    {
        "name": "Journal of Management Studies",
        "abbr": "JMS",
        "issn": ["0022-2380", "1467-6486"],
        "category": "Management",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "high",
        "tags": ["management", "innovation", "organization"],
    },
    {
        "name": "Organization Studies",
        "abbr": "OS",
        "issn": ["0170-8406", "1741-3044"],
        "category": "Organization",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "medium",
        "tags": ["organization", "management"],
    },

    # ============================================================
    # OB & Human Resources (FT50)
    # ============================================================
    {
        "name": "Human Relations",
        "abbr": "HR",
        "issn": ["0018-7267", "1741-282X"],
        "category": "OB & HR",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "low",
        "tags": ["ob", "hr"],
    },
    {
        "name": "Human Resource Management",
        "abbr": "HRM",
        "issn": ["0090-4848", "1099-050X"],
        "category": "OB & HR",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "low",
        "tags": ["hr", "management"],
    },
    {
        "name": "Journal of Applied Psychology",
        "abbr": "JAP",
        "issn": ["0021-9010", "1939-1854"],
        "category": "OB & HR",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "low",
        "tags": ["ob", "psychology"],
    },
    {
        "name": "Organizational Behavior and Human Decision Processes",
        "abbr": "OBHDP",
        "issn": ["0749-5978"],
        "category": "OB & HR",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "low",
        "tags": ["ob", "decision-making"],
    },

    # ============================================================
    # Marketing (FT50 + UTD24)
    # ============================================================
    {
        "name": "Journal of Consumer Research",
        "abbr": "JCR",
        "issn": ["0093-5301", "1537-5277"],
        "category": "Marketing",
        "in_ft50": True,
        "in_utd24": True,
        "innovation_relevance": "low",
        "tags": ["marketing", "consumer-behavior"],
    },
    {
        "name": "Journal of Marketing",
        "abbr": "JM",
        "issn": ["0022-2429", "1547-7185"],
        "category": "Marketing",
        "in_ft50": True,
        "in_utd24": True,
        "innovation_relevance": "medium",
        "tags": ["marketing", "innovation"],
    },
    {
        "name": "Journal of Marketing Research",
        "abbr": "JMR",
        "issn": ["0022-2437", "1547-7193"],
        "category": "Marketing",
        "in_ft50": True,
        "in_utd24": True,
        "innovation_relevance": "low",
        "tags": ["marketing"],
    },
    {
        "name": "Marketing Science",
        "abbr": "MktSci",
        "issn": ["0732-2399", "1526-548X"],
        "category": "Marketing",
        "in_ft50": True,
        "in_utd24": True,
        "innovation_relevance": "low",
        "tags": ["marketing"],
    },
    {
        "name": "Journal of Consumer Psychology",
        "abbr": "JCP",
        "issn": ["1057-7408", "1532-7663"],
        "category": "Marketing",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "low",
        "tags": ["marketing", "consumer-behavior", "psychology"],
    },
    {
        "name": "Journal of the Academy of Marketing Science",
        "abbr": "JAMS",
        "issn": ["0092-0703", "1552-7824"],
        "category": "Marketing",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "low",
        "tags": ["marketing"],
    },

    # ============================================================
    # Accounting (FT50 + UTD24)
    # ============================================================
    {
        "name": "The Accounting Review",
        "abbr": "TAR",
        "issn": ["0001-4826", "1558-7967"],
        "category": "Accounting",
        "in_ft50": True,
        "in_utd24": True,
        "innovation_relevance": "low",
        "tags": ["accounting"],
    },
    {
        "name": "Journal of Accounting and Economics",
        "abbr": "JAE",
        "issn": ["0165-4101"],
        "category": "Accounting",
        "in_ft50": True,
        "in_utd24": True,
        "innovation_relevance": "low",
        "tags": ["accounting", "economics"],
    },
    {
        "name": "Journal of Accounting Research",
        "abbr": "JAR",
        "issn": ["0021-8456", "1475-679X"],
        "category": "Accounting",
        "in_ft50": True,
        "in_utd24": True,
        "innovation_relevance": "low",
        "tags": ["accounting"],
    },
    {
        "name": "Accounting, Organizations and Society",
        "abbr": "AOS",
        "issn": ["0361-3682"],
        "category": "Accounting",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "low",
        "tags": ["accounting", "organization"],
    },
    {
        "name": "Contemporary Accounting Research",
        "abbr": "CAR",
        "issn": ["0823-9150", "1911-3846"],
        "category": "Accounting",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "low",
        "tags": ["accounting"],
    },
    {
        "name": "Review of Accounting Studies",
        "abbr": "RAST",
        "issn": ["1380-6653", "1573-7136"],
        "category": "Accounting",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "low",
        "tags": ["accounting"],
    },

    # ============================================================
    # Finance (FT50 + UTD24)
    # ============================================================
    {
        "name": "Journal of Finance",
        "abbr": "JF",
        "issn": ["0022-1082", "1540-6261"],
        "category": "Finance",
        "in_ft50": True,
        "in_utd24": True,
        "innovation_relevance": "low",
        "tags": ["finance"],
    },
    {
        "name": "Journal of Financial Economics",
        "abbr": "JFE",
        "issn": ["0304-405X"],
        "category": "Finance",
        "in_ft50": True,
        "in_utd24": True,
        "innovation_relevance": "low",
        "tags": ["finance"],
    },
    {
        "name": "Review of Financial Studies",
        "abbr": "RFS",
        "issn": ["0893-9454", "1465-7368"],
        "category": "Finance",
        "in_ft50": True,
        "in_utd24": True,
        "innovation_relevance": "low",
        "tags": ["finance"],
    },
    {
        "name": "Journal of Financial and Quantitative Analysis",
        "abbr": "JFQA",
        "issn": ["0022-1090", "1756-6916"],
        "category": "Finance",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "low",
        "tags": ["finance"],
    },
    {
        "name": "Review of Finance",
        "abbr": "RoF",
        "issn": ["1572-3097", "1573-692X"],
        "category": "Finance",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "low",
        "tags": ["finance"],
    },

    # ============================================================
    # Economics (FT50)
    # ============================================================
    {
        "name": "American Economic Review",
        "abbr": "AER",
        "issn": ["0002-8282", "1944-7981"],
        "category": "Economics",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "medium",
        "tags": ["economics", "innovation"],
    },
    {
        "name": "Econometrica",
        "abbr": "ECMA",
        "issn": ["0012-9682", "1468-0262"],
        "category": "Economics",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "low",
        "tags": ["economics", "econometrics"],
    },
    {
        "name": "Journal of Political Economy",
        "abbr": "JPE",
        "issn": ["0022-3808", "1537-534X"],
        "category": "Economics",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "low",
        "tags": ["economics"],
    },
    {
        "name": "Quarterly Journal of Economics",
        "abbr": "QJE",
        "issn": ["0033-5533", "1531-4650"],
        "category": "Economics",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "low",
        "tags": ["economics"],
    },
    {
        "name": "Review of Economic Studies",
        "abbr": "ReStud",
        "issn": ["0034-6527", "1467-937X"],
        "category": "Economics",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "low",
        "tags": ["economics"],
    },

    # ============================================================
    # Information Systems (FT50 + UTD24)
    # ============================================================
    {
        "name": "Information Systems Research",
        "abbr": "ISR",
        "issn": ["1047-7047", "1526-5536"],
        "category": "Information Systems",
        "in_ft50": True,
        "in_utd24": True,
        "innovation_relevance": "medium",
        "tags": ["information-systems", "innovation", "technology"],
    },
    {
        "name": "MIS Quarterly",
        "abbr": "MISQ",
        "issn": ["0276-7783", "2162-9730"],
        "category": "Information Systems",
        "in_ft50": True,
        "in_utd24": True,
        "innovation_relevance": "medium",
        "tags": ["information-systems", "innovation", "technology"],
    },
    {
        "name": "Journal of Management Information Systems",
        "abbr": "JMIS",
        "issn": ["0742-1222", "1557-928X"],
        "category": "Information Systems",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "medium",
        "tags": ["information-systems", "technology"],
    },
    {
        "name": "INFORMS Journal on Computing",
        "abbr": "IJOC",
        "issn": ["1091-9856", "1526-5528"],
        "category": "Information Systems",
        "in_ft50": False,
        "in_utd24": True,
        "innovation_relevance": "low",
        "tags": ["information-systems", "computing"],
    },

    # ============================================================
    # Operations Management & OR (FT50 + UTD24)
    # ============================================================
    {
        "name": "Operations Research",
        "abbr": "OR",
        "issn": ["0030-364X", "1526-5463"],
        "category": "Operations Research",
        "in_ft50": True,
        "in_utd24": True,
        "innovation_relevance": "low",
        "tags": ["operations-research"],
    },
    {
        "name": "Journal of Operations Management",
        "abbr": "JOM-Ops",
        "issn": ["0272-6963", "1873-1317"],
        "category": "Operations Management",
        "in_ft50": True,
        "in_utd24": True,
        "innovation_relevance": "medium",
        "tags": ["operations-management", "innovation"],
    },
    {
        "name": "Manufacturing and Service Operations Management",
        "abbr": "MSOM",
        "issn": ["1523-4614", "1526-5498"],
        "category": "Operations Management",
        "in_ft50": True,
        "in_utd24": True,
        "innovation_relevance": "low",
        "tags": ["operations-management"],
    },
    {
        "name": "Production and Operations Management",
        "abbr": "POM",
        "issn": ["1059-1478", "1937-5956"],
        "category": "Operations Management",
        "in_ft50": True,
        "in_utd24": True,
        "innovation_relevance": "low",
        "tags": ["operations-management"],
    },

    # ============================================================
    # Ethics (FT50)
    # ============================================================
    {
        "name": "Journal of Business Ethics",
        "abbr": "JBE",
        "issn": ["0167-4544", "1573-0697"],
        "category": "Ethics",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "medium",
        "tags": ["ethics", "social-entrepreneurship"],
    },

    # ============================================================
    # Practitioner (FT50)
    # ============================================================
    {
        "name": "Harvard Business Review",
        "abbr": "HBR",
        "issn": ["0017-8012"],
        "category": "Practitioner",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "high",
        "tags": ["practitioner", "innovation", "entrepreneurship", "strategy"],
    },
    {
        "name": "MIT Sloan Management Review",
        "abbr": "SMR",
        "issn": ["1532-9194"],
        "category": "Practitioner",
        "in_ft50": True,
        "in_utd24": False,
        "innovation_relevance": "high",
        "tags": ["practitioner", "innovation", "technology", "strategy"],
    },
]


# ── Tag constants for --mode innovation ──────────────────────────────
INNOVATION_TAGS = {"innovation", "entrepreneurship", "new-ventures", "venture-capital",
                   "technology-policy", "r-and-d", "social-entrepreneurship"}


def get_journals(list_name=None, relevance=None, tags=None):
    """Filter journals by list membership, innovation relevance, and/or tags.

    Args:
        list_name: "ft50", "utd24", or None for all.
        relevance: "high", "medium", "low", or None for all.
        tags: Iterable of tags. A journal matches if it has ANY of these tags.

    Returns:
        List of matching journal dicts.
    """
    results = JOURNALS
    if list_name == "ft50":
        results = [j for j in results if j["in_ft50"]]
    elif list_name == "utd24":
        results = [j for j in results if j["in_utd24"]]
    if relevance:
        results = [j for j in results if j["innovation_relevance"] == relevance]
    if tags:
        tag_set = set(tags)
        results = [j for j in results if tag_set & set(j.get("tags", []))]
    return results


def get_all_issns(journals=None):
    """Extract all ISSNs from a journal list."""
    if journals is None:
        journals = JOURNALS
    issns = []
    for j in journals:
        issns.extend(j["issn"])
    return issns


def get_journal_by_issn(issn):
    """Look up a journal by any of its ISSNs."""
    for j in JOURNALS:
        if issn in j["issn"]:
            return j
    return None
