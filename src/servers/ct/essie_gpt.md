# Constructing Complex Search Queries for ClinicalTrials.gov

## Query Syntax Grammar (BNF and Precedence)

Below is a Backus–Naur Form (BNF) defining the ESSIE query language for the ClinicalTrials.gov API. This grammar captures how to build complex search queries, including the use of Boolean logic, field scoping, grouping, and special operators. Precedence of operators is indicated (from highest to lowest): unary context operators (including NOT, field/context specifiers, etc.) are evaluated first, then AND, then OR (which has the lowest precedence) ￼.

&lt;Query>           ::= &lt;OrExpr>

&lt;OrExpr>          ::= &lt;AndExpr> ( OR &lt;AndExpr> )*
                    // OR has lowest precedence .

&lt;AndExpr>         ::= &lt;OperatorExpr> ( AND &lt;OperatorExpr> )*
                    // AND evaluated after all unary operators .

&lt;OperatorExpr>    ::= { &lt;UnaryOp> } &lt;SourceExpr>
                    // Any number of unary context ops (including NOT) may prefix a source expression .

&lt;UnaryOp>         ::= NOT
                    | EXPANSION[None|Term|Concept|Relaxation|Lossy]
                    | COVERAGE[FullMatch|StartsWith|EndsWith|Contains]
                    | TILT[&lt;FieldName>]
                    // Unary operators that modify context or scoring .

&lt;SourceExpr>      ::= ALL
                    | SEARCH[Study] '(' &lt;OrExpr> ')'
                    | SEARCH[Location] '(' &lt;OrExpr> ')'
                    | AREA[&lt;FieldOrArea>] &lt;ValueExpr>
                    // Source of search terms: either the entire study, a Location context, or a specific field/area .

&lt;ValueExpr>       ::= &lt;Term>
                    | " &lt;Phrase> "
                    | '(' &lt;OrExpr> ')'
                    | RANGE[&lt;Low>, &lt;High>]
                    | MISSING
                    // A value can be a single term, a quoted phrase, a grouped sub-query, a range, or a MISSING indicator.

Notes: In this grammar, &lt;Term> represents a single search term (a word or number without spaces or special operators) ￼. &lt;Phrase> represents a multi-word phrase enclosed in quotes (e.g. "heart attack"), which will be matched exactly in order ￼. &lt;FieldOrArea> can be the name of any searchable study field or a predefined search area (group of fields). &lt;Low> and &lt;High> in a RANGE are boundary values (for dates or numbers) or special tokens MIN/MAX indicating the extreme ends ￼.

According to the precedence rules, all unary operators (like NOT, EXPANSION, COVERAGE, TILT, or an AREA/SEARCH specifier) are applied first to their immediately following expression, then AND operations are evaluated, and finally OR operations last ￼. Parentheses can be used to override these defaults and group expressions explicitly ￼.

## Query Language Elements and Operators

Below we explain each element of the BNF – search terms, expressions, and various operators – including how to compose sub-expressions and how different operators affect the query. We also clarify the distinction between search areas (groups of fields) and individual study fields in queries.

