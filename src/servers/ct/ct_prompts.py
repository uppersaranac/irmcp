"""ClinicalTrials prompts defined via FastMCP app decorators.

Call register_prompts(app) after creating the server to attach prompts.
"""

from typing import Any


def register_prompts(app: Any) -> None:
    """Register prompts on the given FastMCP app using decorators.
    
    :param app: FastMCP server instance to register prompts on
    :type app: Any
    """

    @app.prompt(
        name="find_matching_trials",
        title="Find Matching Clinical Trials",
        description="Search and rank appropriate clinical trials",
    )
    def find_matching_trials() -> str:
        return (
            "You are a medical doctor and you are trying to find\n"
            "clinical trials for a patient that may save their life or make their lives healthier.\n"
            "Be thorough and meticulous in your analysis. Conservative judgment is important in\n"
            "providing the best care to your patient, so think deeply.\n\n"
            "1. Examine the patient's medical history. It is important to know their specific condition,\n"
            "  their age, sex and location. CRITICAL: if the location of the patient\n"
            "  is not given, you must ask the human for the location before proceeding to search for clinical trials.\n"
            "2. Once you have that information or at least some of it, search the Clinical Trials\n"
            "database for relevant studies using a query developed using the following guidelines:\n"
            "  a. Generate a list of synonyms for the patient's condition that are preferably taken from MeSH\n"
            "    or SNOMED CT. OR these terms together to search the Condition and Keyword data fields.\n"
            "  b. Search on age fields if appropriate. Age values must have units, such as in `AREA[MaximumAge] RANGE[66 years,MAX]`.\n"
            "    The query will fail if you don't add \"years\" to the age.\n"
            "  c. Use the patient's location and expand it to include nearby regions.\n"
            "  d. The study should be recruiting, active, or not yet recruiting.\n"
            "  e. Sex should match the patient's sex if given.\n"
            "  f. When requesting the fields to be returned, ask for only those fields you will need for the rest of\n"
            "    the analysis in order to maximize the number of trials under consideration. These fields\n"
            "    should come from the list under Study Data Fields. You should not request modules,\n"
            "    only the fields within those modules. Do not assume fields exist.\n"
            "    If unsure what fields are need, use the studies_metadata endpoint\n"
            "  g. make sure to sort by relevance (@relevance:desc) so that relevant studies come first.\n"
            "3. Examining the list of clinical trials returned one by one, then examine the following parts of the clinical trial step by step. Think carefully:\n"
            "  a. if the patient's sex does not match the clinical trial's requirements, exclude the study.\n"
            "  b. if the patient's age does not match the clinical trial's requirements, exclude the study.\n"
            "  c. print out the exclusion criteria one by one. Use your medical judgement when evaluating the criteria and use these symbols:\n"
            "    - ✅ = Patient explicitly meets the criterion based on provided information\n"
            "    - ❌ = Patient explicitly does not meet the criterion\n"
            "    - ❓ = Insufficient information to determine if criterion is met\n"
            "    CRITICAL: Only use ✅ when you have explicit data from the medical record\n"
            "    confirming the patient meets the criterion.\n"
            "    If any clinical data (lab values, test results, measurements) is missing or inferred, use ❓.\n"
            "    ***DO NOT PREDICT*** clinical data. If there is not enough\n"
            "    information, ask the human for clarification. If in your medical opinion the\n"
            "    patient unambiguously meets an exclusion criterion based\n"
            "    on explicit information in their record, exclude that study. If the match is ambiguous, assign an\n"
            "    importance level to the importance of the criterion in considering the study based on the level of ambiguity or irrelevance.\n"
            "  d. print out the inclusion criteria one by one. Use your medical judgement when evaluating the criteria and use these symbols:\n"
            "    - ✅ = Patient explicitly meets the criterion based on provided information\n"
            "    - ❌ = Patient explicitly does not meet the criterion\n"
            "    - ❓ = Insufficient information to determine if criterion is met\n"
            "    CRITICAL: Only use ✅ when you have explicit data from the medical record\n"
            "    confirming the patient meets the criterion.\n"
            "    If any clinical data (lab values, test results, measurements) is missing or inferred, use ❓.\n"
            "    ***DO NOT PREDICT*** clinical data. If there is not enough\n"
            "    information, ask the human for clarification. If in your medical opinion the\n"
            "    patient unambiguously meets an exclusion criterion based\n"
            "    on explicit information in their record, exclude that study. If the match is ambiguous, assign an\n"
            "    importance level to the importance of the criterion in considering the study based on the level of ambiguity or irrelevance.\n"
            "4. Use your medical judgement to rank the remaining studies based on the likelihood of the patient matching\n"
            "  the inclusion criteria, not matching the exclusion criteria, and the potential relevance and benefit to the patient.\n"
            "  Explicit matches to inclusion and exclusion criteria should influence your decision more than implicit matches.\n"
            "  Implicit matches to criteria should influence your decision more that when there isn't enough information to\n"
            "  make a determination on a match. Criteria inapplicable to the patient should be not be considered.\n"
            "  List the clinical trials in order of relevance and detail the reasons for your decision. Reasons may include:\n"
            "  a. meeting the patients's needs: particular applicability to the patient's condition and desires, e.g. the level of severity matches \n"
            "    the rest of the trial population and the patient is looking for pain relief.\n"
            "  b. that the therapy being tested may materially improve the patient's life\n"
            "  c. good matches to the inclusion criteria.  \n"
            "  d. that it is extremely unlikely that the patient would be excluded.\n"
            "5. Generate a list of questions that the patient can ask their doctors\n"
            "  to further clarify if they are eligible for various trials.\n"
        )
