import html as html_lib

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="AP Election Explorer",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# HTML
# ============================================================

def render_html(content: str):
    cleaned = " ".join(
        line.strip()
        for line in content.splitlines()
        if line.strip()
    )

    st.markdown(
        cleaned,
        unsafe_allow_html=True,
    )


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 70% -20%,
                rgba(34, 50, 68, 0.13),
                transparent 38%
            ),
            #080c10;

        color: #f5f7fa;
    }

    html,
    body,
    [class*="css"] {
        font-family:
            Inter,
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;
    }

    .block-container {
        max-width: 1800px;
        padding-top: 2.1rem;
        padding-left: 2rem;
        padding-right: 2rem;
        padding-bottom: 3rem;
    }


    /* SIDEBAR */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #11171e 0%,
                #0b1016 100%
            );

        border-right: 1px solid #222b35;
        min-width: 350px;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    section[data-testid="stSidebar"] label {
        color: #f3f5f7 !important;
        font-weight: 650;
    }

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] > div {
        background: #171e27 !important;
        color: white !important;
        border: 1px solid #303946 !important;
        border-radius: 7px !important;
        min-height: 45px;
    }

    section[data-testid="stSidebar"]
    div[data-baseweb="select"] span {
        color: white !important;
    }


    /* DROPDOWN MENUS */

    div[data-baseweb="popover"] {
        background: #111820 !important;
    }

    div[data-baseweb="popover"] > div {
        background: #111820 !important;
    }

    div[role="listbox"] {
        background: #111820 !important;
        border: 1px solid #303946 !important;
        border-radius: 8px !important;

        max-height: 300px !important;
        overflow-y: auto !important;

        font-size: .84rem !important;
    }

    div[role="option"] {
        background: #111820 !important;
        color: #e8edf3 !important;

        font-size: .84rem !important;

        padding-top: 7px !important;
        padding-bottom: 7px !important;
    }

    div[role="option"]:hover {
        background: #202a35 !important;
    }

    div[role="option"][aria-selected="true"] {
        background: #263240 !important;
        color: white !important;
    }


    /* BRAND */

    .brand {
        display: flex;
        align-items: center;
        gap: 13px;
        margin-bottom: 29px;
    }

    .ap-logo {
        width: 48px;
        height: 52px;

        display: flex;
        align-items: center;
        justify-content: center;

        background: white;
        color: #080808;

        font-size: 25px;
        font-weight: 900;
        letter-spacing: -2px;

        border-bottom: 5px solid #ed1c24;

        box-sizing: border-box;
    }

    .brand-title {
        color: white;
        font-size: 1.35rem;
        font-weight: 800;
        line-height: 1.15;
    }

    .brand-sub {
        color: #8d97a4;
        font-size: .72rem;
        letter-spacing: .06em;
        text-transform: uppercase;
        margin-top: 4px;
    }


    /* BUTTON */

    div.stButton > button {
        width: 100%;
        min-height: 46px;

        background:
            linear-gradient(
                180deg,
                #258cff,
                #0878ef
            );

        border: 1px solid #2c93ff;
        border-radius: 7px;

        color: white;
        font-weight: 700;
    }

    div.stButton > button:hover {
        background: #2792ff;
        border-color: #64b1ff;
        color: white;
    }


    /* HEADER */

    .hero-title {
        margin: 0;
        color: white;

        font-size: 3.25rem;
        line-height: 1.02;

        font-weight: 850;

        letter-spacing: -.045em;
    }

    .hero-subtitle {
        color: #aeb6c2;

        font-size: 1.5rem;
        font-weight: 650;

        margin-top: .55rem;
    }

    .updated {
        text-align: right;
        color: #9aa4af;
        font-size: .86rem;
        padding-top: .8rem;
    }


    /* METRIC CARDS */

    .metric-card {
        height: 126px;

        background:
            linear-gradient(
                145deg,
                #121920,
                #0c1117
            );

        border: 1px solid #26303a;
        border-radius: 10px;

        padding: 20px 21px;

        box-sizing: border-box;
    }

    .metric-label {
        color: #aeb7c3;
        font-size: .83rem;
        font-weight: 650;

        margin-bottom: 7px;

        white-space: nowrap;
    }

    .metric-value {
        color: white;

        font-size: 1.8rem;
        font-weight: 850;

        letter-spacing: -.03em;
        line-height: 1.2;
    }

    .metric-value-blue {
        color: #2a9cff;

        font-size: 1.8rem;
        font-weight: 850;

        letter-spacing: -.03em;
        line-height: 1.2;
    }

    .track {
        width: 100%;
        height: 11px;

        margin-top: 13px;

        background: #29333f;

        border-radius: 100px;

        overflow: hidden;
    }

    .track-blue {
        height: 100%;
        background: #2a9cff;
        border-radius: 100px;
    }

    .track-green {
        height: 100%;
        background: #55d16b;
        border-radius: 100px;
    }


    /* PANELS */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background:
            linear-gradient(
                145deg,
                #10161d,
                #090e13
            );

        border: 1px solid #242d37 !important;
        border-radius: 11px;
    }

    .panel-title {
        color: white;
        font-size: 1.25rem;
        font-weight: 800;
        margin-bottom: 2px;
    }

    .panel-subtitle {
        color: #aab3bf;
        font-size: .9rem;
        margin-bottom: 10px;
    }


    /* RESULTS TABLE */

    .results-table-wrap {
        width: 100%;
        max-height: 610px;

        overflow-y: auto;
        overflow-x: auto;

        border: 1px solid #242d37;
        border-radius: 8px;

        background: #0b1015;
    }

    table.results-table {
        width: 100%;
        border-collapse: collapse;

        font-size: .85rem;
        color: #e8edf3;
    }

    table.results-table thead {
        position: sticky;
        top: 0;
        z-index: 2;
    }

    table.results-table thead th {
        background: #121920;
        color: #b7c0cb;

        font-weight: 700;
        text-align: left;

        padding: 12px;

        border-bottom: 1px solid #2a3440;

        white-space: nowrap;
    }

    table.results-table tbody td {
        padding: 11px 12px;

        border-bottom: 1px solid #1d252e;

        white-space: nowrap;
    }

    table.results-table tbody tr:hover {
        background: #111820;
    }

    .eevp-bar {
        width: 64px;
        height: 8px;

        background: #27313c;

        border-radius: 100px;

        overflow: hidden;
    }

    .eevp-fill {
        height: 100%;

        background: #2a9cff;

        border-radius: 100px;
    }


    /* DETAIL CARDS */

    .detail-grid {
        display: grid;

        grid-template-columns:
            repeat(4, minmax(0, 1fr));

        gap: 14px;

        margin-top: 14px;
    }

    .detail-card {
        background: #0f151b;

        border: 1px solid #242d37;
        border-radius: 9px;

        padding: 16px 18px;
    }

    .detail-label {
        color: #8f99a5;

        font-size: .78rem;
        font-weight: 650;

        text-transform: uppercase;

        letter-spacing: .04em;
    }

    .detail-value {
        color: white;

        font-size: 1.2rem;
        font-weight: 750;

        margin-top: 5px;

        overflow-wrap: anywhere;
    }


    /* CANDIDATES */

    .candidate-section-title {
        color: white;

        font-size: 1.2rem;
        font-weight: 800;

        margin-top: 24px;
        margin-bottom: 10px;
    }

    .candidate-table {
        width: 100%;
        border-collapse: collapse;

        margin-top: 8px;

        font-size: .88rem;
    }

    .candidate-table th {
        text-align: left;

        color: #aeb7c3;
        background: #121920;

        padding: 10px;

        border-bottom: 1px solid #27313c;
    }

    .candidate-table td {
        color: #e8edf3;

        padding: 10px;

        border-bottom: 1px solid #1d252e;
    }


    /* INPUTS */

    div[data-testid="stTextInput"] input {
        background: #171e27 !important;
        color: white !important;
        border: 1px solid #303946 !important;
    }

    div[data-testid="stSelectbox"]
    div[data-baseweb="select"] > div {
        background: #171e27 !important;
        color: white !important;
        border: 1px solid #303946 !important;
    }

    div[data-testid="stSelectbox"] span {
        color: white !important;
    }


    /* EXPANDERS */

    div[data-testid="stExpander"] {
        background: #0b1015 !important;
        border: 1px solid #242d37 !important;
    }

    div[data-testid="stExpander"] summary {
        background: #0b1015 !important;
        color: #cfd6de !important;
    }


    .side-divider {
        height: 1px;
        background: #333d48;
        margin: 22px 0;
    }

    #MainMenu,
    footer {
        visibility: hidden;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SETTINGS
# ============================================================

ELECTION_DATE = "2026-11-03"
STATE_POSTAL = "GA"

OFFICE_MAP = {
    "Governor": "G",
    "U.S. Senate": "S",
    "U.S. House": "H",
}


# ============================================================
# GENERIC FIELD ACCESS
# ============================================================

def field(obj, *names, default=None):
    if not isinstance(obj, dict):
        return default

    for name in names:
        if name in obj:
            return obj[name]

    lower_map = {
        str(key).lower(): value
        for key, value in obj.items()
    }

    for name in names:
        if name.lower() in lower_map:
            return lower_map[name.lower()]

    return default


# ============================================================
# ELAPI
# ============================================================

@st.cache_data(
    ttl=30,
    show_spinner=False,
)
def fetch_elapi(
    election_date,
    state_postal,
    race_ids=None,
    reporting_unit_ids=None,
    level="ru",
):
    api_key = st.secrets["ELAPI_KEY"]

    url = (
        f"https://api.ap.org/v3/elections/"
        f"{election_date}"
    )

    params = {
        "resultstype": "l",
        "statepostal": state_postal,
        "level": level,
        "format": "json",
    }

    if race_ids:
        params["raceid"] = ",".join(
            str(value)
            for value in race_ids
        )

    if reporting_unit_ids:
        params["reportingunitid"] = ",".join(
            str(value)
            for value in reporting_unit_ids
        )

    headers = {
        "x-api-key": api_key,
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=30,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"ELAPI request failed: "
            f"{response.status_code}\n\n"
            f"{response.text[:1500]}"
        )

    return response.json()


# ============================================================
# GEOJSON
# ============================================================

@st.cache_data(
    ttl=86400,
    show_spinner=False,
)
def get_georgia_geojson():
    url = (
        "https://raw.githubusercontent.com/"
        "plotly/datasets/master/"
        "geojson-counties-fips.json"
    )

    response = requests.get(
        url,
        timeout=30,
    )

    response.raise_for_status()

    raw = response.json()

    return {
        "type": "FeatureCollection",
        "features": [
            feature
            for feature in raw["features"]
            if str(feature["id"]).startswith("13")
        ],
    }


# ============================================================
# RACE HELPERS
# ============================================================

def get_races(data):
    return (
        field(
            data,
            "races",
            "Races",
            default=[],
        )
        or []
    )


def race_id_value(race):
    return field(
        race,
        "raceID",
        "RaceID",
        "id",
        "ID",
    )


def race_display_name(race):
    office = field(
        race,
        "officeName",
        "OfficeName",
        default="Race",
    )

    seat = field(
        race,
        "seatName",
        "SeatName",
    )

    if seat:
        return f"{office} — {seat}"

    return office


def short_race_label(race):
    office = field(
        race,
        "officeName",
        "OfficeName",
        default="Race",
    )

    seat = field(
        race,
        "seatName",
        "SeatName",
        default="",
    )

    office_short = {
        "Lieutenant Governor":
            "Lt. Governor",

        "Agriculture Commissioner":
            "Agriculture Comm.",

        "Insurance Commissioner":
            "Insurance Comm.",

        "Secretary of State":
            "Secretary of State",

        "Attorney General":
            "Attorney General",

        "School Superintendent":
            "School Superintendent",

        "U.S. House":
            "U.S. House",

        "U.S. Senate":
            "U.S. Senate",

        "State Senate":
            "State Senate",

        "State House":
            "State House",

        "Governor":
            "Governor",
    }.get(
        office,
        office,
    )

    if seat:
        seat_text = str(seat)

        seat_text = seat_text.replace(
            "District ",
            "D",
        )

        return (
            f"{office_short} "
            f"{seat_text}"
        )

    return office_short


def office_id(race):
    return str(
        field(
            race,
            "officeID",
            "OfficeID",
            default="",
        )
    ).upper()


# ============================================================
# REPORTING UNIT HELPERS
# ============================================================

def reporting_units(race):
    return (
        field(
            race,
            "reportingUnits",
            "ReportingUnits",
            default=[],
        )
        or []
    )


def reporting_unit_level(ru):
    raw = field(
        ru,
        "reportingUnitLevel",
        "reportingunitLevel",
        "ReportingUnitLevel",
    )

    try:
        return int(raw)

    except (
        TypeError,
        ValueError,
    ):
        return None


def reporting_unit_id(ru):
    return field(
        ru,
        "reportingUnitID",
        "reportingunitID",
        "ReportingUnitID",
        "id",
        "ID",
    )


def reporting_unit_name(ru):
    return field(
        ru,
        "reportingUnitName",
        "reportingunitName",
        "ReportingUnitName",
        "name",
        "Name",
        default="Unknown",
    )


def get_state_reporting_unit(race):
    for ru in reporting_units(race):
        if reporting_unit_level(ru) == 1:
            return ru

        level_name = str(
            field(
                ru,
                "level",
                "Level",
                default="",
            )
        ).lower()

        if level_name == "state":
            return ru

    return None


def get_level_2_reporting_units(race):
    return [
        ru
        for ru in reporting_units(race)
        if reporting_unit_level(ru) == 2
    ]


# ============================================================
# CANDIDATES
# ============================================================

def candidate_list(ru):
    return (
        field(
            ru,
            "candidates",
            "Candidates",
            default=[],
        )
        or []
    )


def vote_count(candidate):
    raw = field(
        candidate,
        "voteCount",
        "VoteCount",
        default=0,
    )

    try:
        return int(raw or 0)

    except (
        TypeError,
        ValueError,
    ):
        return 0


def party(candidate):
    return str(
        field(
            candidate,
            "party",
            "Party",
            default="",
        )
        or ""
    )


# ============================================================
# EXPECTED DATA
# ============================================================

def get_expected_data(obj):
    if not obj:
        return {
            "registered": None,
            "expected_actual": None,
            "eevp_cap": None,
            "parameters": {},
        }

    parameters = (
        field(
            obj,
            "parameters",
            "Parameters",
            default={},
        )
        or {}
    )

    vote_info = (
        field(
            parameters,
            "vote",
            "Vote",
            default={},
        )
        or {}
    )

    expected_info = (
        field(
            vote_info,
            "expected",
            "Expected",
            default={},
        )
        or {}
    )

    return {
        "registered":
            field(
                vote_info,
                "registered",
                "Registered",
            ),

        "expected_actual":
            field(
                expected_info,
                "actual",
                "Actual",
            ),

        "eevp_cap":
            field(
                expected_info,
                "eevpCap",
                "EEVPCap",
            ),

        "parameters":
            parameters,
    }


# ============================================================
# COUNTY DATA
# ============================================================

def build_county_dataframe(race):
    rows = []

    for ru in get_level_2_reporting_units(race):
        fips = field(
            ru,
            "fipsCode",
            "FIPSCode",
        )

        if not fips:
            continue

        candidates = candidate_list(ru)

        total_votes = sum(
            vote_count(candidate)
            for candidate in candidates
        )

        dem_votes = sum(
            vote_count(candidate)
            for candidate in candidates
            if party(candidate).lower()
            in {
                "dem",
                "democrat",
                "democratic",
            }
        )

        gop_votes = sum(
            vote_count(candidate)
            for candidate in candidates
            if party(candidate).lower()
            in {
                "gop",
                "rep",
                "republican",
            }
        )

        if total_votes:
            dem_pct = (
                dem_votes
                / total_votes
                * 100
            )

            gop_pct = (
                gop_votes
                / total_votes
                * 100
            )

            margin_numeric = (
                dem_pct
                - gop_pct
            )

            if margin_numeric >= 0:
                margin = (
                    f"D +"
                    f"{abs(margin_numeric):.1f}"
                )

            else:
                margin = (
                    f"R +"
                    f"{abs(margin_numeric):.1f}"
                )

        else:
            dem_pct = None
            gop_pct = None
            margin_numeric = None
            margin = "—"

        try:
            eevp = float(
                field(
                    ru,
                    "eevp",
                    "EEVP",
                    default=0,
                )
                or 0
            )

        except (
            TypeError,
            ValueError,
        ):
            eevp = 0


        expected_data = (
            get_expected_data(ru)
        )

        parameters = (
            expected_data[
                "parameters"
            ]
        )

        precincts = (
            field(
                ru,
                "precincts",
                "Precincts",
                default={},
            )
            or {}
        )

        geo_stratum = (
            field(
                parameters,
                "geoStratum",
                "GeoStratum",
                default={},
            )
            or {}
        )

        pol_stratum = (
            field(
                parameters,
                "polStratum",
                "PolStratum",
                default={},
            )
            or {}
        )

        candidate_details = []

        for candidate in candidates:
            first = field(
                candidate,
                "first",
                "First",
                default="",
            )

            last = field(
                candidate,
                "last",
                "Last",
                default="",
            )

            nickname = field(
                candidate,
                "nickname",
                "Nickname",
                default="",
            )

            full_name = " ".join(
                part
                for part in [
                    first,

                    (
                        f'"{nickname}"'
                        if nickname
                        else ""
                    ),

                    last,
                ]
                if part
            )

            candidate_details.append(
                {
                    "Candidate ID":
                        field(
                            candidate,
                            "candidateID",
                            "CandidateID",
                            "id",
                            "ID",
                        ),

                    "Name":
                        full_name,

                    "Party":
                        party(candidate),

                    "Votes":
                        vote_count(
                            candidate
                        ),

                    "Ballot Order":
                        field(
                            candidate,
                            "ballotOrder",
                            "BallotOrder",
                        ),

                    "Pol ID":
                        field(
                            candidate,
                            "polID",
                            "PolID",
                        ),
                }
            )

        rows.append(
            {
                "County":
                    reporting_unit_name(
                        ru
                    ),

                "Reporting Unit ID":
                    str(
                        reporting_unit_id(
                            ru
                        )
                    ),

                "FIPS":
                    str(fips).zfill(5),

                "Dem %":
                    dem_pct,

                "GOP %":
                    gop_pct,

                "Margin":
                    margin,

                "Margin Numeric":
                    margin_numeric,

                "Total Votes":
                    total_votes,

                "Registered":
                    expected_data[
                        "registered"
                    ],

                "Expected Vote":
                    expected_data[
                        "expected_actual"
                    ],

                "EEVP":
                    eevp,

                "EEVP Cap":
                    expected_data[
                        "eevp_cap"
                    ],

                "Precincts Reporting":
                    field(
                        precincts,
                        "reporting",
                        "Reporting",
                        default=0,
                    ),

                "Precincts Total":
                    field(
                        precincts,
                        "total",
                        "Total",
                        default=0,
                    ),

                "Precincts %":
                    field(
                        precincts,
                        "reportingPct",
                        "ReportingPct",
                    ),

                "GeoStratum":
                    field(
                        geo_stratum,
                        "name",
                        "Name",
                        default="—",
                    ),

                "PolStratum":
                    field(
                        pol_stratum,
                        "name",
                        "Name",
                        default="—",
                    ),

                "Poll Closing Time":
                    field(
                        ru,
                        "pollClosingTime",
                        "PollClosingTime",
                    ),

                "Tab Status Number":
                    field(
                        ru,
                        "tabStatusNumber",
                        "TabStatusNumber",
                    ),

                "Last Updated":
                    field(
                        ru,
                        "lastUpdated",
                        "LastUpdated",
                    ),

                "Candidates":
                    candidate_details,
            }
        )

    return pd.DataFrame(
        rows
    )


# ============================================================
# FORMATTERS
# ============================================================

def fmt_int(value):
    if value is None:
        return "—"

    try:
        if pd.isna(value):
            return "—"

    except Exception:
        pass

    try:
        return f"{int(float(value)):,}"

    except Exception:
        return str(value)


def fmt_pct(
    value,
    decimals=1,
):
    if value is None:
        return "—"

    try:
        if pd.isna(value):
            return "—"

    except Exception:
        pass

    try:
        return (
            f"{float(value):.{decimals}f}%"
        )

    except Exception:
        return str(value)


def format_timestamp(value):
    if not value:
        return "—"

    try:
        parsed = pd.to_datetime(
            value,
            utc=True,
        )

        return (
            parsed
            .tz_convert(
                "US/Eastern"
            )
            .strftime(
                "%b %-d, "
                "%-I:%M:%S %p ET"
            )
        )

    except Exception:
        return str(value)


def format_poll_close(value):
    if not value:
        return "—"

    try:
        parsed = pd.to_datetime(
            value,
            utc=True,
        )

        return (
            parsed
            .tz_convert(
                "US/Eastern"
            )
            .strftime(
                "%b %-d, %-I:%M %p ET"
            )
        )

    except Exception:
        return str(value)


def state_total_votes(state_ru):
    if not state_ru:
        return 0

    return sum(
        vote_count(candidate)
        for candidate
        in candidate_list(
            state_ru
        )
    )


# ============================================================
# RESULTS TABLE
# ============================================================

def build_results_table(df):
    rows = []

    for _, row in df.iterrows():
        eevp = float(
            row["EEVP"]
            or 0
        )

        rows.append(
            f"""
            <tr>

                <td>
                    {html_lib.escape(str(row["County"]))}
                </td>

                <td>
                    {html_lib.escape(str(row["Reporting Unit ID"]))}
                </td>

                <td>
                    {fmt_pct(row["Dem %"])}
                </td>

                <td>
                    {fmt_pct(row["GOP %"])}
                </td>

                <td>
                    {html_lib.escape(str(row["Margin"]))}
                </td>

                <td>
                    {fmt_int(row["Total Votes"])}
                </td>

                <td>
                    {fmt_int(row["Expected Vote"])}
                </td>

                <td>

                    <div
                        style="
                            display:flex;
                            align-items:center;
                            gap:7px;
                        "
                    >

                        <span>
                            {eevp:.0f}%
                        </span>

                        <div class="eevp-bar">

                            <div
                                class="eevp-fill"
                                style="
                                    width:
                                    {min(eevp,100)}%;
                                "
                            ></div>

                        </div>

                    </div>

                </td>

            </tr>
            """
        )

    return f"""
    <div class="results-table-wrap">

        <table class="results-table">

            <thead>

                <tr>
                    <th>County</th>
                    <th>RU ID</th>
                    <th>Dem %</th>
                    <th>GOP %</th>
                    <th>Margin</th>
                    <th>Votes</th>
                    <th>Expected</th>
                    <th>EEVP</th>
                </tr>

            </thead>

            <tbody>
                {''.join(rows)}
            </tbody>

        </table>

    </div>
    """


# ============================================================
# COUNTY LABEL CENTERS
# ============================================================

def feature_centroid(feature):
    geometry = feature.get(
        "geometry",
        {},
    )

    geometry_type = (
        geometry.get("type")
    )

    coordinates = (
        geometry.get(
            "coordinates",
            [],
        )
    )

    points = []


    if geometry_type == "Polygon":

        for ring in coordinates:
            points.extend(ring)


    elif (
        geometry_type
        == "MultiPolygon"
    ):

        for polygon in coordinates:
            for ring in polygon:
                points.extend(ring)


    if not points:
        return None, None


    longitude = sum(
        point[0]
        for point in points
    ) / len(points)

    latitude = sum(
        point[1]
        for point in points
    ) / len(points)


    return (
        longitude,
        latitude,
    )


# ============================================================
# BASE FEED
#
# This is always unfiltered and is used to populate controls.
# ============================================================

try:
    base_data = fetch_elapi(
        election_date=
            ELECTION_DATE,

        state_postal=
            STATE_POSTAL,

        level=
            "ru",
    )

except Exception as exc:
    st.error(
        "Could not load ELAPI."
    )

    st.code(
        str(exc)
    )

    st.stop()


base_races = get_races(
    base_data
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    render_html(
        """
        <div class="brand">

            <div class="ap-logo">
                AP
            </div>

            <div>

                <div class="brand-title">
                    Election Explorer
                </div>

                <div class="brand-sub">
                    AP Elections API (ELAPI)
                </div>

            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # ELECTION
    # --------------------------------------------------------

    st.markdown(
        "**Election**"
    )

    st.selectbox(
        "Election",
        [
            "2026 General "
            "(Nov. 3, 2026)"
        ],
        label_visibility=
            "collapsed",
    )


    # --------------------------------------------------------
    # STATE
    # --------------------------------------------------------

    st.markdown(
        "**State**"
    )

    st.selectbox(
        "State",
        [
            "Georgia (GA)"
        ],
        label_visibility=
            "collapsed",
    )


    # --------------------------------------------------------
    # OFFICE
    # --------------------------------------------------------

    st.markdown(
        "**Race**"
    )

    office_choice = st.selectbox(
        "Race",
        [
            "Governor",
            "U.S. Senate",
            "U.S. House",
        ],
        label_visibility=
            "collapsed",
    )


    # --------------------------------------------------------
    # FIND RACES THAT MATCH MAIN SELECTOR
    # --------------------------------------------------------

    desired_office = (
        OFFICE_MAP[
            office_choice
        ]
    )

    main_matching_races = [
        race
        for race in base_races
        if (
            office_id(race)
            == desired_office
        )
    ]


    # --------------------------------------------------------
    # IF HOUSE / MULTIPLE RACES, CHOOSE SPECIFIC ONE
    # --------------------------------------------------------

    main_selected_race = None


    if len(
        main_matching_races
    ) == 1:

        main_selected_race = (
            main_matching_races[0]
        )


    elif len(
        main_matching_races
    ) > 1:

        main_race_options = {
            short_race_label(race):
                race

            for race
            in main_matching_races
        }


        main_race_label = (
            st.selectbox(
                "Specific race",

                list(
                    main_race_options.keys()
                ),
            )
        )


        main_selected_race = (
            main_race_options[
                main_race_label
            ]
        )


    # --------------------------------------------------------
    # LEVEL
    # --------------------------------------------------------

    st.markdown(
        "**Level**"
    )

    level_choice = (
        st.selectbox(
            "Level",
            [
                "Reporting units (RU)",
                "State",
            ],
            label_visibility=
                "collapsed",
        )
    )


    # ========================================================
    # ADVANCED FILTERS
    #
    # IMPORTANT:
    # Default = follow the main selector.
    # It no longer silently chooses a different race.
    # ========================================================

    with st.expander(
        "Advanced Filters"
    ):

        race_dropdown_options = {
            "Follow race selector":
                None
        }


        for race in base_races:

            rid = (
                race_id_value(
                    race
                )
            )

            race_dropdown_options[
                (
                    f"{short_race_label(race)}"
                    f" · {rid}"
                )
            ] = rid


        selected_race_label = (
            st.selectbox(
                "Race ID",

                list(
                    race_dropdown_options.keys()
                ),
            )
        )


        selected_race_filter = (
            race_dropdown_options[
                selected_race_label
            ]
        )


        # ----------------------------------------------------
        # WHAT RACE SHOULD THE RU MENU FOLLOW?
        # ----------------------------------------------------

        ru_source_race = None


        # Explicit advanced override
        if (
            selected_race_filter
            is not None
        ):

            for race in base_races:

                if (
                    str(
                        race_id_value(
                            race
                        )
                    )
                    ==
                    str(
                        selected_race_filter
                    )
                ):

                    ru_source_race = (
                        race
                    )

                    break


        # Otherwise follow normal selector
        else:

            ru_source_race = (
                main_selected_race
            )


        # ----------------------------------------------------
        # REPORTING UNIT DROPDOWN
        # ----------------------------------------------------

        ru_dropdown_options = {
            "All reporting units":
                None
        }


        if ru_source_race:

            for ru in (
                get_level_2_reporting_units(
                    ru_source_race
                )
            ):

                ru_id = (
                    reporting_unit_id(
                        ru
                    )
                )

                ru_name = (
                    reporting_unit_name(
                        ru
                    )
                )


                ru_dropdown_options[
                    f"{ru_name} · {ru_id}"
                ] = ru_id


        selected_ru_label = (
            st.selectbox(
                "Reporting Unit ID",

                list(
                    ru_dropdown_options.keys()
                ),
            )
        )


        selected_ru_filter = (
            ru_dropdown_options[
                selected_ru_label
            ]
        )


    # --------------------------------------------------------
    # LOAD / REFRESH
    # --------------------------------------------------------

    refresh_clicked = (
        st.button(
            "▷ Load Results",
            use_container_width=True,
        )
    )


    if refresh_clicked:
        fetch_elapi.clear()
        st.rerun()


    render_html(
        '<div class="side-divider"></div>'
    )


    # --------------------------------------------------------
    # MAP VIEW
    # --------------------------------------------------------

    st.markdown(
        "### Map View"
    )


    map_view = (
        st.radio(
            "Map View",
            [
                "EEVP",
                "Margin",
                "Dem %",
                "GOP %",
                "Total Votes",
                "Expected Vote",
            ],
            label_visibility=
                "collapsed",
        )
    )


    render_html(
        '<div class="side-divider"></div>'
    )


    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    st.markdown(
        "### Display Options"
    )


    show_labels = (
        st.toggle(
            "Show county labels",
            value=False,
        )
    )


    show_tooltips = (
        st.toggle(
            "Show tooltips",
            value=True,
        )
    )


# ============================================================
# DETERMINE ACTUAL RACE
# ============================================================

# Advanced filter explicitly overrides main selector.
if (
    selected_race_filter
    is not None
):

    effective_race_id = (
        str(
            selected_race_filter
        )
    )

else:

    effective_race_id = (
        str(
            race_id_value(
                main_selected_race
            )
        )
        if main_selected_race
        else None
    )


race_ids = (
    [effective_race_id]
    if effective_race_id
    else None
)


ru_ids = (
    [
        str(
            selected_ru_filter
        )
    ]
    if (
        selected_ru_filter
        is not None
    )
    else None
)


level_param = (
    "ru"
    if (
        level_choice
        == "Reporting units (RU)"
    )
    else "state"
)


# ============================================================
# FETCH SELECTED RACE
# ============================================================

try:
    data = fetch_elapi(
        election_date=
            ELECTION_DATE,

        state_postal=
            STATE_POSTAL,

        race_ids=
            race_ids,

        reporting_unit_ids=
            ru_ids,

        level=
            level_param,
    )

except Exception as exc:
    st.error(
        "Could not load ELAPI data."
    )

    st.code(
        str(exc)
    )

    st.stop()


races = get_races(
    data
)


if not races:
    st.warning(
        "No race was returned for the current filters."
    )

    st.stop()


# We specifically requested one race.
selected_race = (
    races[0]
)


# ============================================================
# EXTRACT
# ============================================================

state_ru = (
    get_state_reporting_unit(
        selected_race
    )
)


county_df = (
    build_county_dataframe(
        selected_race
    )
    if (
        level_param
        == "ru"
    )
    else pd.DataFrame()
)


# ============================================================
# STATE EXPECTED DATA
# ============================================================

state_expected = (
    get_expected_data(
        state_ru
        if state_ru
        else selected_race
    )
)


state_expected_actual = (
    state_expected[
        "expected_actual"
    ]
)


state_eevp_cap = (
    state_expected[
        "eevp_cap"
    ]
)


state_registered = (
    state_expected[
        "registered"
    ]
)


# ============================================================
# STATE EEVP
# ============================================================

race_eevp = field(
    selected_race,
    "eevp",
    "EEVP",
    default=0,
)


if state_ru:

    race_eevp = field(
        state_ru,
        "eevp",
        "EEVP",
        default=race_eevp,
    )


try:
    state_eevp = float(
        race_eevp or 0
    )

except (
    TypeError,
    ValueError,
):
    state_eevp = 0


# ============================================================
# TOTALS
# ============================================================

state_votes = (
    state_total_votes(
        state_ru
    )
)


reporting_units_total = (
    len(county_df)
)


reporting_units_reporting = (
    int(
        (
            county_df[
                "Total Votes"
            ]
            > 0
        ).sum()
    )
    if not county_df.empty
    else 0
)


# ============================================================
# TIMESTAMP
# ============================================================

last_updated_raw = None


if state_ru:

    last_updated_raw = field(
        state_ru,
        "lastUpdated",
        "LastUpdated",
    )


if not last_updated_raw:

    last_updated_raw = field(
        data,
        "timestamp",
        "TimeStamp",
        "Timestamp",
    )


last_updated = (
    format_timestamp(
        last_updated_raw
    )
)


# ============================================================
# RACE METADATA
# ============================================================

selected_race_id = (
    race_id_value(
        selected_race
    )
)


race_status = field(
    selected_race,
    "raceCallStatus",
    "RaceCallStatus",
    default="—",
)


tabulation_status = field(
    selected_race,
    "tabulationStatus",
    "TabulationStatus",
    default="—",
)


office_name = field(
    selected_race,
    "officeName",
    "OfficeName",
    default="Race",
)


seat_name = field(
    selected_race,
    "seatName",
    "SeatName",
)


if seat_name:

    hero_title = (
        f"Georgia "
        f"{office_name} "
        f"— {seat_name}"
    )

else:

    hero_title = (
        f"Georgia "
        f"{office_name}"
    )


hero_title_safe = (
    html_lib.escape(
        str(
            hero_title
        )
    )
)


last_updated_safe = (
    html_lib.escape(
        str(
            last_updated
        )
    )
)


# ============================================================
# HEADER
# ============================================================

header_left, header_right = (
    st.columns(
        [4, 1]
    )
)


with header_left:

    render_html(
        f"""
        <div class="hero-title">
            {hero_title_safe}
        </div>
        """
    )

    render_html(
        """
        <div class="hero-subtitle">
            2026 General Election
        </div>
        """
    )


with header_right:

    render_html(
        f"""
        <div class="updated">
            Last updated:
            {last_updated_safe}
        </div>
        """
    )


st.write("")


# ============================================================
# METRICS
# ============================================================

reporting_pct = (
    reporting_units_reporting
    / reporting_units_total
    * 100
    if reporting_units_total
    else 0
)


m1, m2, m3, m4, m5 = (
    st.columns(5)
)


with m1:

    render_html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                ▮▮ &nbsp;
                Estimated Expected Vote
            </div>

            <div class="metric-value-blue">
                {state_eevp:.0f}%
            </div>

            <div class="track">

                <div
                    class="track-blue"
                    style="
                        width:
                        {min(state_eevp,100):.1f}%;
                    "
                ></div>

            </div>

        </div>
        """
    )


with m2:

    render_html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                ▤ &nbsp;
                Reporting Units
            </div>

            <div class="metric-value">
                {reporting_units_reporting}
                /
                {reporting_units_total}
            </div>

            <div class="track">

                <div
                    class="track-green"
                    style="
                        width:
                        {min(reporting_pct,100):.1f}%;
                    "
                ></div>

            </div>

        </div>
        """
    )


with m3:

    render_html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                ◫ &nbsp;
                Expected Vote
            </div>

            <div class="metric-value">
                {fmt_int(state_expected_actual)}
            </div>

            <div
                style="
                    color:#89939f;
                    font-size:.76rem;
                    margin-top:7px;
                "
            >
                EEVP cap:
                {fmt_pct(state_eevp_cap, 0)}
            </div>

        </div>
        """
    )


with m4:

    render_html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                ♙ &nbsp;
                Total Votes Reported
            </div>

            <div class="metric-value">
                {state_votes:,}
            </div>

        </div>
        """
    )


with m5:

    render_html(
        f"""
        <div class="metric-card">

            <div class="metric-label">
                ◷ &nbsp;
                Last Update
            </div>

            <div
                class="metric-value"
                style="
                    font-size:.94rem;
                    margin-top:12px;
                "
            >
                {last_updated_safe}
            </div>

        </div>
        """
    )


st.write("")


# ============================================================
# RU VIEW
# ============================================================

if level_param == "ru":

    map_col, table_col = (
        st.columns(
            [1.08, 1.08],
            gap="medium",
        )
    )


    # ========================================================
    # MAP
    # ========================================================

    with map_col:

        with st.container(
            border=True
        ):

            render_html(
                """
                <div class="panel-title">
                    🗺️ &nbsp;
                    Georgia Counties
                </div>

                <div class="panel-subtitle">
                    County-level ELAPI reporting units
                </div>
                """
            )


            if county_df.empty:

                st.info(
                    "No county-level reporting units returned."
                )

            else:

                geojson = (
                    get_georgia_geojson()
                )


                map_df = (
                    county_df.copy()
                )


                # --------------------------------------------
                # COLORS
                # --------------------------------------------

                eevp_scale = [
                    [0.0000, "#30363d"],
                    [0.0001, "#30363d"],
                    [0.10, "#d6e8ff"],
                    [0.25, "#9dc8ff"],
                    [0.50, "#5ca5f5"],
                    [0.75, "#2478d0"],
                    [1.00, "#064b96"],
                ]


                if map_view == "EEVP":

                    color_column = "EEVP"

                    color_scale = (
                        eevp_scale
                    )

                    range_color = (
                        0,
                        100,
                    )


                elif map_view == "Margin":

                    color_column = (
                        "Margin Numeric"
                    )

                    color_scale = (
                        "RdBu"
                    )

                    range_color = (
                        -100,
                        100,
                    )


                elif map_view == "Dem %":

                    color_column = (
                        "Dem %"
                    )

                    color_scale = (
                        "Blues"
                    )

                    range_color = (
                        0,
                        100,
                    )


                elif map_view == "GOP %":

                    color_column = (
                        "GOP %"
                    )

                    color_scale = (
                        "Reds"
                    )

                    range_color = (
                        0,
                        100,
                    )


                elif (
                    map_view
                    == "Expected Vote"
                ):

                    color_column = (
                        "Expected Vote"
                    )

                    color_scale = (
                        "Blues"
                    )

                    range_color = None


                else:

                    color_column = (
                        "Total Votes"
                    )

                    color_scale = (
                        "Blues"
                    )

                    range_color = None


                # --------------------------------------------
                # CHOROPLETH
                # --------------------------------------------

                fig = px.choropleth(
                    map_df,

                    geojson=
                        geojson,

                    locations=
                        "FIPS",

                    featureidkey=
                        "id",

                    color=
                        color_column,

                    color_continuous_scale=
                        color_scale,

                    range_color=
                        range_color,
                )


                custom_data = (
                    map_df[
                        [
                            "County",
                            "Reporting Unit ID",
                            "EEVP",
                            "Dem %",
                            "GOP %",
                            "Total Votes",
                            "Expected Vote",
                        ]
                    ]
                    .fillna(0)
                    .to_numpy()
                )


                if show_tooltips:

                    hovertemplate = (
                        "<b>%{customdata[0]}</b>"
                        "<br><br>"
                        "RU ID: %{customdata[1]}"
                        "<br>"
                        "EEVP: %{customdata[2]:.0f}%"
                        "<br>"
                        "Dem: %{customdata[3]:.1f}%"
                        "<br>"
                        "GOP: %{customdata[4]:.1f}%"
                        "<br>"
                        "Votes: %{customdata[5]:,}"
                        "<br>"
                        "Expected: %{customdata[6]:,}"
                        "<extra></extra>"
                    )

                else:

                    hovertemplate = (
                        "<extra></extra>"
                    )


                fig.update_traces(
                    customdata=
                        custom_data,

                    hovertemplate=
                        hovertemplate,

                    marker_line_color=
                        "#dbe3ec",

                    marker_line_width=
                        .60,
                )


                # --------------------------------------------
                # MAP FIT
                #
                # Statewide races: all Georgia counties.
                #
                # House races: naturally zoom to only the
                # reporting units returned for that district.
                # --------------------------------------------

                fig.update_geos(
                    fitbounds=
                        "locations",

                    visible=
                        False,

                    bgcolor=
                        "rgba(0,0,0,0)",

                    projection_type=
                        "mercator",

                    domain=dict(
                        x=[
                            0.00,
                            0.88,
                        ],

                        y=[
                            0.00,
                            1.00,
                        ],
                    ),
                )


                # --------------------------------------------
                # COUNTY LABELS
                # --------------------------------------------

                if show_labels:

                    county_lookup = {
                        str(row["FIPS"]):
                            row["County"]

                        for _, row
                        in map_df.iterrows()
                    }


                    label_lons = []
                    label_lats = []
                    label_names = []


                    for feature in (
                        geojson[
                            "features"
                        ]
                    ):

                        feature_id = str(
                            feature[
                                "id"
                            ]
                        )


                        if (
                            feature_id
                            not in county_lookup
                        ):

                            continue


                        lon, lat = (
                            feature_centroid(
                                feature
                            )
                        )


                        if (
                            lon is None
                            or lat is None
                        ):

                            continue


                        label_lons.append(
                            lon
                        )

                        label_lats.append(
                            lat
                        )

                        label_names.append(
                            county_lookup[
                                feature_id
                            ]
                            .replace(
                                " County",
                                "",
                            )
                        )


                    fig.add_trace(
                        go.Scattergeo(
                            lon=
                                label_lons,

                            lat=
                                label_lats,

                            text=
                                label_names,

                            mode=
                                "text",

                            textfont=dict(
                                size=7,
                                color=
                                    "#e4ebf3",
                            ),

                            hoverinfo=
                                "skip",

                            showlegend=
                                False,
                        )
                    )


                # --------------------------------------------
                # LAYOUT
                # --------------------------------------------

                fig.update_layout(
                    height=
                        610,

                    margin=dict(
                        l=0,
                        r=0,
                        t=0,
                        b=0,
                    ),

                    paper_bgcolor=
                        "rgba(0,0,0,0)",

                    plot_bgcolor=
                        "rgba(0,0,0,0)",

                    font=dict(
                        color=
                            "#ffffff"
                    ),

                    hoverlabel=dict(
                        bgcolor=
                            "#111820",

                        bordercolor=
                            "#34404c",

                        font=dict(
                            color=
                                "#ffffff",

                            size=
                                13,
                        ),
                    ),

                    coloraxis_colorbar=dict(
                        title=
                            map_view,

                        thickness=
                            11,

                        len=
                            .70,

                        x=
                            .93,

                        xanchor=
                            "left",

                        y=
                            .50,

                        outlinewidth=
                            0,

                        tickfont=dict(
                            color=
                                "#aeb7c3",

                            size=
                                11,
                        ),
                    ),
                )


                st.plotly_chart(
                    fig,

                    use_container_width=
                        True,

                    config={
                        "displayModeBar":
                            False,

                        "scrollZoom":
                            False,
                    },
                )


    # ========================================================
    # RESULTS TABLE
    # ========================================================

    with table_col:

        with st.container(
            border=True
        ):

            heading_col, search_col = (
                st.columns(
                    [2, 1]
                )
            )


            with heading_col:

                render_html(
                    """
                    <div class="panel-title">
                        ▤ &nbsp;
                        County Results
                    </div>

                    <div class="panel-subtitle">
                        Reporting units in this race
                    </div>
                    """
                )


            with search_col:

                search = (
                    st.text_input(
                        "Search counties",

                        placeholder=
                            "Search counties...",

                        label_visibility=
                            "collapsed",
                    )
                )


            display_df = (
                county_df.copy()
            )


            if search:

                display_df = (
                    display_df[
                        display_df[
                            "County"
                        ]
                        .str.contains(
                            search,
                            case=False,
                            na=False,
                        )
                    ]
                )


            render_html(
                build_results_table(
                    display_df
                )
            )


    # ========================================================
    # RU DETAIL
    # ========================================================

    st.write("")


    with st.container(
        border=True
    ):

        render_html(
            """
            <div class="panel-title">
                Reporting Unit Detail
            </div>

            <div class="panel-subtitle">
                Full ELAPI metadata for the selected reporting unit
            </div>
            """
        )


        county_options = (
            county_df[
                "County"
            ]
            .dropna()
            .tolist()
        )


        if county_options:

            default_index = 0


            if (
                selected_ru_filter
                is not None
            ):

                matches = (
                    county_df[
                        county_df[
                            "Reporting Unit ID"
                        ]
                        ==
                        str(
                            selected_ru_filter
                        )
                    ]
                )


                if not matches.empty:

                    target = (
                        matches
                        .iloc[0][
                            "County"
                        ]
                    )


                    if (
                        target
                        in county_options
                    ):

                        default_index = (
                            county_options
                            .index(
                                target
                            )
                        )


            selected_county = (
                st.selectbox(
                    "County",

                    county_options,

                    index=
                        default_index,
                )
            )


            selected_row = (
                county_df[
                    county_df[
                        "County"
                    ]
                    ==
                    selected_county
                ]
                .iloc[0]
            )


            poll_close = (
                format_poll_close(
                    selected_row[
                        "Poll Closing Time"
                    ]
                )
            )


            render_html(
                f"""
                <div class="detail-grid">

                    <div class="detail-card">
                        <div class="detail-label">
                            Reporting Unit ID
                        </div>
                        <div class="detail-value">
                            {html_lib.escape(str(selected_row["Reporting Unit ID"]))}
                        </div>
                    </div>

                    <div class="detail-card">
                        <div class="detail-label">
                            FIPS
                        </div>
                        <div class="detail-value">
                            {html_lib.escape(str(selected_row["FIPS"]))}
                        </div>
                    </div>

                    <div class="detail-card">
                        <div class="detail-label">
                            Registered
                        </div>
                        <div class="detail-value">
                            {fmt_int(selected_row["Registered"])}
                        </div>
                    </div>

                    <div class="detail-card">
                        <div class="detail-label">
                            Expected Vote
                        </div>
                        <div class="detail-value">
                            {fmt_int(selected_row["Expected Vote"])}
                        </div>
                    </div>

                    <div class="detail-card">
                        <div class="detail-label">
                            EEVP
                        </div>
                        <div class="detail-value">
                            {fmt_pct(selected_row["EEVP"],0)}
                        </div>
                    </div>

                    <div class="detail-card">
                        <div class="detail-label">
                            EEVP Cap
                        </div>
                        <div class="detail-value">
                            {fmt_pct(selected_row["EEVP Cap"],0)}
                        </div>
                    </div>

                    <div class="detail-card">
                        <div class="detail-label">
                            Precincts
                        </div>
                        <div class="detail-value">
                            {fmt_int(selected_row["Precincts Reporting"])}
                            /
                            {fmt_int(selected_row["Precincts Total"])}
                        </div>
                    </div>

                    <div class="detail-card">
                        <div class="detail-label">
                            Precinct Reporting %
                        </div>
                        <div class="detail-value">
                            {fmt_pct(selected_row["Precincts %"])}
                        </div>
                    </div>

                    <div class="detail-card">
                        <div class="detail-label">
                            GeoStratum
                        </div>
                        <div class="detail-value">
                            {html_lib.escape(str(selected_row["GeoStratum"]))}
                        </div>
                    </div>

                    <div class="detail-card">
                        <div class="detail-label">
                            PolStratum
                        </div>
                        <div class="detail-value">
                            {html_lib.escape(str(selected_row["PolStratum"]))}
                        </div>
                    </div>

                    <div class="detail-card">
                        <div class="detail-label">
                            Tab Status Number
                        </div>
                        <div class="detail-value">
                            {html_lib.escape(str(selected_row["Tab Status Number"] if selected_row["Tab Status Number"] is not None else "—"))}
                        </div>
                    </div>

                    <div class="detail-card">
                        <div class="detail-label">
                            Poll Closing Time
                        </div>
                        <div class="detail-value">
                            {html_lib.escape(str(poll_close))}
                        </div>
                    </div>

                </div>
                """
            )


            # =================================================
            # CANDIDATES
            # =================================================

            candidate_rows = []


            for candidate in (
                selected_row[
                    "Candidates"
                ]
            ):

                candidate_rows.append(
                    f"""
                    <tr>

                        <td>
                            {html_lib.escape(str(candidate["Name"] or "—"))}
                        </td>

                        <td>
                            {html_lib.escape(str(candidate["Party"] or "—"))}
                        </td>

                        <td>
                            {fmt_int(candidate["Votes"])}
                        </td>

                        <td>
                            {html_lib.escape(str(candidate["Candidate ID"] or "—"))}
                        </td>

                        <td>
                            {html_lib.escape(str(candidate["Ballot Order"] if candidate["Ballot Order"] is not None else "—"))}
                        </td>

                        <td>
                            {html_lib.escape(str(candidate["Pol ID"] or "—"))}
                        </td>

                    </tr>
                    """
                )


            render_html(
                f"""
                <div class="candidate-section-title">
                    Candidates
                </div>

                <table class="candidate-table">

                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Party</th>
                            <th>Votes</th>
                            <th>Candidate ID</th>
                            <th>Ballot Order</th>
                            <th>Pol ID</th>
                        </tr>
                    </thead>

                    <tbody>
                        {''.join(candidate_rows)}
                    </tbody>

                </table>
                """
            )


# ============================================================
# STATE VIEW
# ============================================================

else:

    st.info(
        "State-level mode selected. "
        "Choose Reporting units (RU) "
        "to display reporting-unit results."
    )


# ============================================================
# RACE METADATA
# ============================================================

st.write("")


with st.container(
    border=True
):

    render_html(
        """
        <div class="panel-title">
            Race Metadata
        </div>
        """
    )


    render_html(
        f"""
        <div class="detail-grid">

            <div class="detail-card">

                <div class="detail-label">
                    Race ID
                </div>

                <div class="detail-value">
                    {html_lib.escape(str(selected_race_id or "—"))}
                </div>

            </div>


            <div class="detail-card">

                <div class="detail-label">
                    Race Call Status
                </div>

                <div class="detail-value">
                    {html_lib.escape(str(race_status))}
                </div>

            </div>


            <div class="detail-card">

                <div class="detail-label">
                    Tabulation Status
                </div>

                <div class="detail-value">
                    {html_lib.escape(str(tabulation_status))}
                </div>

            </div>


            <div class="detail-card">

                <div class="detail-label">
                    State Registered
                </div>

                <div class="detail-value">
                    {fmt_int(state_registered)}
                </div>

            </div>

        </div>
        """
    )


# ============================================================
# RAW API
# ============================================================

with st.expander(
    "Raw ELAPI response"
):

    st.json(
        data
    )