* Search Term: A search term is a basic word or token to match in the data. It may be a single word (e.g. aspirin) or a number, or an exact phrase when enclosed in quotes (e.g. "heart attack"). Quoted phrases require the words to appear together in the specified order ￼. Terms are case-insensitive by default, and minor variations (plurals, hyphenation) are handled by the search engine’s expansion logic ￼. If a term collides with a reserved operator word, prefix it with a backslash to treat it literally (e.g. \AND) ￼.
* Search Expression: A search expression is any combination of terms and operators that can be evaluated to filter studies. In the grammar above, &lt;Query>, &lt;OrExpr>, &lt;AndExpr> etc. represent increasingly structured search expressions. By default, multiple terms without an explicit operator are interpreted as an AND combination (the default Boolean operator is AND) ￼. For example, the query heart attack aspirin is equivalent to heart attack AND aspirin (meaning studies containing both terms). Use OR to broaden the search (match either term) and NOT to exclude terms. All search expressions ultimately resolve to a set of matching study records.
* Boolean Operators (AND, OR, NOT): Boolean operators connect search terms or sub-expressions logically. AND means both conditions must be satisfied, OR means either may be satisfied, and NOT excludes records containing the term/expression it prefixes. These operators must be written in uppercase. In terms of precedence: NOT (a unary operator) is applied to a term/expression first, then AND is evaluated, and OR last ￼. You can use parentheses to group logic and override precedence. For example: (aspirin OR ibuprofen) AND NOT "heart failure" will find studies that contain either “aspirin” or “ibuprofen” (or both) and do not mention “heart failure” ￼ ￼.
* Grouping (Parentheses): Parentheses (...) are used to group sub-expressions and force a certain evaluation order that differs from the default precedence. Anything inside ( and ) is treated as a single unit. For instance, in the query acetaminophen OR (aspirin AND ibuprofen), the parentheses ensure that aspirin AND ibuprofen is evaluated together (requiring both terms) before the OR considers acetaminophen ￼. Without parentheses, the default precedence would have AND evaluated before OR anyway, but complex combinations always benefit from explicit grouping for clarity.
* Search Areas vs. Study Fields: A search area is a predefined group of one or more related fields from the study record that can be searched together. For example, the ConditionSearch area encompasses fields related to conditions (diseases) associated with the study, and the LocationSearch area covers fields for facility location information. Using a search area allows querying multiple related fields at once with a single term. By contrast, a study field refers to a specific data field in the study structure (e.g. the BriefTitle field or the LocationCity field). In query syntax, you can target either an entire search area or a specific field using the AREA[...] operator, or switch context to nested data (like locations) using the SEARCH[...] operator, as described below.
* Source Operator – AREA[…] (Field/Area Scoping): The AREA operator restricts a search term or sub-expression to a particular field or search area of the study record ￼. You provide the field name or area name in square brackets after AREA. For example:
* AREA[InterventionName] aspirin searches for the term “aspirin” only in the Intervention Name field of studies ￼.
* AREA[BriefTitle] "heart attack" searches for the exact phrase “heart attack” only in study titles.
* AREA[LocationCity] Boston AND AREA[LocationState] Massachusetts finds studies with “Boston” in the city field and “Massachusetts” in the state field (in any location record).
Any field from the study data structure can be searched this way; the documentation notes that “any field from the study structure is searchable” via an area specifier ￼. If the argument of AREA[...] corresponds to a multi-field search area (like ConditionSearch or LocationSearch), the query will be applied to all fields in that area simultaneously (with their defined weights). If it is a single field, the search is limited to that field. You can also group multiple terms inside one field-scoped expression: e.g. AREA[BriefTitle] (aspirin AND stroke) would require both “aspirin” and “stroke” to appear in the Brief Title field of a study record.
* Context Operator – SEARCH[…] (Nested Contexts): The SEARCH operator is used to specify a context within the study structure that may repeat or that requires grouping of fields. In practice, SEARCH is most relevant for nested record sets like locations. The SEARCH[Location]( ... ) operator limits the scope of the enclosed sub-query to each location (facility) of a study ￼. This ensures that all conditions inside the parentheses must be satisfied by the same location record. For example:
heart attack AND SEARCH[Location](AREA[LocationCity] Portland AND AREA[LocationState] Maine) ￼
This query finds studies where “heart attack” appears (in default areas) and which have at least one location with city = Portland and state = Maine. By using SEARCH[Location], we guarantee Portland and Maine refer to the same site. Without it, a study that had “Portland” in one location and “Maine” in another different location could incorrectly match (since AREA[LocationCity]Portland AND AREA[LocationState]Maine without the context might match across different records). SEARCH[Location] groups the location-specific criteria. The SEARCH operator can currently take either Location or Study as a parameter ￼ ￼. SEARCH[Study] would explicitly scope terms to the top-level study fields (which is usually the default context). In most cases you won’t need SEARCH[Study] because any terms not in a SEARCH[Location] block implicitly apply to the study-level fields.
* Expansion Operator – EXPANSION[…] (Synonym & Variant Control): The EXPANSION operator lets you control how much the search engine will expand a term to include synonyms or variations ￼. By default, ClinicalTrials.gov uses Concept expansion for most searches, meaning it will match not only the exact term but also synonyms and related terms (using the Unified Medical Language System, UMLS, and other sources) albeit with a slight scoring penalty for non-exact matches ￼. For example, a search for cancer will also find studies with “neoplasm” (a synonym), and a search for “heart attack” will match “myocardial infarction” even if the study uses the medical term ￼. You can change this behavior:
* EXPANSION[None] – No expansion; search the term exactly as written (case- and accent-sensitive, no plural/stem variations) ￼.
* EXPANSION[Term] – Basic lexical variations (e.g., plural forms, spelling variations) but no broader concept mapping ￼.
* EXPANSION[Concept] – (Default) Include synonym concepts from UMLS and other vocabularies ￼. For example, Concept expansion of “cancer” includes “malignancy” etc. Records that match the actual term are ranked higher than those matching only a synonym ￼.
* EXPANSION[Relaxation] – Further relaxes matching by allowing terms to appear separately and out of order. E.g. EXPANSION[Relaxation]"heart disease" could match a record that has “heart and lung disease” (terms separated) ￼. This comes with a larger scoring penalty (exact phrase matches rank higher) ￼.
* EXPANSION[Lossy] – Even more permissive; allows one of the terms to be missing entirely. E.g. EXPANSION[Lossy]"heart disease" might match a record that only has “heart” but not “disease”, or vice versa ￼. This is a very broad match and results in significantly lower relevancy score if the full term isn’t present ￼.
These expansion controls can be applied as a prefix to a term or a grouped expression. For example, EXPANSION[None] aspirin would search for “aspirin” exactly (no synonyms like “acetylsalicylic acid”), whereas EXPANSION[Concept] aspirin (or just aspirin by default) would match synonyms like “ASA” if present.
* Coverage Operator – COVERAGE[…] (Field Matching Extent): The COVERAGE operator specifies how fully a term must match the content of a field ￼. By default, a term can match anywhere within a field’s text (Contains). You can restrict this:
* COVERAGE[FullMatch] – The search term must match the entire content of the field exactly ￼. For instance, if a field value is “lung cancer”, a FullMatch search for “cancer” would not match because the field has additional text.
* COVERAGE[StartsWith] – Field value must begin with the search term ￼.
* COVERAGE[EndsWith] – Field value must end with the search term.
* COVERAGE[Contains] – The term can appear anywhere in the field (this is the default behavior if no coverage specified) ￼.
Coverage is useful if you need very precise matching in certain fields (for example, if you wanted studies where the Brief Title is exactly “Diabetes”, you might use AREA[BriefTitle] COVERAGE[FullMatch] diabetes).
* Range Expression – RANGE[…] (Numeric/Date Ranges): A range expression matches numeric or date fields within a specified interval. Use the syntax AREA[FieldName] RANGE[low, high] to find records where the field value falls between low and high (inclusive) ￼. This is typically used for numeric fields (like ages or enrollment counts) or dates. For example:
* AREA[MinimumAge] RANGE[0 years, 18 years] – finds studies with minimum eligible age between 0 and 18 (i.e., includes children).
* AREA[ResultsFirstPostDate] RANGE[01/01/2015, 12/31/2020] – finds studies that first posted results between Jan 1, 2015 and Dec 31, 2020 ￼.
You can use the special keywords MIN and MAX to indicate open-ended ranges ￼. For instance, AREA[EnrollmentCount] RANGE[500, MAX] finds studies with enrollment ≥500 (no upper bound), and RANGE[MIN, 1990] could be used on a date field to mean “up to 1990”. A study field must be numeric or date-typed for RANGE to work meaningfully. (If a field is text, putting a numeric range on it will likely fail or not match anything.)
* MISSING Operator: The MISSING keyword can be used to find studies where a certain field has no value ￼. For example, AREA[ResultsFirstPostDate] MISSING would retrieve all studies that have no results posted (the Results First Post Date field is empty) ￼. This is essentially a check for null/absent data in that field. You can combine this with other criteria (e.g., find studies that are completed but missing results: AREA[OverallStatus] "Completed" AND AREA[ResultsFirstPostDate] MISSING).
* ALL Operator: Using ALL by itself in a query will match every study in the database, regardless of any criteria ￼. This is rarely used except in combination with exclusions or other operators (since just ALL would retrieve everything). For instance, one could do ALL AND NOT cancer to get all studies that do not mention “cancer” anywhere – though this would be a very broad query. Essentially, ALL acts as a wildcard matching all records.
* Scoring Operator – TILT[…] (Relevance Biasing): While the search engine by default ranks results based on relevance (taking into account term frequency, field weight, synonym matches, etc.), the TILT operator allows you to bias the ranking toward certain values in an ordered field ￼. The typical use is to favor more recent studies by tilting on date fields. For example:
* TILT[StudyFirstPostDate] prostate cancer ￼ will prioritize studies where “prostate cancer” appears in more recently posted studies. TILT[StudyFirstPostDate] imposes a scoring penalty on older studies, so that among the set of studies matching “prostate cancer”, those with later first-posted dates rank higher than those with earlier dates ￼.
TILT can be used with any field that has an inherent order (dates, numeric values, perhaps phases). The operator doesn’t filter out any records; it only affects the sort order by boosting records with higher (more desirable) field values. For example, one might use TILT[EnrollmentCount] aspirin to favor studies with larger enrollment numbers if that was relevant, or TILT[LastUpdatePostDate] diabetes to favor studies updated more recently. Keep in mind, TILT is about biasing ranking, not strict filtering. (If you need strict sorting of results, the API’s separate sort parameter can be used, but that’s outside the query syntax.)

In summary, a complex query can combine these elements to precisely target studies. For instance, you could write a query that searches multiple fields for multiple terms, uses SEARCH[Location] to bind city/state together, uses RANGE to restrict ages, and so on. The next sections list the actual field names and search areas available, and then we’ll walk through some example queries to illustrate how everything comes together.

## Study Data Fields (Structure, Types, Synonyms, Examples)

ClinicalTrials.gov study records are structured into many fields. Below is a list of key study data fields that are commonly used in search queries, along with their data types, any special synonyms or controlled vocabulary, and a brief description. Where applicable, we provide example values and mention ontologies or vocabularies (e.g. MeSH) used for that field.

