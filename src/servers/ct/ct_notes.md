# Clinical trial server implementation notes

## Creation of essie_gpt.md

### Prompt

* Sent to GPT-5 thinking with deep research. Deep research was used to try and fill
  in the holes in the specs.

```md
Examine the following documents and any others you feel relevant to construct a markdown explanation of the clinical trials search queries
https://clinicaltrials.gov/find-studies/constructing-complex-search-queries#search-terms
https://clinicaltrials.gov/data-api/about-api/search-areas
https://clinicaltrials.gov/data-api/about-api/study-data-structure

Think hard and create your own understanding of the structure of the queries as the documents are not well organized and may be incomplete. The purpose of the document will be to give an AI agent enough information to flexibly search the get /studies endpoint for relevant clinical studies given a patient's records.

To begin, create a detailed BNF that explains how to compose a search query. The BNF should include precedence.

For each element of the BNF, explain what it is and how to compose various useful subexpressions including order of precedence. This should include an operator-by-operator discussion of boolean, context, grouping, source, and scoring operators.  It should also explain search terms, search expressions, source expressions, and range expressions. The BNF should distinguish between search areas and study structure fields.

Then create a list of study structure fields (also called data fields), their type, if the field has synonyms, enumeration values if available and a description of the field. The description should reference any ontologies or controlled vocabularies used. Show an example value for the field.

Then create a list of search areas. For each search area, list the corresponding RESTful parameter for the get /studies endpoint if available, the corresponding study structure fields in the search area and their corresponding weight.

Give a list of example queries and use the above explanation to show what the query is accomplishing step by step. For example, what does the query heart attack AND SEARCH[Location](AREA[LocationCity] Bethesda AND AREA[LocationState] Maryland) mean precisely? Or, for example, how to compose a location query centered on Washington DC but extends to Fairfax, VA and Baltimore, MD. Or detailed examples that show how to compose a query with relevance scoring using different field weighting if possible. Finally, create an example that searches for relevant clinical trials  using a patient's age, sex, condition, keywords, the clinical trial's status and location with the ability to adjust the relevance, e.g. upweighting the condition field.

This specification should be optimized for use by LLMs. The BNF should not include the JSON expected by the REST API. The specification should not be tailored to a particular medical domain.
```

* GPT didn't create a markdown doc, so had to cut and paste and do some
  light editing to make the doc markdown format
* The intro and conclusion were edited out
* added " years" to ages in RANGE[] queries
* added an addendum on the filters and postfilters using the prompt:

```md
Please create an addendum to this file that discusses the importance of the REST API parameters in doing relevancy searching, e.g. how do filters and postfilter affect the searching and scoring
```

## Pydantic model adjustments

* in pydantic, Optional means that a field can be set to None. When creating/reading
  in a pydantic BaseModel, the optional fields are automatically set to None,
  so when writing out the BaseModel, all of those fields are output with a value of 
  null. So input != output. Since all of these null fields fill up LLM context,
  we added a prune_nulls option to each tool in the ToolFactory that will prune
  out all nulls in the output. This option is on by default. One minus of this is 
  that if an field is set to null on input, it won't be on output.

## ctg-oas-v2.yaml OpenAPI spec

* added default value to /studies fields parameter
* changed default value of includeIndexedOnly to true for metadata endpoint

Error executing tool fetch_study: 2 validation errors for FetchStudyResponse
protocolSection.statusModule.studyFirstPostDateStruct.date
  Input should be None [type=none_required, input_value='2009-02-11', input_type=str]
    For further information visit https://errors.pydantic.dev/2.11/v/none_required
protocolSection.statusModule.lastUpdatePostDateStruct.date
  Input should be None [type=none_required, input_value='2009-02-11', input_type=str]
    For further information visit https://errors.pydantic.dev/2.11/v/none_required
