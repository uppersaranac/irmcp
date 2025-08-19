from __future__ import annotations

import os
from typing import Any, Dict

# Ensure FastMCP uses the experimental OpenAPI parser before importing fastmcp modules
os.environ.setdefault("FASTMCP_EXPERIMENTAL_ENABLE_NEW_OPENAPI_PARSER", "true")

import yaml
from fastmcp.experimental.utilities.openapi import convert_openapi_schema_to_json_schema

from irmcp.server import create_server, make_async_httpx_client

# Prompt registry for ClinicalTrials.gov MCP server
PROMPT_REGISTRY: Dict[str, Dict[str, Any]] = {
    "find_matching_trials": {
        "title": "Find Matching Clinical Trials",
        "description": "Search and rank appropriate clinical trials",
        "message": """You are a medical doctor and you are trying to find
clinical trials for a patient that may save their life or make their lives healthier.
Be thorough and meticulous in your analysis. Conservative judgment is important in
providing the best care to your patient, so think deeply.

1. Examine the patient's medical history. It is important to know their specific condition,
their age, sex and location. If they haven't given you that information, ask the human before performing the search.
2. Once you have that information or at least some of it, search the Clinical Trials
database for relevant studies using a query developed using the following guidelines:
  a. Generate a list of synonyms for the patient's condition that are preferably taken from MeSH
    or SNOMED CT. OR these terms together to search the Condition and Keyword data fields.
  b. Search on age fields if appropriate. Age values must have units, such as in `AREA[MaximumAge] RANGE[66 years,MAX]`.
    The query will fail if you don't add "years" to the age.
  c. Use the patient's location and expand it to include nearby regions.
  d. The study should be recruiting, active, or not yet recruiting.
  e. Sex should match the patient's sex if given.
  f. When requesting the fields to be returned, ask for only those fields you will need for the rest of
    the analysis in order to maximize the number of trials under consideration. These fields
    should come from the list under Study Data Fields. You should not request modules,
    only the fields within those modules. Do not assume fields exist.
    If unsure what fields are need, use the studies_metadata endpoint
  g. make sure to sort by relevance (@relevance:desc) so that relevant studies come first.
3. Examining the list of clinical trials returned one by one, then examine the following parts of the clinical trial step by step. Think carefully:
  a. if the patient's sex does not match the clinical trial's requirements, exclude the study.
  b. if the patient's age does not match the clinical trial's requirements, exclude the study.
  c. print out the exclusion criteria one by one and give your medical opinion on whether the patient matches (put a checkbox next to the criterion) or does not match
    that criterion (put a minus by the criterion), or that there is not enough information or the criterion is inapplicable 
    (put a ? by the criterion). If there is not enough
    information, ask the human for clarification. If in your medical opinion the
    patient unambiguously meets an exclusion criterion based
    on explicit information in their record, exclude that study. If the match is ambiguous, assign an
    importance level to the importance of the criterion in considering the study based on the level of ambiguity or irrelevance.
  d. print out the inclusion criteria one by one and give your medical opinion on whether the patient matches (put a checkbox next to the criterion) or does not match
    that criterion (put a minus by the criterion), or that there is not enough information or the criterion is inapplicable (put a ? by the criterion).
    If there is not enough information, ask the human for clarification.
    If in your medical opinion the patient unambiguously does not meet an inclusion criterion based
    on explicit information in their record, exclude the study. If the match is ambiguous, assign an
    importance level to the importance of the criterion in considering the study based on the level of ambiguity or irrelevance.
4. Use your medical judgement to rank the remaining studies based on the likelihood of the patient matching
  the inclusion criteria, not matching the exclusion criteria, and the potential relevance and benefit to the patient.
  Explicit matches to inclusion and exclusion criteria should influence your decision more than implicit matches.
  Implicit matches to criteria should influence your decision more that when there isn't enough information to
  make a determination on a match. Criteria inapplicable to the patient should be not be considered.
  List the clinical trials in order of relevance and detail the reasons for your decision. Reasons may include:
  a. meeting the patients's needs: particular applicability to the patient's condition and desires, e.g. the level of severity matches 
    the rest of the trial population and the patient is looking for pain relief.
  b. that the therapy being tested may materially improve the patient's life
  c. good matches to the inclusion criteria.  
  d. that it is extremely unlikely that the patient would be excluded.
5. Generate a list of questions that the patient can ask their doctors
  to further clarify if they are eligible for various trials.
"""
    }
}

# Read clinical trials search guide file
def load_essie_rules() -> str:
    rules_file = os.path.join(os.path.dirname(__file__), "essie_gpt.md")
    try:
        with open(rules_file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "ClinicalTrials.gov study search guide file not found."


# TOOL_REGISTRY['list_studies']["description"] += "\n\n" + load_essie_rules() + """
# \n\n When composing queries you must follow these guidelines:
# 1. Only use the search fields, search areas, sections, modules and structs given above. Use full names and do not invent names.
# 2. Use ESSIE search syntax for params that can accept that format except when doing free text searching.
# 3. When filling out the fields parameter, use only fields, not modules.
# """

# Server configuration
API_BASE = os.environ.get("API_BASE", "https://clinicaltrials.gov/api/v2")
DEFAULT_TIMEOUT = float(os.environ.get("API_TIMEOUT", "30"))


def main() -> None:
  """Entry point: build and run the MCP server."""

  # Use an async client: FastMCP's OpenAPI server awaits HTTP calls
  client = make_async_httpx_client(
    base_url=API_BASE,
    timeout=DEFAULT_TIMEOUT,
    log_http=os.environ.get("API_HTTP_LOG", "").lower() in {"1", "true", "yes", "on", "debug"},
    log_headers=os.environ.get("API_HTTP_LOG_HEADERS", "").lower() in {"1", "true", "yes", "on"},
    log_body=os.environ.get("API_HTTP_LOG_BODY", "").lower() in {"1", "true", "yes", "on"},
    logger_name="ct.http",
  )

  schema_path = os.path.join(os.path.dirname(__file__), "ctg-oas-v2.yaml")
  with open(schema_path, "r", encoding="utf-8") as f:
    schema = yaml.safe_load(f)

  openapi_spec = convert_openapi_schema_to_json_schema(schema=schema)

  # Build app using the server factory with both tools and prompts
  app = create_server(
    name="clinical-trials",
    openapi_spec=openapi_spec,
    client=client,
    prompt_registry=PROMPT_REGISTRY,
  )
  app.run()

if __name__ == "__main__":
    main()