* NCTId (text) – National Clinical Trial Identifier, the unique registry ID assigned by ClinicalTrials.gov. Format is “NCT” followed by an 8-digit number. Example: NCT04292899 ￼. This is an index field (searchable) in the Identification Module of the study record. No synonyms or expansion are applied (it’s an exact identifier).
* OrgStudyId (text) – The “Other Study ID” or unique identifier assigned by the study’s sponsor or institution. This is often an alphanumeric code. Example: Study-XYZ-123. Treated as text; synonyms are generally not applicable (though the search engine may still treat it as a text field). This field is indexed for search (often grouped under “Study IDs” searches) ￼.
* SecondaryId (text) – Another secondary identifier for the study (there can be multiple). For example, an NIH grant number or EudraCT number might appear here. Example: U01HL123456. Like OrgStudyId, this is text without synonym expansion. It is indexed and searchable as part of the study IDs ￼.
* BriefTitle (text) – The short title of the study, as given by the study investigators. This is a single line title. Example: “A Study of XYZ for Treatment of Diabetes”. This field is searchable and, like other text, will undergo synonym/variant expansion by default (e.g. “Diabetes” could match “Diabetes Mellitus”). It’s an important field for general searches; by default, it’s included in broad search areas (like BasicSearch and ConditionSearch) with a moderate weight ￼.
* OfficialTitle (text) – The official scientific title of the study (often a longer, more detailed title). Example: “A Phase 3 Randomized, Double-Blind Study of XYZ Compound in Subjects with Type 2 Diabetes Mellitus”. This is also text and indexed for search (with synonyms expansion). It tends to have similar but slightly lower weight than BriefTitle in relevant search areas (since it’s longer and sometimes less succinct) ￼.
* Acronym (text) – A short acronym or abbreviation for the study, if provided. Example: SOLID-TIMI 52 (for a trial titled “The Stabilization of Plaques Using Darapladib”). Acronyms are searchable; if they coincide with common words, the search might treat them literally or expand them if known (e.g. “TIMI” is a specific study acronym – it probably wouldn’t expand as a word). Acronym may be considered in Title searches. Synonym expansion generally doesn’t apply unless the acronym itself is a known term.
* Condition (text) – A condition, disease, or problem studied by the trial. This field is populated by the sponsor and is not standardized (free-text entry), though sponsors often use medical terms. Example: Heart Attack or Myocardial Infarction. Conditions are a key search field; by default, condition terms are mapped to standard Medical Subject Headings (MeSH) terms behind the scenes. In the search index, the Condition field has a high weight (e.g. ~0.95 in the ConditionSearch area) because it’s very important for relevance ￼. Synonym and concept expansion do apply – for instance, searching “heart attack” will match studies whose Condition is “Myocardial Infarction” (the MeSH term), due to concept-level expansion ￼. Conversely, a search for “Myocardial Infarction” would also find “heart attack” if a study listed the lay term. (Ontology/Vocabulary: Sponsor-provided terms, often mapped to MeSH by the system for searching).
* ConditionMeshTerm (text) – A MeSH term corresponding to the condition, from the NLM’s Medical Subject Headings. Many studies have Browse Conditions which are standardized MeSH descriptors. Example: Myocardial Infarction (MeSH term for heart attack). This field is derived from the Condition field or assigned via indexing. It uses the controlled MeSH vocabulary, meaning terms come from a defined hierarchy. This field is used in searches (e.g., in ConditionSearch area) but often at a slightly lower weight than the raw Condition text. For example, ConditionSearch might weight ConditionMeshTerm around 0.5–0.8 relative to Condition’s 0.95 ￼ ￼. Synonyms: MeSH terms have entry terms and synonyms (e.g. “Heart Attack” is an entry term for Myocardial Infarction). The search engine’s concept expansion will ensure synonyms are matched, so ConditionMeshTerm also effectively matches lay synonyms of the MeSH term. (Ontology: NLM MeSH).
* ConditionAncestorTerm (text) – A higher-level MeSH category term for the condition. Each MeSH term belongs to a hierarchy; this field contains broader ancestor terms. Example: For condition “Myocardial Infarction”, an ancestor term might be Heart Diseases or Cardiovascular Diseases. This is a derived field (found in the Browse Condition module as MeSH categories) ￼. It may be indexed to allow more generic searches. Synonyms: since these are MeSH terms as well, standard synonym expansion applies. This field likely has a similar weight to ConditionMeshTerm (since it’s another way to match, albeit broader). (Ontology: MeSH hierarchy).
* Keyword (text) – Keywords provided by the study investigators. These are free-form terms meant to complement conditions, e.g. to tag studies with specific biomarkers, patient population characteristics, or informal terms. Example: STEMI or acute MI as keywords in a myocardial infarction study. Keywords are indexed as text with concept expansion, so synonyms are applied (e.g. “MI” would match “Myocardial Infarction” as a concept). In older search configurations, Keyword had a moderate weight (e.g. 0.6 in an obsolete ConditionSearch grouping) ￼. They can be useful for catching colloquial terms or related concepts not in the official Condition field.
* InterventionName (text) – The name of an intervention being studied. This could be a drug name, device name, behavioral therapy name, etc. Example: Aspirin or Losartan or FitBit®. This field is free-text but often corresponds to drug generic names or procedure names. It is a primary field in the InterventionSearch area and carries a high weight (expected to be similar to conditions in importance, around 0.9). Synonym expansion is applied. In particular, drug names may have synonyms (brand names vs generic, or common abbreviations). The search system can expand to those: e.g., searching “acetylsalicylic acid” would find studies where the Intervention Name is “Aspirin” (and vice versa), because those are known synonyms (UMLS links many drug names and their synonyms). There is also a MeSH equivalent: see below.
* InterventionType (enumeration) – The type/category of intervention. Controlled vocabulary with values like Drug, Device, Biological, Procedure, Behavioral, Dietary Supplement, Diagnostic Test, Radiation, Genetic and Other (and possibly a few others) as defined by ClinicalTrials.gov data elements. Example: Drug or Behavioral. This field is not typically used in free-text search queries (since it’s categorical), but one could filter by it through advanced search filters. If one were to search it, one would likely use exact terms (e.g. AREA[InterventionType] Drug). It’s enumerated and doesn’t have synonyms beyond its defined list. (Controlled vocabulary: ClinicalTrials.gov intervention categories).
* InterventionMeshTerm (text) – A MeSH term for the intervention (if available). Similar to ConditionMeshTerm, many interventions (especially drugs) have MeSH descriptors. Example: Acetylsalicylic Acid (the MeSH term for Aspirin). These come from the Browse Interventions provided for a study. They are standardized and part of the MeSH ontology. In searches, Intervention MeSH terms are indexed (likely somewhat lower weight than the raw InterventionName). Synonym expansion will cover entry terms (so a search for “Aspirin” could match a study whose InterventionMeshTerm is “Acetylsalicylic Acid”). (Ontology: MeSH).
* InterventionAncestorTerm (text) – Broader MeSH categories for interventions. For example, for Aspirin (Acetylsalicylic Acid), an ancestor might be Analgesics, Non-Narcotic. This field, if present, functions like ConditionAncestorTerm, allowing broader category matching. It’s derived from MeSH hierarchy. Typically lower weight, used for very general searches.
* PrimaryOutcomeMeasureTitle (text) – Title or brief description of a primary outcome measure. Studies list one or more primary outcome measures, each with a title and time frame (and sometimes description). Example: “Change in systolic blood pressure at 6 months”. This title is free text and indexed. It is the main part of the OutcomeSearch area. Synonyms will be applied (e.g. “systolic blood pressure” could match “SBP” if the system knows that abbreviation, or “6 months” might be considered a duration but likely not expanded). The weight for outcome titles is significant when using outcome-specific search, but generally a bit lower than conditions or interventions. If multiple outcomes exist, they’re all indexed (so a search term could match any primary outcome title in the study).
* SecondaryOutcomeMeasureTitle (text) – Title of a secondary outcome measure. Similar structure to primary outcome. Example: “Incidence of cardiovascular events”. These are also indexed (likely combined with primary outcomes in the search index or with slightly lower weight than primary). They provide additional points of match for outcome-related queries.
* OutcomeMeasureDescription (text) – Description/details of an outcome measure (if provided). This is usually a sentence or two explaining the measurement. It’s long-form text. Typically, this field would not be highly weighted in search (to avoid noise), but it may still be searchable. For most use cases, searching by outcome is done via titles rather than descriptions, unless specific keywords are only present in descriptions.
* OverallStatus (enumeration) – The overall recruitment status of the study. Controlled terms include values like Not yet recruiting, Recruiting, Active, not recruiting, Completed, Suspended, Terminated, Withdrawn, etc. ￼ ￼. This field is often used to filter studies (e.g., only show recruiting studies). In the API, it’s typically handled via filters rather than full-text query. However, you can search it in a query by specifying the exact status. E.g. AREA[OverallStatus] Recruiting will match studies currently recruiting subjects ￼. The field uses a fixed vocabulary (each status has an exact phrase). Example values: “Recruiting”, “Completed”. (These correspond to a defined status enumeration in ClinicalTrials.gov data model).
* Phase (enumeration) – Clinical trial phase. Possible values: Phase 1, Phase 2, Phase 3, Phase 4, plus combinations like Phase 1/Phase 2, and Early Phase 1, or N/A for trials without phases (like observational studies). This is controlled terminology. If searching by phase, one should use the exact phrase (e.g. AREA[Phase] "Phase 1"). This field might not be often directly searched via free text; more commonly, it’s a filter. But it is indexed (type is string enumeration). Example: “Phase 1”.
* StudyType (enumeration) – Indicates the type of study, e.g. Interventional, Observational, Observational [Patient Registry], or Expanded Access. This is a controlled field. Like Phase and Status, it’s usually used for filtering or faceting. Example value: “Interventional”. One could search it by AREA[StudyType] Interventional. No synonyms (fixed categories).
* Enrollment (number) – The target or actual enrollment number of participants. This is a numeric field. If searching for enrollment ranges, one would use the RANGE operator. For instance, AREA[Enrollment] RANGE[100, 1000] to find medium-sized studies. (In the data structure this may be split into EnrollmentCount and EnrollmentType, but generally the number is what one would query).
* Gender (enumeration) – Eligibility gender criterion. Values: All, Female, or Male. This specifies whether the study accepts all genders, or only females, or only males. It’s part of the Eligibility section. To use in a search query, one would likely do AREA[Gender] Female (for example) to find studies open only to females. In a combined “patient” query context, this can be important. No synonyms (just these three values).
* MinimumAge (numerical range with units) – The minimum age eligible for study participation. In the raw data, this is given as an age plus a unit (“Years”, “Months”, “Days”) or “N/A” if there is no minimum. In the modern API, this might be represented as a numeric value (perhaps in years or days) plus a unit. For searching, you can treat it as a number (the engine likely indexes an integer representing the age in years or an equivalent). For example, to find studies with min age &lt;= 18, one could use a range: AREA[MinimumAge] RANGE[MIN, 18 years]. If you want studies that include a specific age (say 65), you would ensure MinimumAge &lt;= 65 and MaximumAge >= 65 (see MaximumAge below). Example: “18 Years” (would be stored as 18 and unit “Years”). (Controlled values: typically an integer and one of the units “Years”, “Months”, etc., or “N/A”).
* MaximumAge (numerical range with units) – The maximum age eligible for study participation. Format similar to MinimumAge. “N/A (No limit)” is used if there’s no upper age limit. Searching usage: e.g., AREA[MaximumAge] RANGE[65 years, MAX] finds studies where max age is at least 65 (i.e., they allow 65-year-olds or older) ￼. If a study has no maximum (N/A), that likely is treated as an extremely high value or infinity for purposes of comparison. Example: “65 Years” or “N/A”.
* HealthyVolunteers (enumeration) – Indicates whether the study accepts healthy volunteers. Values: Yes or No. If “Yes”, people without the condition can participate; if “No”, the study is only for those with the condition under study. This is also a filter-type field. Example use: AREA[HealthyVolunteers] Yes to find studies open to healthy volunteers. Example value: “No”. (No synonyms, just yes/no).
* EligibilityCriteria (text) – The full text of the eligibility criteria (inclusion and exclusion criteria) for the study. This is a potentially long, unstructured field (often multiple paragraphs describing medical conditions, lab values, etc.). This field is indexed for search, but due to its length and detail, it’s usually not part of the default search areas for simple queries. However, it becomes important for very specific patient matching. If you use the PatientSearch area (see next section), criteria text might be searched for keywords. For example, if you search for AREA[EligibilityCriteria] "ejection fraction", you would find studies that mention “ejection fraction” in their inclusion/exclusion criteria. Synonym expansion does apply (medical concepts in criteria text will be recognized), but because of the length, matches here might be given lower weight to avoid overwhelming the relevance ranking with incidental mentions. Example snippet: “Inclusion Criteria: …males over 50 years old… Exclusion Criteria: …history of heart failure…”. (There is no controlled vocabulary; this is free text written by study investigators).
* LeadSponsorName (text) – Name of the lead sponsor organization (or individual) of the study ￼. This is usually a pharmaceutical company, university, or institute for interventional studies, or could be a person (investigator) in some cases. Example: National Heart, Lung, and Blood Institute (NHLBI). This field is searchable; it’s included in the Sponsor search area and has a high weight there (since if you search by sponsor name, you want exact matches). Synonyms: Generally, names are taken literally, though the search may handle acronyms (e.g. searching “NHLBI” would match the example above, since “NHLBI” appears in parentheses in the name). There is no formal ontology, but known acronyms or name variants might be recognized. (Note: There is also a LeadSponsorClass, see below).
* LeadSponsorClass (enumeration) – The type of lead sponsor (also known as Agency Class) ￼. Values are things like NIH, Industry, U.S. Fed (for U.S. federal agencies other than NIH), Other (for all other sponsors like universities or individuals) ￼ ￼. Example: “Industry” (for a pharmaceutical company sponsor), “NIH” (for a National Institutes of Health institute). This field could be used if one wanted to filter or search by sponsor type. E.g. AREA[LeadSponsorClass] NIH would find NIH-sponsored studies. It’s enumerated with a small set of possible values.
* CollaboratorName (text) – Names of collaborator organizations (if any). A study can list multiple collaborators (other organizations that provide support or funding). Example: American Heart Association. These names are also indexed. In the Sponsor search area, collaborator names are included but likely at slightly lower weight than the lead sponsor’s name. Otherwise, they behave similarly (literal string match, no special synonym expansion except handling acronyms).
* CollaboratorClass (enumeration) – The type of each collaborator (same categories as LeadSponsorClass: NIH, Industry, U.S. Fed, Other). Each collaborator has its own class. If multiple collaborators exist, they might not be aggregated in search – typically one would search collaborator names or filter by class indirectly. Not commonly used in queries directly.
* Facility/Location Fields: These fields describe the sites where the study is conducted:
* LocationFacility (text) – The name of the facility or center. Example: Massachusetts General Hospital. You can search by facility name (e.g., part of Location search). If one searches for a hospital name, this field would be matched. Synonyms: generally none, but the search will match partial names (and ignores punctuation).
* LocationCity (text) – City of the facility. Example: Boston. Searchable (as part of Location or via AREA[LocationCity]). No special synonyms (but concept expansion might allow small variations or treat “New York” and “NYC” similarly if known, etc.).
* LocationState (text) – State or province of the facility (if applicable). Example: Massachusetts. For US, states are full names (sometimes abbreviations are also present or recognized; e.g., “CA” vs “California”). The search likely treats state names as text (no synonyms except maybe common abbreviations could match the full name).
* LocationCountry (text) – Country of the facility. Example: United States. Countries are from a controlled list (usually full country names). Searching by country name is straightforward (you could also use filters). In queries, one might do AREA[LocationCountry] "United States" or simply include it in a Location search context.
* LocationZIP (text) – Postal code of the facility (for US locations). Example: 02114. This is text (digits). One can search by zip code by AREA[LocationZip] 02114. (Note: The modern API also supports a geo-spatial filter for locations, but that is done via a separate parameter rather than the query string).
* LocationStatus (enumeration) – Recruitment status of the study at that specific location. Values mirror OverallStatus, but per site, e.g. Recruiting, Active, not recruiting, etc. Example: “Recruiting”. In an advanced query, you can require a certain site status. For example, the query SEARCH[Location](AREA[LocationCountry] "United States" AND AREA[LocationStatus] Recruiting) finds studies with at least one U.S. location that is recruiting ￼. Usually, if one is interested only in recruiting studies, it’s easier to use OverallStatus or a filter; but specifying LocationStatus ensures that you have a recruiting site in a specific region, which can be a finer criterion.

These are by no means all fields in the data structure (there are many more, such as various dates – e.g. StudyStartDate, PrimaryCompletionDate, ResultsFirstPostDate – as well as detailed description fields, contacts, etc.), but the ones listed above are the most relevant for formulating search queries. Each of the above fields is considered searchable (Index Field) in the API ￼ ￼. Fields like MeSH terms and Ancestor terms derive from controlled vocabularies (MeSH), and fields like status, type, phase derive from controlled lists defined by ClinicalTrials.gov. Synonym expansion is primarily applied to text fields containing medical content (conditions, interventions, titles, keywords, criteria, etc.), leveraging sources like UMLS for concept mapping ￼. Enumerated fields and IDs do not use synonym expansion; they must match exactly one of the allowed values or codes.

Example field values and vocabularies in context: If a study is about heart attacks, you might see:

* Condition: “Heart Attack”
* ConditionMeshTerm: “Myocardial Infarction” (MeSH term) – the system knows these are equivalent concepts.
* ConditionAncestorTerm: “Cardiovascular Diseases” (MeSH category).
* InterventionName: “Aspirin”
* InterventionMeshTerm: “Acetylsalicylic Acid” (MeSH) – again a known synonym for aspirin.
* OverallStatus: “Recruiting” (controlled status list).
* Phase: “Phase 3”
* Gender: “Male” (if only males eligible, otherwise “All”).
* MinimumAge: “50 Years”
* MaximumAge: “80 Years”
* LeadSponsorName: “University of Example”
* LeadSponsorClass: “Other” (since it’s not Industry, NIH, or US Fed in this hypothetical).
* LocationCity: “Boston”
* LocationState: “Massachusetts”
* LocationCountry: “United States”
* LocationStatus: “Recruiting”

Understanding these fields and their types helps in crafting precise queries (e.g., knowing that you should quote multi-word phrases, or use RANGE for numeric fields, or that searching “MI” might find “Myocardial Infarction” because of the synonym system).

## Search Areas, Field Weights, and API Parameters

Search areas are predefined groupings of fields used by the ClinicalTrials.gov search engine to simplify querying common concepts. Each search area aggregates one or more study fields (from the list above) and assigns them weights for ranking. When you search within an area, all its fields are searched at once, with matches in higher-weight fields contributing more to relevance scoring. Below, we list the main search areas, the corresponding query parameter in the GET /studies API, the fields included, and their relative weights in that area.

* ConditionSearch – Param: query.cond (Condition or disease) ￼. This area is the default used when you enter terms in the “Condition or disease” field on the website. Fields & Weights: It searches primarily the condition-related fields. Specifically: Condition (weight ~0.95) ￼, BriefTitle (~0.60) ￼, OfficialTitle (~0.55) ￼, and ConditionMeshTerm (~0.5) ￼ – all as text with synonym expansion ✓. (In an older configuration, ConditionAncestorTerm and Keywords were also included, but in the modern configuration the titles appear instead for broader matching ￼ ￼.) This means a term in the Condition field contributes the most to relevance, but the query will also match that term in the study titles, albeit with lower weight. Example: Searching query.cond=heart+attack will return studies where “heart attack” appears in the Condition field most strongly, but also some where it’s only in the title (at lower rank).
* InterventionSearch – Param: query.intr (Intervention/treatment) ￼. Used for the “Intervention/treatment” search field. Fields & Weights: It covers intervention-related fields: InterventionName (high weight, ~0.9) and InterventionMeshTerm (lower weight, e.g. ~0.5–0.7). It may also include InterventionAncestorTerm if applicable. All are text with concept expansion (e.g., matching drug synonyms). This means searching an intervention will primarily hit the Intervention Name field (exact drug names) but will also match studies indexed with the corresponding MeSH terms. Example: query.intr=aspirin finds studies where aspirin is an intervention (with highest relevance if “Aspirin” is explicitly named as an intervention).
* OutcomeSearch – Param: query.outc (Outcome measures) ￼. Searches in the reported outcome measure titles. Fields & Weights: likely includes PrimaryOutcomeMeasureTitle (highest weight) and SecondaryOutcomeMeasureTitle (slightly lower weight). It might also search outcome measure descriptions to a small extent. All text with synonyms. Example: query.outc=mortality will find studies with an outcome measure related to “mortality” (e.g. “Overall survival at 1 year”), ranking primary outcomes higher.
* TitleSearch – Param: query.titles (Title/Acronym) ￼. Searches the study titles. Fields & Weights: BriefTitle and OfficialTitle (both highly weighted in this context), and Acronym. For instance, BriefTitle might be ~0.9, OfficialTitle ~0.8, Acronym ~0.7 in this area (roughly). All text with synonyms. This area is useful if you want to find a study by words in its title. Example: query.titles=vaccine finds studies with “vaccine” in their titles or acronyms.
* LocationSearch – Param: query.locn (Location) ￼. Searches facility location fields. Fields & Weights: LocationFacility (hospital/site name), LocationCity, LocationState/Province, LocationCountry, and possibly LocationZIP. Each is weighted such that more specific fields (facility, city) might have higher weight than broader ones (country). For example, the search area might weight Facility and City around 0.9, State around 0.7, Country around 0.5. Synonyms generally don’t apply (except that spelling variations or abbreviations of state/country might be recognized). This area allows queries like query.locn=Boston+Massachusetts to find studies with a location in Boston, MA. (Under the hood, that example would match “Boston” in city and “Massachusetts” in state). Important: Using SEARCH[Location] in an advanced query ties multiple terms to the same location record, whereas using the query.locn parameter (or a plain location search) will automatically handle city/state combinations appropriately ￼. Example: query.locn=Canada finds studies with locations in Canada.
* SponsorSearch – Param: query.spons (Sponsor/Collaborator) ￼. Searches sponsor and collaborator names. Fields & Weights: LeadSponsorName (highest weight) and CollaboratorName (lower weight). For example, in this area a match in LeadSponsorName might be weighted ~0.9 and in CollaboratorName ~0.7. This means if you search a company name, studies where that company is the lead sponsor will rank higher than studies where it’s just a collaborator. Example: query.spons="National Cancer Institute" will return studies sponsored or co-sponsored by NCI, with NCI-led studies first.
* LeadSponsorSearch – Param: query.lead (Lead Sponsor only) ￼. Specifically searches the Lead Sponsor Name field (and perhaps class). Fields & Weights: LeadSponsorName exclusively, likely at a very high weight (since it’s the only field). This is useful if you explicitly want only lead sponsor matches. Example: query.lead=Pfizer finds studies where Pfizer is the lead sponsor (not just a collaborator).
* StudyIdSearch – Param: query.id (Study identifiers) ￼. Searches various study ID fields. Fields & Weights: It includes NCTId, OrgStudyId, and SecondaryId. Likely, NCTId matches are given the highest weight (perhaps ~1.0, since an NCT match is very specific) and OrgStudyId slightly lower (0.9) and SecondaryId lower (0.7) ￼. A search by ID typically is an exact or near-exact match search (though it will treat the ID string as text). Example: query.id=NCT04292899 will directly find that specific study. A partial ID or grant number would also be found via this area.
* PatientSearch – Param: query.patient (Patient characteristics) ￼. This is a special area intended to help match based on patient attributes (a newer feature). Fields & Weights: It likely encompasses EligibilityCriteria text (with a low weight), and structured eligibility fields like Gender, MinimumAge, MaximumAge, and HealthyVolunteers. The idea is to allow searching with patient-related terms or filters. For instance, if you put query.patient="65 year old female", the system might interpret it as Female gender and age ~65. In practice, one would use range queries on age fields and direct matches on gender. The search engine might not automatically parse that sentence, so an advanced approach is: AREA[Gender] Female AND AREA[MinimumAge] RANGE[MIN,65 years] AND AREA[MaximumAge] RANGE[65 years, MAX] to find studies where a 65-year-old female would be eligible. In PatientSearch area, the weights might not be as relevant (since it’s more about filtering by criteria). However, concept terms in Criteria (like a comorbidity or biomarker) might be given some weight to rank studies where that criterion appears. Example: query.patient=melanoma+AND+Female could find studies that mention “melanoma” in criteria or conditions and are open to females. (Often, though, one would combine patient criteria with condition searches across areas for best results.)
* OtherTermsSearch – Param: query.term (Other terms) ￼ ￼. This is a broad catch-all search area historically used for the “Other terms” field on the website. It spans many fields not covered by the dedicated ones above. Fields & Weights: It can include parts of titles, descriptions, interventions, outcomes, sponsors – effectively a wide net. According to the documentation, the Other Terms field is used to narrow a search and you may enter things like a drug name, or an outcome, or an NCT number in it ￼. In the modern setting, query.term likely maps to what the BasicSearch covers. The BasicSearch area (the default all-fields search) consists of a large number of fields (about 58) ￼. This presumably includes: BriefTitle, OfficialTitle, Acronym, Keywords, PrimaryOutcomeTitle, SecondaryOutcomeTitle, LeadSponsorName, CollaboratorName, maybe Mesh terms, maybe criteria text, etc. Essentially, OtherTerms (BasicSearch) will find the query term anywhere in those many fields. The weights in BasicSearch vary: fields more central to a study’s identity (like title, conditions, interventions, sponsor names) have higher weights, whereas lengthy text fields (like descriptions or criteria) have lower weights to reduce their impact on ranking. For example, BasicSearch might weight BriefTitle ~0.7, OutcomeTitle ~0.6, SponsorName ~0.5, Keywords ~0.5, OfficialTitle ~0.4, BriefSummary (description) ~0.3, EligibilityCriteria ~0.2, etc (illustrative). The presence of a term in any of those will make the study a candidate, but those with the term in more critical fields rank higher ￼. Example: query.term=diabetes would search many fields for “diabetes”: conditions, titles, outcomes, etc. If a study has “diabetes” as a Condition, that will likely score higher than a study that only mentions “diabetes” in the description. If it’s in both, even better. (Note: In many cases, you might combine a Condition search and Other terms search for different concepts; e.g., Condition for disease and Other terms for a treatment or gene.)

In summary, the search areas correspond to the main facets of a study record one might be interested in. Each area has an associated query parameter in the API and a defined set of fields it searches (with certain weights). When writing an advanced query string (using the grammar described earlier), you can achieve the same targeting by using the SEARCH or AREA operators. But if you are using the API’s parameters directly, it may be simpler to put each part of your query into the appropriate parameter – the system will then apply the correct field groupings and weights automatically ￼ ￼.

For instance, using the API parameters:

* cond=heart+attack
* locn=Boston+Massachusetts
would internally search the ConditionSearch area for “heart attack” and the LocationSearch area for Boston & Massachusetts, respectively. This is equivalent to an advanced single-string query: heart attack AND SEARCH[Location](AREA[LocationCity]Boston AND AREA[LocationState]Massachusetts) as given in the documentation example ￼. Both approaches end up searching the same fields with the same weights and constraints.

Below is a quick reference mapping of search areas to fields and typical weights (✓ denotes that concept-based synonym expansion is applied):

* BasicSearch (All Fields) – Default used when no specific field is selected. Fields: ~58 fields covering most text (Title, Acronym, Summary, Conditions, Interventions, Outcomes, Keywords, Sponsors, etc.) ￼. Varied weights: Condition ≈0.8, Intervention ≈0.8, BriefTitle ≈0.7, Outcome titles ≈0.6, Sponsor names ≈0.5, Summary/Criteria ≈0.3 (roughly). ✓ Synonyms on all text fields.
* ConditionSearch (cond) – Fields: Condition (0.95)✓, BriefTitle (0.6)✓, OfficialTitle (0.55)✓, ConditionMeshTerm (0.5)✓ ￼.
* InterventionSearch (intr) – Fields: InterventionName (~0.9)✓, InterventionMeshTerm (~0.7)✓, (possibly InterventionAncestorTerm ~0.5✓).
* OutcomeSearch (outc) – Fields: PrimaryOutcomeMeasureTitle (~0.9)✓, SecondaryOutcomeMeasureTitle (~0.5–0.8)✓.
* TitleSearch (titles) – Fields: BriefTitle (~0.9)✓, OfficialTitle (~0.8)✓, Acronym (~0.7)✓ ￼.
* LocationSearch (locn) – Fields: Facility (0.9), City (0.8), State/Province (0.5), Country (0.3), Zip (0.3). (No synonym expansion needed – direct string match).
* SponsorSearch (spons) – Fields: LeadSponsorName (0.9)✓, CollaboratorName (0.7)✓.
* LeadSponsorSearch (lead) – Fields: LeadSponsorName (1.0)✓.
* StudyIdSearch (id) – Fields: NCTId (1.0), OrgStudyId (0.9), SecondaryId (0.7) ￼ (treated as text; usually an exact or near-exact match is required).
* Patient (Eligibility) Search (patient) – Fields: Gender, MinimumAge, MaximumAge, HealthyVolunteers, EligibilityCriteria. (Gender/HealthyVolunteers are exact matches; age uses numeric range logic; Criteria text is concept-expanded✓ for medical terms). Weighting in this area likely prioritizes structured fields (gender/age) for filtering, and uses criteria text matches only to rank within results when multiple studies meet the same basic filters.

(Note: The weights provided above are approximate and based on documentation snippets ￼ ￼ ￼ and logical inference. The ClinicalTrials.gov team can adjust these weights, but the general idea is that within each area, the most relevant field gets weight ~1.0 or 0.9, and supplementary fields get lower weights. The ✓ indicates fields where UMLS synonym/concept expansion is applied, which is most text fields ￼.)

By understanding these search areas and their composition, you can fine-tune queries to emphasize certain aspects. For example, placing a term in the condition parameter vs the other terms parameter will inherently give it more importance (weight) because of how the underlying fields are weighted ￼. If you need even more control, the advanced syntax with AREA[...] and SEARCH[...] can target specific fields or combinations directly.

## Examples of Complex Queries and Step-by-Step Explanations

Finally, let’s walk through some example queries to illustrate how to construct complex searches and what each part of the query accomplishes. We will use the syntax described above to demonstrate various features (field scoping, location grouping, range filtering, relevance biasing, etc.), and explain each query in plain language.

### Example 1: Condition with Specific Location

Query: heart attack AND SEARCH[Location](AREA[LocationCity] Bethesda AND AREA[LocationState] Maryland)

Explanation: This query finds studies related to heart attack that have a location in Bethesda, Maryland. It is composed of two parts joined by AND:

* heart attack – Without an explicit area, these terms will be searched in the default fields (BasicSearch). In practice, this will heavily match the Condition field (and Condition MeSH terms) for “heart attack” due to the weighting in ConditionSearch ￼. It will also match “heart attack” in titles or descriptions, but those are secondary. Essentially, we are looking for studies about heart attack (myocardial infarction).
* SEARCH[Location](AREA[LocationCity] Bethesda AND AREA[LocationState] Maryland) – This is a nested location context. It requires that at least one location (facility) of the study has City = Bethesda AND State = Maryland ￼. By grouping these in SEARCH[Location](...), we ensure both city and state criteria apply to the same location record. This part doesn’t specify anything about country, so it would match Bethesda, Maryland in any country that has such city/state (though in reality Bethesda, MD is in USA – and most likely the country is USA by implication).
* The AND between them means both conditions must hold: the study is about heart attack and has a site in Bethesda, MD.

In plain terms: “Find me studies that deal with heart attacks (myocardial infarction) that are being conducted in Bethesda, Maryland.” The first part ensures relevance to heart attack, the second part filters to studies available in that location.

This example shows field scoping (AREA[LocationCity] and AREA[LocationState]) and the use of SEARCH[Location] to tie those fields together in one site ￼. Without SEARCH[Location], a study that had “Bethesda” as a city for one site and “Maryland” as the state of another site would incorrectly match – but with the context, only studies with a Bethesda in Maryland qualify.

### Example 2: Multiple Location OR Query

Task: Compose a location query centered on Washington, DC, but also include surrounding areas like Fairfax, VA and Baltimore, MD.

Query: SEARCH[Location]((AREA[LocationCity] "Washington" AND AREA[LocationState] "District of Columbia") OR (AREA[LocationCity] "Fairfax" AND AREA[LocationState] "Virginia") OR (AREA[LocationCity] "Baltimore" AND AREA[LocationState] "Maryland"))

Explanation: This query finds studies that have a location in either Washington, D.C., or Fairfax, Virginia, or Baltimore, Maryland. Here’s the breakdown:

* We use one big SEARCH[Location]( ... ) block to handle the location criteria. This means we’re looking within each study’s locations for any site that matches any of the given city/state combos.
* Inside the parentheses, we have an OR combination of three location sub-expressions:
  * (AREA[LocationCity] "Washington" AND AREA[LocationState] "District of Columbia") – matches sites in Washington, DC. (We put quotes around “District of Columbia” since it’s a two-word state name.) This ensures city is Washington and state is DC for a single site.
  * (AREA[LocationCity] "Fairfax" AND AREA[LocationState] "Virginia") – matches sites in Fairfax, VA.
  * (AREA[LocationCity] "Baltimore" AND AREA[LocationState] "Maryland") – matches sites in Baltimore, MD.
* These three are joined by OR, so a study is included if any one of the three city/state pairs is present among its locations.
* The entire OR group is enclosed in the SEARCH[Location], so that each OR clause is evaluated per location record. Essentially, the study passes if it has at least one location in DC or Fairfax or Baltimore.

In plain language: “Find studies that have a trial site in Washington DC, or in Fairfax (VA), or in Baltimore (MD).” This would cover a DC-centric region, possibly of interest if a patient is willing to travel to any of those cities.

This example demonstrates combining multiple criteria with OR and grouping them. Each parenthesized (city AND state) ensures the two parts stick together, and the OR lets you list alternatives. Note that we could also include a country filter if needed (e.g., AREA[LocationCountry] United States for each, but since these city/state combos clearly imply USA, it’s optional).

Example 3: Using Relevance Scoring Operators

Scenario: Suppose we want to search for prostate cancer studies, but we want to favor more recent studies in the results. We can use the TILT scoring operator to bias by a date field (say, the Study First Posted date).

Query: TILT[StudyFirstPostDate] "prostate cancer"

Explanation: This query will retrieve studies matching “prostate cancer” (either in Condition or other relevant fields, due to concept expansion the engine will match “Prostatic Neoplasms” etc. as well). The addition of TILT[StudyFirstPostDate] in front doesn’t change which studies qualify – it still finds all studies about prostate cancer – but it adjusts the ranking score to favor those with more recent StudyFirstPostDate values ￼. That means studies that were posted more recently on ClinicalTrials.gov will appear higher in the list than they normally would, relative to older studies, if both are about equally relevant by content.

In effect: “Find prostate cancer studies, and rank newer ones higher.” This can be helpful if, for instance, you are more interested in current trials than those from many years ago, without outright filtering out the older ones.

We could combine TILT with other criteria. For example, TILT[StudyFirstPostDate] (prostate AND cancer AND NOT Phase 1) could find prostate cancer studies that aren’t phase 1, favoring recent ones. But the simple example above demonstrates the core idea: TILT[field] biases scoring by that field’s values (here, a date – newer = higher rank).

Another scoring-related operator is the expansion control. For example, searching EXPANSION[None] "heart failure" vs EXPANSION[Concept] "heart failure" can influence results. The latter (or default) will match studies indexed under “Cardiac Failure” or “Heart Failure, Congestive” synonyms, whereas EXPANSION[None] would only match the exact phrase “heart failure” ￼. Using these strategically can either widen or narrow your search with impact on relevance (concept matches get a slight penalty ￼, so exact matches still bubble up).

### Example 4: Complex Eligibility Criteria and Field-Weighted Query

Scenario: We have a patient who is a 65-year-old female with myocardial infarction (heart attack) as a condition, who also has diabetes. We want recruiting trials in her area (say Washington, DC). We also know that the condition (heart attack) is the main focus, so we want to weight that heavily in the search relative to the secondary factor (diabetes). We will construct an advanced query combining these pieces:

Query:
SEARCH[Condition] "myocardial infarction"
AND AREA[Keyword] diabetes
AND AREA[Gender] Female
AND AREA[MinimumAge] RANGE[MIN,65 years]
AND AREA[MaximumAge] RANGE[65 years,MAX]
AND AREA[OverallStatus] Recruiting 
AND SEARCH[Location]
     (AREA[LocationCity] "Washington" AND AREA[LocationState] "District of Columbia")
   )

(Line breaks added for readability; the actual query would be one line.)

Explanation: This looks complex, but we can break it down into logical parts:

* SEARCH[Condition] "myocardial infarction" – This restricts the phrase “myocardial infarction” to the Condition search area ￼. In other words, it’s looking for studies whose Condition (or related fields like condition MeSH) is “myocardial infarction” (heart attack). By doing this, we explicitly focus on the condition field with high weight. This is effectively up-weighting the condition: any match here is very influential on relevance (since Condition has weight 0.95 in that area) ￼. We used the formal medical term “myocardial infarction”, but we could have used “heart attack” – the search engine’s concept expansion would equate them. We put it in quotes to treat it as a phrase, ensuring the two words appear together in that order in the field.
* AND AREA[Keyword] diabetes – This requires that the word “diabetes” appear in the Keyword field of the study. We chose Keyword field for the secondary condition (diabetes) as an example; sometimes diabetes might also appear as a Condition or in Criteria, but by using Keyword we’re simulating that we want any mention of diabetes as a related term. The weight for Keyword is lower (about 0.6 in older config) ￼, so a match here will count but not override the main condition. In essence, this says “prefer studies that also mention diabetes (perhaps as a comorbidity or secondary focus).” If a study has “Diabetes” as a condition, it will actually also match via Condition field – but since our main condition is myocardial infarction, we use Keyword to represent the comorbidity. If a study has diabetes only in criteria, it wouldn’t be caught by this unless keywords or conditions include it. We could alternatively use AREA[EligibilityCriteria] diabetes, but that could yield too many loose matches. Using Keyword is a controlled way (assuming some studies might tag common comorbidities in keywords).
* AND AREA[Gender] Female – Ensures the study accepts female participants. This directly checks the Gender eligibility field for “Female”. If a study is gender-specific to males, this filter will exclude it. If Gender is “All”, this condition will not be satisfied (since “All” is not “Female”). If we wanted to include studies open to all as well, we could do something like AREA[Gender] (Female OR All), but in our scenario, perhaps we specifically need female-only studies (or we assume maybe the patient’s condition might be sex-specific – though heart attacks are not sex-specific, so maybe we should allow All; but let’s stick with the example as given).
* AND AREA[MinimumAge] RANGE[MIN,65 years] AND AREA[MaximumAge] RANGE[65,MAX years] – These two together ensure the patient’s age 65 falls within the study’s age eligibility range.
* AREA[MinimumAge] RANGE[MIN,65 years] means the minimum age is &lt;= 65 ￼.
* AREA[MaximumAge] RANGE[65 years,MAX] means the maximum age is >= 65 (or no maximum) ￼.
So if a study is for ages 40 and up (min 40, no max), it passes (min 40 ≤65 and max = N/A which we treat as ∞ ≥65). If a study is for ages 18-64, it would fail the second part because max 64 is &lt; 65. If a study is 65 and above only, it fails the first part if min is 65 (actually if min = 65, range[MIN,65 years] includes 65, so that passes; if min was 66, it fails). So effectively we’re filtering to studies that allow 65-year-olds.
This showcases numeric range filtering on age fields. These fields are numeric internally, even if originally entered as text like “65 Years”.
* AND AREA[OverallStatus] Recruiting – Filters to studies that are currently recruiting participants. We target the OverallStatus field for “Recruiting” ￼. Only studies actively recruiting will satisfy this. This is important in a real scenario to find open trials.
* AND SEARCH[Location]((AREA[LocationCity] "Washington" AND AREA[LocationState] "District of Columbia")) – Finally, we restrict to trials with a location in Washington, DC. This uses the same pattern as earlier examples: the location search context with city and state. We only put one city/state here (Washington/DC). We could include surrounding cities with OR as shown before, but let’s assume the patient only wants DC proper. This will ensure the study has at least one recruiting site in DC (implicitly, since we combined with Recruiting status overall, one might also ensure the site is recruiting; however, OverallStatus=Recruiting usually means at least one site is recruiting, but not necessarily in DC – a subtle point. If we wanted to be very strict that the DC location is recruiting, we would include AREA[LocationStatus] Recruiting inside the SEARCH[Location] block too. E.g., SEARCH[Location](AREA[LocationCity]Washington AND AREA[LocationState]District of Columbia AND AREA[LocationStatus]Recruiting). For simplicity, we’ve assumed overall recruiting and location presence in DC.)

Putting it all together: this query finds studies where:

* Condition = myocardial infarction (heart attack) – highly weighted in relevance ￼.
* Preferably they mention diabetes as well (likely as a keyword or secondary condition) – that will boost those that do, but it’s an AND so actually it requires it. So we made it required in this query (AND Keyword diabetes means studies must have “diabetes” in keywords). If we wanted to merely boost but not require diabetes, we could do something clever like an OR with bias, but the query language doesn’t have a direct boost except making it optional. Alternatively, we could remove the AND and rely on synonyms or separate search. But for demonstration, we’ve required it, meaning we’re looking for trials that address heart attack and diabetes together (which might be a narrower set).
* Only female participants, age 65 allowed.
* Trials must be recruiting.
* Trials must have a location in Washington, DC.

This is a very specific query. Conceptually, it’s doing a form of patient-trial matching:
“Find recruiting studies for 65-year-old female patients with myocardial infarction, that also involve diabetes (perhaps as a comorbidity or focus), available in Washington, DC.”

Because we used SEARCH[Condition] for the main condition, the search engine will give a lot of weight to matches on “myocardial infarction” in the Condition field ￼. Using the medical term ensures we catch studies where that is the official condition. The diabetes requirement might be a bit strict – if no study lists diabetes explicitly, that AND would yield no results. We could relax it by doing an OR or using EXPANSION[Concept] on criteria text. For instance, we could alternatively search criteria for diabetes like:

… AND (AREA[Keyword] diabetes OR AREA[EligibilityCriteria] diabetes)

to allow matches in either field. But then we’d want to not eliminate studies lacking it, maybe just score them lower. Achieving an optional criterion in the query string is tricky since the language inherently treats terms as required unless OR’d. We could OR the whole diabetes part with something like OR NOT diabetes in criteria, but that’s not straightforward.

In practice, one might issue a broader query and then post-filter or examine results. However, for an AI agent tasked with querying, one strategy is to run multiple queries or adjust weighting via separate area usage. Since the question specifically asked to show the ability to adjust relevance by up-weighting condition, we did that by isolating the condition in its own area search. If we wanted diabetes to be a softer criterion, we might omit it from the query but rather include it as a term in a different area param (like query.term). But given the query language, every term in an AND sequence is required. The scoring weight will matter if many studies meet all criteria; among them, those with more relevance (like containing the terms in more important fields, or multiple occurrences) will rank higher.

Relevance adjustment note: In the above query, “myocardial infarction” is in the Condition area (very high weight) while “diabetes” is only required in the keyword (moderate weight). So any study that doesn’t mention diabetes at all is excluded, but those that do are all considered. Within those, what if one study has diabetes as a condition vs another just in keyword? The one with diabetes as a condition would actually have it also in Condition field, which wasn’t directly searched by that term (we searched condition for MI specifically). However, if a study lists both MI and diabetes as conditions, our query would catch MI via condition and diabetes via keyword (assuming they also repeated diabetes in keyword or criteria; if not, that study might be missed if it didn’t list diabetes in keyword – a limitation of our strict structure).

One might approach this differently by doing: SEARCH[Condition]("myocardial infarction" OR diabetes) but then that would find studies whose condition is diabetes alone or MI alone or both, which is too broad and not exactly our patient profile. We specifically wanted MI + diabetes. That kind of combination query can be done by requiring MI in Condition and allowing diabetes in either condition or keywords. We did keyword.

In summary, the query above is illustrative of combining multiple factors:

* SEARCH[...] to focus on a particular facet with high weight,
* field-specific AREA[...] to apply filters (age, gender, status, location),
* and by the structure of the query, we inherently “up-weighted” the MI condition because of how the search area weights work. We didn’t explicitly do something like ^2 boost (the language doesn’t use that syntax), but effectively, any matches on the condition “myocardial infarction” are much more influential than matches on the word “diabetes” in keywords due to the weighting scheme ￼ ￼. So studies truly focused on MI will rank on top, while among those, having diabetes mentioned is just a requirement we set (not a booster in this case).

If we wanted to adjust relevance without strict exclusion for a factor, we’d use OR to make it optional and rely on weight. For example, say we wanted to find MI studies and “boost if diabetes is mentioned but not strictly require it”. We could do:

SEARCH[Condition] "myocardial infarction"
AND AREA[Gender] Female AND ... (other filters) ... AND AREA[OverallStatus] Recruiting
AND SEARCH[Location]( ... DC ...)
AND (AREA[Keyword] diabetes OR ALL)

This way, the OR ALL makes the clause always true, effectively not filtering anything out, but it will still impact scoring because a match in Keyword diabetes will differentiate some records. However, writing OR ALL is a hack to allow an optional term. A more intended method might be using expansion or just doing two separate searches. But this shows how one might try to incorporate an optional term in a single query (with ALL acting as a neutral pass-through for the OR) ￼.

For clarity, our example kept it required. It demonstrates using multiple AND criteria.

## Addendum: Importance of REST API Parameters in Relevancy Searching

When using the ClinicalTrials.gov REST API, the choice of parameters significantly influences both which studies are returned and how they are ranked by relevance. In addition to the core query parameters (e.g., query.cond, query.intr, query.locn), the API provides mechanisms such as filters and postfilters that alter the inclusion and scoring of results.

### 1. Filters (Pre-Search Constraints)

Filters act as hard constraints on the search. When you apply a filter (e.g., filter.overall_status=Recruiting or filter.phase=Phase 3), only studies meeting those criteria are included in the result set. This step occurs before relevancy scoring, meaning irrelevant records are excluded outright rather than being scored lower.

Impact on Relevance:

* Filters reduce the candidate pool, so the scoring engine only ranks studies that meet the exact filter criteria.
* This ensures efficiency and precision, but it also means potentially relevant studies outside the filter scope (e.g., Phase 2 trials when filtering for Phase 3) will not be considered at all.
* Best practice: use filters when you want categorical exclusion (e.g., phase, status, age ranges).

Example:

/studies?query.cond=lung+cancer&filter.overall_status=Recruiting

This query returns only recruiting studies about lung cancer. Non-recruiting trials are excluded entirely and cannot appear in the results.

⸻

### 2. Postfilters (Re-Scoring Adjustments)

Postfilters differ from filters in that they adjust ranking and scoring after the main search results are retrieved, rather than eliminating studies outright. They allow you to bias the relevance of results toward or away from certain values without removing them from the candidate set.

Impact on Relevance:

* Postfilters apply additional weighting to studies that match specific criteria, effectively boosting or penalizing their rank in the results.
* Unlike filters, they do not exclude studies; they simply alter ordering.
* This is particularly important for nuanced relevance ranking, where you want broader inclusivity but prefer some matches over others.

Example:

/studies?query.cond=diabetes&postfilter.lead_sponsor_class=Industry

This query retrieves all diabetes studies, but those sponsored by industry receive a score boost and will rank higher in the results.

⸻

### 3. Combining Filters and Postfilters

For maximum precision, filters and postfilters are often used together:

* Filters define strict eligibility boundaries.
* Postfilters bias results within that filtered set.

Example (patient-centric search):

/studies?query.cond=breast+cancer&filter.overall_status=Recruiting&postfilter.study_first_post_date=recent

* filter.overall_status=Recruiting ensures only actively recruiting studies are returned.
* postfilter.study_first_post_date=recent tilts ranking toward newly posted studies, helping ensure patients see the most current opportunities.

⸻

### 4. Practical Implications for Relevance Searching

* Filters = precision control → use them to enforce must-have constraints.
* Postfilters = ranking control → use them to guide prioritization of certain studies without excluding others.
* Together, they allow an API consumer to balance inclusivity with fine-grained relevance scoring.
* When building AI-driven agents for clinical trial matching, filters are best suited for patient eligibility requirements (e.g., age, status, phase), while postfilters are best for tuning search results to user preferences (e.g., recency, sponsor type, trial size).

⸻

Summary

Filters and postfilters are critical in shaping the outcome of a ClinicalTrials.gov REST API search:

* Filters act as hard gates that restrict results before scoring.
* Postfilters adjust relevance scores to favor certain attributes.
* Used together, they enable precise, patient-centered, and context-sensitive search strategies that go beyond simple keyword matching.