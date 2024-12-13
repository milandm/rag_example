from string import Template


# system messages describe the behavior of the AI assistant. A useful system message for data science use cases is "You are a helpful assistant who understands data science."
# user messages describe what you want the AI assistant to say. We'll cover examples of user messages throughout this tutorial
# assistant messages describe previous responses in the conversation. We'll cover how to have an interactive conversation in later tasks


question_template = """
QUESTION: {question}
=========
=========
ANSWER:

"""


combine_template = """
PREVIOUS:
{previous}

Da li si siguran da ANSWER sadrzi sve informacije koje se pominju u dokumentaciji vezano za QUESTION.
Kompletan odgovor treba da bude u dole zadatom formatu:

```
QUESTION: <the question>
=========
<Source of information 1>
...
<Source of information N>
=========
ANSWER: <you provide your answer here. Always use bullet points.>

SOURCES: <list the sources used from those provided above>
```

"""


synopsis_template = """

Ti si ekspert za zakone u oblasti klinickih istrazivanja.
Tvoj zadatak je da pruzis informacije iz datih izvora.
Treba da navedes dokument u kom si pronasao odgovor.
Odgovor treba da bude u dole zadatom formatu:

```
QUESTION: <the question>
=========
<Source of information 1>
...
<Source of information N>
=========
ANSWER: <you provide your answer here. Always use bullet points.>

SOURCES: <list the sources used from those provided above>
```

QUESTION: {question}
=========
{summaries}
=========
ANSWER:"""


combine_template = """
PREVIOUS:
{previous}

Da li si siguran da PREVIOUS sadrzi sve informacije koje se pominju u dokumentaciji vezano za QUESTION.
Kompletan odgovor treba da bude u dole zadatom formatu:

```
QUESTION: <the question>
=========
<Source of information 1>
...
<Source of information N>
=========
{summaries}
=========
ANSWER: <you provide your answer here. Always use bullet points.>

SOURCES: <list the sources used from those provided above>
```

"""






QUESTION_PROMPT_TEMPLATE = """
        You propose closest meaning sentences : $question

        Cite them in your answer.

        References:

        $references

        \nHow to cite a reference: This is a citation [1]. This one too [3]. And this is sentence with many citations [2][3].\nAnswer:
        """

RECOMMEND_PROMPT_TEMPLATE = """
        You propose closest meaning sentences : $questions

        Cite them in your answer.

        References:

        $references

        \nHow to cite a reference: This is a citation [1]. This one too [3]. And this is sentence with many citations [2][3].\nAnswer:
        """




SYSTEM_MSG_EXPERT = """

Ti si ekspert za zakone u oblasti klinickih istrazivanja.
Tvoj zadatak je da pruzis informacije iz datih izvora.
Treba da navedes dokument u kom si pronasao odgovor.
Odgovor treba da bude u dole zadatom formatu:

```
RESULT: {
    "question": <the question>,
    "answer": <you provide your answer here. Always use bullet points.>,
    "sources": [
        <list the sources used from those provided above>
        <Source of information 1>,
        ...
        <Source of information N>
    ]}
```
"""

SYSTEM_MSG_COMPLIANCE = """
You are doing background check for given personal data.
"""

SYSTEM_MSG_TITLE = """
You are someone who check and validate certificates for companies
"""

TITLE_EXTRACT_KEY = "TITLE:"

CERTIFICATE_DATA_EXTRACT_KEY = "EXPORT:"

DOCUMENT_EXTRACTION_EVALUATION_V1 = """
OCR_DOCUMENT_EXTRACTION: ocr_document_extraction

DI_DOCUMENT_EXTRACTION: di_document_extraction

Please, compare OCR_DOCUMENT_EXTRACTION "pdf_loaded" and "ocr_loaded" vs  DI_DOCUMENT_EXTRACTION "documents_content",
please enlist if some of these fields missed something compared to each other.

Please compare OCR_DOCUMENT_EXTRACTION and DI_DOCUMENT_EXTRACTION corresponding fields one by one,
and enlist if there is any difference, entitle which EXTRACTION contains more accurate field value.

Both extractions should contain these values:

"certification_authority",
"certificate_type",
"certification_date_valid_from",
"certification_date_valid_to",
"company_name",
"company_address",
"expiration_date",
"material_group",
"all_important_fields",
"official_company_name"

If EXTRACTION doesn't contain some of these value please mark this extraction as FAILED,
and please explain which value is not EXTRACTED and explain why. 

Export should contain these values:
- best_content_extraction -  OCR_DOCUMENT_EXTRACTION "pdf_loaded" and "ocr_loaded" content vs DI_DOCUMENT_EXTRACTION "documents_content" content which is better
- ocr_missing_info - OCR_DOCUMENT_EXTRACTION "pdf_loaded" and "ocr_loaded" content missing information list compare to DI_DOCUMENT_EXTRACTION "documents_content" content
- di_missing_info - DI_DOCUMENT_EXTRACTION "documents_content" content missing information list compared to OCR_DOCUMENT_EXTRACTION "pdf_loaded" and "ocr_loaded" content
- ocr_failed_fields - list of extraction failed fields in OCR_DOCUMENT_EXTRACTION 
- di_failed_fields - list of extraction failed fields in DI_DOCUMENT_EXTRACTION
- ocr_succeed - all fields are extracted successfully True of False 
- di_succeed - all fields are extracted successfully True of False 
- explanation - if ocr_succeed or di_succeed is False, this field should contain explanation, why

Export should be formatted as:
EXPORT:
{
    "best_content_extraction": "some_value",
    "ocr_missing_info": "some_value",
    "di_missing_info": "some_value",
    "ocr_failed_fields": "some_value",
    "di_failed_fields": "some_value",
    "ocr_succeed": "some_value",
    "di_succeed": "some_value",
    "explanation": "some_value"
}

"""


EXTRACT_CERTIFICATE_DATA_V1 = """
DOCUMENT_CONTENT: $document_content

From DOCUMENT_CONTENT extract fields: 
- certification_authority- certification authority
- certificate_type- certificate type
- certification_date_valid_from- certification date valid from 
- certification_date_valid_to- certification date valid to
- company_name - company name
- company_address - company address
- expiration_date - expiration date

Export should be formatted as:
EXPORT:
{
    "certification_authority": certification authority value
    "certificate_type": certificate type value
    "certification_date_valid_from": certification date valid from value
    "certification_date_valid_to": certification date valid to value
    "company_name": company name value
    "company_address": company address value
    "expiration_date": expiration date value
}

"""

EXTRACT_CERTIFICATE_DATA_V2 = """

CERTIFICATE_SCOPE_LIST: $certificate_scope_list

CERTIFICATE_DOCUMENT_CONTENT: $document_content

From CERTIFICATE_DOCUMENT_CONTENT extract fields: 
- certification_authority- certification authority
- certificate_type- certificate type
- certification_date_valid_from- certification date valid from 
- certification_date_valid_to- certification date valid to
- company_name - company name
- company_address - company address
- expiration_date - expiration date
- material_group - certificate scope, if CERTIFICATE_DOCUMENT_CONTENT scope is close to any scope label from CERTIFICATE_SCOPE_LIST, please add that scope label value to material_group field 

- all_important_fields - key value dictionary of all string sequences in the DOCUMENT_CONTENT that could refer to some important information as label and that value





Export should be formatted as:
EXPORT:
{
    "certification_authority": certification authority value
    "certificate_type": certificate type value
    "certification_date_valid_from": certification date valid from value
    "certification_date_valid_to": certification date valid to value
    "company_name": company name value
    "company_address": company address value
    "expiration_date": expiration date value
    "material_group": material group value
    "all_important_fields": all important fields label and value dict
}

"""


# social media info and news articles info
ENRICH_DNB_DATA_TEMPLATE = """
Could you find all relevant public data related exactly to person with given personal data: 
SCREENING_PERSONAL_DATA: $screening_personal_data

Please try to find as much as possible additional info about given person, 
taking in account:
    - persons name and sure name with highest priority
    - company that person is working for with next highest priority
    - persons birthday with next highest priority
    - rest of given data

!!! It is mandatory to PROVIDE SOURCE for every information you found !!!

At the end of response, please provide links to sources where you obtained information

"""



# social media info and news articles info
SCREENING_PERSONAL_DATA_TEMPLATE = """
Could you find all relevant public data related exactly to person with given personal data: 
SCREENING_PERSONAL_DATA: $screening_personal_data

Please provide info about persons that could be possibly associated with requested person by mistake,
based on SCREENING_PERSONAL_DATA and public data that you can find related to these persons.

!!! It is mandatory to PROVIDE SOURCE for every information you found !!!

At the end of response, please provide links to sources where you obtained information

"""


# social media info and news articles info
PERSONAL_DATA_INCONSISTENCIES_COMPARISON_TEMPLATE  = """

SCREENING_PERSON: $screening_personal_data

This is list of individuals with high risk that could be potentially associated with SCREENING_PERSON.
POTENTIAL_MATCHES_DATA_LIST:$potential_matches

To find discrepancies within the SCREENING_PERSON information provided and individuals from POTENTIAL_MATCHES_DATA_LIST,
please check these:

Personal Information Discrepancies:

    Name Variations: Check for inconsistencies in spellings, use of aliases, or middle names across different documents.
    Date of Birth Mismatches: Verify that the date of birth is consistent and aligns with the individual's educational and professional timelines.
    Nationality/Citizenship: Ensure the nationality or citizenship information matches official records and public data.

Educational Background:

    Timeline Consistency: Confirm that the years of education are plausible given the person's date of birth.
    Accredited Institutions: Verify that degrees and certifications are from recognized and accredited institutions.
    Overlapping Dates: Look for any overlapping education or employment dates that may indicate discrepancies.

Professional Experience:

    Occupation vs. Risk Indicators: Assess whether the individual's high-reputation occupation is inconsistent with any associated criminal records or risk types.
    Employment History Verification: Cross-check previous employers, job titles, and durations for accuracy.
    Unexplained Career Gaps: Identify any unexplained periods in the professional timeline that may require further investigation.

Criminal and Legal Records:

    Severity Alignment: Check if any minor offenses or petty criminal records conflict with the individual's professional stature.
    Undisclosed Legal Issues: Search for any legal actions, sanctions, or regulatory penalties not disclosed by the individual.
    Consistency with Risk Type: Ensure that any identified risks are consistent with the individual's profile and background.

Financial and Regulatory Compliance:

    Sanctions and Watchlists: Verify that the individual is not listed on any financial sanctions lists or government watchlists inconsistent with their provided information.
    Licensing and Certifications: Ensure all professional licenses and certifications are valid, current, and match official records.
    Financial Red Flags: Look for signs of bankruptcy, tax evasion, or unusual financial activities that are inconsistent with the individual's profile.

Digital Footprint:

    Online Profiles Consistency: Compare information from social media and professional networks like LinkedIn with the provided data to identify any discrepancies.
    Negative Online Presence: Search for adverse media, negative news articles, or publications that conflict with the individual's claimed reputation or associations.
    Absence of Expected Presence: Note if there is a lack of online presence where one would be expected for someone in their position.

Document Examination:

    Authenticity Checks: Inspect provided documents for signs of tampering, forgery, or alterations.
    Consistent Details: Ensure that document numbers, issue dates, and issuing authorities are correct and match across all documents.
    Unusual Issuing Authorities: Be cautious of documents issued by non-recognized or suspicious authorities.

!!! It is mandatory to PROVIDE SOURCE for every information you found !!!    
    
At the end of response, please provide links to sources where you obtained information    
    
Output should contain compared info and inconsistency explanation:
    
Output: JSON object with the following structure:            
    {
        screened_occupation: "some occupation",
        potential_match_risk_type: "some risk type"
        occupation_risk_type_discrepancy_explanation: "some explanation",
        screened_birthday: "some birthday",
        potential_match_years_of_education: "some years of education"
        birthday_years_of_education_discrepancy_explanation: "some explanation",
        ....,
        sources_list: []
    }
"""



# social media info and news articles info
SCREENING_PERSONAL_DATA_COMPARISON_TEMPLATE = """

SCREENING_PERSON: $screening_personal_data

This is list of individuals with high risk that could be potentially associated with SCREENING_PERSON.
POTENTIAL_MATCHES_DATA_LIST:$potential_matches

To validate and verify the information provided for SCREENING_PERSON follow these steps:

1. **Verify Company Information:**
   - **Company Name:**
   - **DUNS Number:** 
   - **Address:** 
   - **Website:** 
   - **Registration Numbers:** 

2. **Verify Personal Information:**
   - **Full Name:** 
   - **Residence Country:** 
   - **Company Association:** 

3. **Cross-Reference Public Data:**
   - Search for SCREENING_PERSON in public databases, news articles, and professional networks like LinkedIn to confirm her association with SAP SE.
   - Check for any public records or press releases from **Company Name:** that mention **Full Name:**.

4. **Identify Potential Confusions:**
   - **Name Similarities:** Look for other individuals similar to SCREENING_PERSON who might be associated with different companies or industries.
   - **Company Confusions:** Ensure there are no other companies with similar names or addresses that might cause confusion.

5. **Public Data Sources:**
   - **Business Registries:** Check business registries for any discrepancies in the registration numbers or company details.
   - **Professional Networks:** Verify professional profile on platforms like LinkedIn to confirm role and association with **Company Name:**.
   - **News and Publications:** Search for any news articles or publications that mention SCREENING_PERSON in relation to **Company Name:**.

6. **Potential Misassociations:**
   - If there are other individuals named as **Full Name:**, they might be associated with different companies or industries. 
   Verify their details to ensure they are not mistakenly associated with **Company Name:**.
   - Check for any public records or databases that might list multiple individuals with the same name but different professional backgrounds.

By following these steps,you aim to confirm the identity and association of SCREENING_PERSON with **Company Name:** and identify any potential misassociations with other individuals.

Please enlist all individuals from  POTENTIAL_MATCHES_DATA_LIST with high possibility of matching SCREENING_PERSON.

!!! It is mandatory to PROVIDE SOURCE for every information you found !!!

At the end of response, please provide links to sources where you obtained information

"""



# social media info and news articles info
SCREENING_PERSONAL_SEARCH_MORE_TEMPLATE = """

For this:

SCREENING_PERSON: $screening_personal_data

Please search available public data for another individuals with similar name and personal data,
that could possibly be associated to this person:

1. **Verify Company Information:**
   - **Company Name:**
   - **DUNS Number:** 
   - **Address:** 
   - **Website:** 
   - **Registration Numbers:** 

2. **Verify Personal Information:**
   - **Full Name:** 
   - **Residence Country:** 
   - **Company Association:** 

3. **Cross-Reference Public Data:**
   - Search for SCREENING_PERSON in public databases, news articles, and professional networks like LinkedIn to confirm her association with **Company Name:**.
   - Check for any public records or press releases from **Company Name:** that mention **Full Name:**.

4. **Identify Potential Confusions:**
   - **Name Similarities:** Look for other individuals similar to SCREENING_PERSON who might be associated with different companies or industries.
   - **Company Confusions:** Ensure there are no other companies with similar names or addresses that might cause confusion.

5. **Public Data Sources:**
   - **Business Registries:** Check business registries for any discrepancies in the registration numbers or company details.
   - **Professional Networks:** Verify professional profile on platforms like LinkedIn to confirm role and association with **Company Name:**.
   - **News and Publications:** Search for any news articles or publications that mention SCREENING_PERSON in relation to **Company Name:**.

6. **Potential Misassociations:**
   - If there are other individuals named as **Full Name:**, they might be associated with different companies or industries. 
   Verify their details to ensure they are not mistakenly associated with **Company Name:**.
   - Check for any public records or databases that might list multiple individuals with the same name but different professional backgrounds.

By following these steps, you aim to confirm the identity and association of SCREENING_PERSON with **Company Name:** and identify any potential misassociations with other individuals.

Please enlist all individuals with high possibility of matching SCREENING_PERSON.

!!! It is mandatory to PROVIDE SOURCE for every information you found !!!

At the end of response, please provide links to sources where you obtained information

"""



TITLE_TEMPLATE = """

DOCUMENT_SPLIT: $document_split

Izdvoj naslov iz DOCUMENT_SPLIT teksta
"""




DOCUMENT_SYSTEM_MSG_COMPRESSION_V1 = """
Compress the following text in a way that fits in a tweet - 280 characters (ideally)
and such that you (GPT-4) can reconstruct the intention of the human 
who wrote text as close as possible to the original intention. 
This is for yourself. It does not need to be human readable or understandable. 
Abuse of language mixing, abbreviations, symbols (unicode and emoji), 
or any other encodings or internal representations is all permissible, 
as long as it, if pasted in a new inference cycle, 
will yield near-identical results as the original text: 

Complete answer should be formatted this way:

```
TEXT_COMPRESSION: <text you compressed>
```
"""


DOCUMENT_SYSTEM_MSG_COMPRESSION_V2 = """
Compress the given text following rules specified below sorted by priority:
    1. Mandatory keep all enlisted items!!!
    2. Highest priority is to preserve all key information and entities in the text.
    3. Very high priority is to compress the following text in a way that you (GPT-4) 
    can reconstruct the intention of the human who wrote text as close as possible to the original intention. 
    4. If it is possible to keep all key information and entities it is preferable that compressed text fits 
    in a tweet(280) characters.
    If it is not possible to keep all key information and entities it is preferable that compressed text fits 
    in a tweet(280) characters, compress the given text in more then 280 characters.

    5. This is for yourself. 
    It does not need to be human readable or understandable. 
    Abuse of language mixing, abbreviations, symbols (unicode and emoji), 
    or any other encodings or internal representations is all permissible, 
    as long as it, if pasted in a new inference cycle, 
    will yield near-identical results as the original text. 

Complete answer should be formatted this way:

```
TEXT_COMPRESSION: <text you compressed>
```
"""


DOCUMENT_SYSTEM_MSG_COMPRESSION_V2 = """
Compress the given text following rules specified below sorted by priority:
    1. It is mandatory to keep all enlisted items!!!
    2. Highest priority is to preserve all key information and entities in the text.
    3. Very high priority is to compress the following text in a way that you (GPT-4) 
    can reconstruct the intention of the human who wrote text as close as possible to the original intention. 
    4. Compress text size to as much as possible low count of characters

    5. This is for yourself. 
    It does not need to be human readable or understandable. 
    Abuse of language mixing, abbreviations, symbols (unicode and emoji), 
    or any other encodings or internal representations is all permissible, 
    as long as it, if pasted in a new inference cycle, 
    will yield near-identical results as the original text. 

Complete answer should be formatted this way:

```
TEXT_COMPRESSION: <text you compressed>
```
"""


DOCUMENT_SYSTEM_MSG_COMPRESSION_V3 = """
Compress the given text following rules specified below sorted by priority:
    1. It is mandatory to keep all enlisted items!!!
    2. Highest priority is to preserve all key information and entities in the text.
    3. Very high priority is to compress the following text in a way that you (GPT-4) 
    can reconstruct the intention of the human who wrote text as close as possible to the original intention. 
    4. Compress text size to as much as possible low count of characters

    5. This is for yourself. 
    It does not need to be human readable or understandable. 
    Abuse of language mixing, abbreviations, symbols (unicode and emoji), 
    or any other encodings or internal representations is all permissible, 
    as long as it, if pasted in a new inference cycle, 
    will yield near-identical results as the original text. 

Complete answer should be formatted this way:

```
TEXT_COMPRESSION: <text you compressed>
```
"""


DOCUMENT_COMPRESSION_EXTRACT_KEY = "TEXT_COMPRESSION:"


DOCUMENT_COMPRESSION_TEMPLATE_V1 = """
This is text that should be compressed: 
$text_to_compress
"""

DOCUMENT_COMPRESSION_TEMPLATE_V2 = """
This is the given text that should be compressed: 
$text_to_compress
"""





DOCUMENT_SYSTEM_MSG_COMPRESSION_CHECK_V1 = """
You are expert for clinical trial research and you should check if given response is correct.
"""

DOCUMENT_COMPRESSION_CHECK_TEMPLATE_V1 = """

GIVEN_REQUEST:

    ```
    Compress the given text following rules specified below sorted by priority:
        1. It is mandatory to keep all enlisted items!!!
        2. Highest priority is to preserve all key information and entities in the text.
        3. Very high priority is to compress the following text in a way that you (GPT-4) 
        can reconstruct the intention of the human who wrote text as close as possible to the original intention. 
        4. Compress text size to as much as possible low count of characters
    
        5. This is for yourself. 
        It does not need to be human readable or understandable. 
        Abuse of language mixing, abbreviations, symbols (unicode and emoji), 
        or any other encodings or internal representations is all permissible, 
        as long as it, if pasted in a new inference cycle, 
        will yield near-identical results as the original text. 
    
        This is the given text that should be compressed: 
        $text_to_compress
    
    ```

PREVIOUS_RESPONSE: $previous_response
    
    Please check if PREVIOUS_RESPONSE for GIVEN_REQUEST is complete and correct.
    If PREVIOUS_RESPONSE is complete and correct, its MANDATORY!!! that new response should be just "YES".
    If PREVIOUS_RESPONSE is not complete or not correct, please provide as short as possible comment on PREVIOUS_RESPONSE,
    and complete and correct new response.
    
    Your new response should be formatted this way:

```
{
    "comment": <comment>,
    "new_response": <new response>
}
```
    
"""



# For this specific domain CRI chatGPT cant do reconstruction of high extent of comression in proper way.
# Domain fine-tuning is needed
BETTER_COMPRESSION_TEMPLATE = """

The PREVIOUS_RESPONSE is readable, well-formatted, and maintains the essence of the GIVEN_REQUEST. However, the goal was to compress it further using any permissible encodings or representations that I can later reconstruct for a new inference cycle.

Given this, I will compress the text even further.



NEW_RESPONSE: UZpkQI📋. OpšKI:👤sponz,🔀CRO,📖stud,🔢protokol,📊faza,💊lek,🏢ZU&👥istraž. TokKI:📅kvart,👥iskr&rndm,🚫ispitKI,🔒bez(🚫🏥RS&🔗IMP). 18.07.17.
"""




# Rewrite-Retrieve-Read


template = """Answer the users question based only on the following context:

<context>
{context}
</context>

Question: {question}
"""



template = """Provide a better search query for \
web search engine to answer the given question, end \
the queries with ’**’. Question: \
{x} Answer:"""





# Semi-structured RAG
#
# Many documents contain a mixture of content types, including text and tables.


template = """Provide a better search query for \
web search engine to answer the given question, end \
the queries with ’**’. Question: \
{x} Answer:"""


# table_summaries = summarize_chain.batch(tables, {"max_concurrency": 5})


# RAG Fusion
#
# vectorstore = Pinecone.from_existing_index("data_extraction-fusion", OpenAIEmbeddings())
# retriever = vectorstore.as_retriever()
#
# from langchain.load import dumps, loads
#
#
# def reciprocal_rank_fusion(results: List[list], k=60):
#     fused_scores = {}
#     for docs in results:
#         # Assumes the docs are returned in sorted order of relevance
#         for rank, doc in enumerate(docs):
#             doc_str = dumps(doc)
#             if doc_str not in fused_scores:
#                 fused_scores[doc_str] = 0
#             previous_score = fused_scores[doc_str]
#             fused_scores[doc_str] += 1 / (rank + k)
#
#     reranked_results = [(loads(doc), score) for doc, score in
#                         sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)]
#     return reranked_results




# Rules Based Checker
# from langchain_experimental.tot.checker import ToTChecker
# from langchain_experimental.tot.thought import ThoughtValidity

# Step-Back Prompting (Question-Answering)

response_prompt_template = """You are an expert of world knowledge. I am going to ask you a question. Your response should be comprehensive and not contradicted with the following context if they are relevant. Otherwise, ignore them if they are not relevant.

{normal_context}

Original Question: {question}
Answer:"""

from langchain.chains.qa_with_sources.refine_prompts import DEFAULT_REFINE_PROMPT_TMPL


# # Few Shot Examples
# examples = [
#     {
#         "input": "Could the members of The Police perform lawful arrests?",
#         "output": "what can the members of The Police do?"
#     },
#     {
#         "input": "Jan Sindel’s was born in what country?",
#         "output": "what is Jan Sindel’s personal history?"
#     },
# ]
# # We now transform these to example messages
# example_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("human", "{input}"),
#         ("ai", "{output}"),
#     ]
# )
# few_shot_prompt = FewShotChatMessagePromptTemplate(
#     example_prompt=example_prompt,
#     examples=examples,
# )

# Hypothetical Document Embeddings (HyDE)

prompt_template = """Please answer the user's question about the most recent state of the union address
Question: {question}
Answer:"""


# Learned Prompt Variable Injection via RL


# Summarization checker chain

# EmbeddingsRedundantFilter


# k: Optional[int] = 20
# """The number of relevant documents to return. Can be set to None, in which case
# `similarity_threshold` must be specified. Defaults to 20."""
# similarity_threshold: Optional[float]
# """Threshold for determining when two documents are similar enough
# to be considered redundant. Defaults to None, must be specified if `k` is set
# to None."""


# similarity_fn: Callable = cosine_similarity
# """Similarity function for comparing documents. Function expected to take as input
# two matrices (List[List[float]]) and return a matrix of scores where higher values
# indicate greater similarity."""
# similarity_threshold: float = 0.95
# """Threshold for determining when two documents are similar enough
# to be considered redundant."""


# Counter Hypothetical Document Embeddings (HyDE)
# CREATE QUESTIONS FOR CONTEXT

# langchain_experimental.smart_llm import SmartLLMChain

# what is this split related to? many contexts


DOCUMENT_SYSTEM_MSG_SEMANTIC_TEXT_CHUNKING_V1 = """
You are expert for clinical trial research and you should check if given response is correct.
"""

DOCUMENT_SEMANTIC_TEXT_CHUNKING_TEMPLATE_V1 = """for this given text : 
$text_to_chunk 

Chunk this text in semantically connected  text units and format output as  json  list.

Extract the semantic sections and for every section extract list of its subsections, 
understanding their content, and then dividing them into coherent units that can be represented in a JSON format.

For every unit please provide:

Section Title: [Title of the Section]
Section Content Summary: [Brief summary or key points of this subsection]
Section Text:[Here provide section full original text content]
Section References:[List of all important concepts and terms that this section refers to  taking in account whole text]
Section Topics:[List of all topics and terms that this section refers to  taking in account whole text]
For this section give Subsection List:
Subsection Title: [Details of Subsection]
Subsection Content Summary: [Brief summary or key points of this subsection]
Subsection Text :[Here provide subsection full original text content]
Subsection References:[List of all important concepts and terms that this subsections refers to  taking in account whole containing section text]
Subsection Topics:[List of all topics and terms that this subsection refers to  taking in account whole containing section text]


!!!It is MANDATORY to populate all of these values!!!
!!!It is MANDATORY to give original content!!!

Output should look like this:

[{
    "section_title": "",
    "section_content_summary": "",
    "section_text": "",
    "section_references": [],
    "section_topics": [],
    "subsection_list": 
    [
        {
            "subsection_title": "",
            "subsection_content_summary": "",
            "subsection_text": "",
            "subsection_references": [],
            "subsection_topics": []
        }
    ]
}]"""




DOCUMENT_SYSTEM_MSG_QUESTION_STATEMENT_V1 = """
You are psychologist and wise man and you should find best motivational quotes to support users current psychological state.
"""

QUESTION_STATEMENT_PROMPT_TEMPLATE_V1 = """
Formulate this question as a statement:
$question 
"""


THREE_QUESTION_STATEMENTS_PROMPT_TEMPLATE_V1= """
Formulate given question as a statement in three different ways. 
Export json list of strings:

QUESTION: $question 
"""

THREE_QUESTION_STATEMENTS_PROMPT_TEMPLATE_V2= """
Formulate given question or statement as a statement in three different ways. 
Export json list of strings:

QUESTION: $question 
"""

QUERY_BASED_COMPRESSION_TEMPLATE_V1 = """

We are looking for answer on this question: 
QUESTION: $question
in the text given bellow.

This is the given text we are looking for answer on given question: 
TEXT: $text_to_compress

Pick up all information form given TEXT related to given QUESTION 
and compress related information following rules specified below sorted by priority:
    1. It is mandatory to keep all enlisted items!!!
    2. Highest priority is to preserve all key information and entities in the text.
    3. Very high priority is to compress the following text in a way that you (GPT-4) 
    can reconstruct the intention of the human who wrote text as close as possible to the original intention. 
    4. Compress text size to as much as possible low count of characters

    5. This is for yourself. 
    It does not need to be human readable or understandable. 
    Abuse of language mixing, abbreviations, symbols (unicode and emoji), 
    or any other encodings or internal representations is all permissible, 
    as long as it, if pasted in a new inference cycle, 
    will yield near-identical results as the original text. 

Complete answer should be formatted this way:

```
TEXT_COMPRESSION: <text you compressed>
```


$text_to_compress

"""


DOCUMENT_SYSTEM_MSG_QUESTION_RELATED_INFORMATION_V1 = """
You are expert for clinical trial research and you should check if given response is correct.
"""

QUESTION_RELATED_INFORMATION_PROMPT_TEMPLATE_V2 = """
QUESTION: $question 
SECTION_TEXT: $section_text

From given SECTION_TEXT extract ALL!!! information relevant for given QUESTION.
    1. It is mandatory to keep any related enlisted items!!!
    2. Highest priority is to preserve all key information and entities in the text. 

If there is no any related information, please always answer with this answer:
NO RELEVANT INFO    
    
Complete answer should be exclusively in Serbian language formatted this way:

```
<all related info text>
```
"""

QUESTION_RELATED_INFORMATION_PROMPT_TEMPLATE_V1 = """
QUESTION: $question 
SECTION_TEXT: $section_text

From given SECTION_TEXT extract ALL!!! information relevant for given QUESTION.
    1. It is mandatory to keep any related enlisted items!!!
    2. Highest priority is to preserve all key information and entities in the text. 
    3. Enlist with bullet points all important items related to question!!!
    4. Formulate output as answer to given QUESTION!!!

If there is no any related information, please always answer with this answer:
NO RELEVANT INFO    

Complete answer should be exclusively in Serbian language!!! (Latin)!!! formatted this way:

```
ANSWER:  <all related info text>
```
PLease check if this ANSWER contains all information requested by QUESTION.

"""

QUESTION_RELATED_INFORMATION_PROMPT_TEMPLATE_V3 = """
PSYCHOLOGICAL_STATE: $psychological_state
SECTION_TEXT: $section_text

From given SECTION_TEXT extract !!!MAXIMUM 3!!! !!!MOTIVATIONAL QUOTES!!! which are best to support person facing explained PSYCHOLOGICAL_STATE.
    1. Dont give any additional explanation, just enlist related quotes
    1. Enlist with bullet points all motivational quotes related to given PSYCHOLOGICAL_STATE!!!
    2. Quotes should be exactly the same as given in SECTION_TEXT!!!

If there is no any related information, please always answer with this answer:
NO RELEVANT INFO    

Output should be just valid json list look like this:
[{"some quote": "quote source"},
    {"some quote": "quote source"},
    {"some quote": "quote source"}]
"""

QUESTION_RELATED_INFORMATION_PROMPT_TEMPLATE_V5 = """
PSYCHOLOGICAL_STATE: $psychological_state
SECTION_TEXT: $section_text

From given SECTION_TEXT extract !!!MAXIMUM 3!!! !!!MOTIVATIONAL QUOTES!!! which are best to support person facing explained PSYCHOLOGICAL_STATE.
    1. Dont give any additional explanation, just enlist related quotes
    1. Enlist with bullet points all motivational quotes related to given PSYCHOLOGICAL_STATE!!!
    2. Quotes should be exactly the same as given in SECTION_TEXT!!!

If there is no any related information, please always answer with this answer:
NO RELEVANT INFO    

Output should be json look like this:
[{"some quote": "quote source"},
    {"some quote": "quote source"},
    {"some quote": "quote source"}]

"""

QUESTION_RELATED_INFORMATION_PROMPT_TEMPLATE_V4 = """
PSYCHOLOGICAL_STATE: $psychological_state
SECTION_TEXT: $section_text

From given SECTION_TEXT extract !!!MAXIMUM 3!!! !!!MOTIVATIONAL QUOTES!!! which are best to support person facing explained PSYCHOLOGICAL_STATE.
    1. Dont give any additional explanation, just enlist related quotes
    1. Enlist with bullet points all motivational quotes related to given PSYCHOLOGICAL_STATE!!!
    2. Quotes should be exactly the same as given in SECTION_TEXT!!!

ANSWER should be formatted as json list.

If there is no any related information, please always answer with this answer:
NO RELEVANT INFO    

PLease check if this ANSWER contains all MOTIVATIONAL quotes related to explained PSYCHOLOGICAL_STATE.

Output should look like this:
ANSWER: [
    {"some quote": "quote source"},
    {"some quote": "quote source"},
    {"some quote": "quote source"}
]

"""


# ```json
# [
#   {
#     "Section Title": "I. УВОДНЕ ОДРЕДБЕ",
#     "Section Content Summary": "Introduction to the regulation specifying the content and labeling of external and internal packaging of medicines, additional labeling, and the content of the medicine instructions.",
#     "Section Text": "I. УВОДНЕ ОДРЕДБЕ\nСадржина правилника\nЧлан 1.\nОвим правилником прописује се садржај и начин обележавања спољњег и унутрашњег паковања\nлека, додатно обележавање лека, као и садржај упутства за лек.",
#     "Section References": ["правилник", "лек", "спољње паковање", "унутрашње паковање", "обележавање", "упутство за лек"],
#     "Subsection Topics": ["Садржина правилника", "обележавање", "упутство за лек"],
#     "Subsections": [
#       {
#         "Subsection Title": "Садржина правилника",
#         "Subsection Content Summary": "Defines the regulation of the content and labeling of external and internal packaging of medicines, additional labeling, and the content of the medicine instructions.",
#         "Subsection Text": "Члан 1.\nОвим правилником прописује се садржај и начин обележавања спољњег и унутрашњег паковања\nлека, додатно обележавање лека, као и садржај упутства за лек.",
#         "Subsection References": ["правилник", "лек", "спољње паковање", "унутрашње паковање", "обележавање", "упутство за лек"],
#         "Subsection Topics": ["правилник", "обележавање", "упутство за лек"]
#       }
#     ]
#   },
#   {
#     "Section Title": "II. САДРЖАЈ И НАЧИН ОБЕЛЕЖАВАЊА СПОЉЊЕГ ПАКОВАЊА ЛЕКА",
#     "Section Content Summary": "Details the requirements for the content and method of labeling the external packaging of medicines.",
#     "Section Text": "II. САДРЖАЈ И НАЧИН ОБЕЛЕЖАВАЊА СПОЉЊЕГ ПАКОВАЊА ЛЕКА\nЧлан 5.\nСпољње паковање лека јесте паковање у коме се налази унутрашње паковање лека.\nЧлан 6.\nНа спољњем паковању лека, кao и на паковању код кога унутрашње паковање уједно представља и спољње паковање лека, морају да буду наведени следећи подаци: [followed by a list of required information]",
#     "Section References": ["спољње паковање", "лек", "обележавање", "информације"],
#     "Subsection Topics": ["Спољње паковање лека", "обележавање", "информације"],
#     "Subsections": [
#       {
#         "Subsection Title": "Спољње паковање лека",
#         "Subsection Content Summary": "Defines what is considered the external packaging of a medicine.",
#         "Subsection Text": "Члан 5.\nСпољње паковање лека јесте паковање у коме се налази унутрашње паковање лека.",
#         "Subsection References": ["спољње паковање", "лек"],
#         "Subsection Topics": ["спољње паковање"]
#       },
#       {
#         "Subsection Title": "Обележавање спољњег паковања лека",
#         "Subsection Content Summary": "Lists the specific information that must be included on the external packaging of medicines.",
#         "Subsection Text": "Члан 6.\nНа спољњем паковању лека, кao и на паковању код кога унутрашње паковање уједно представља и спољње паковање лека, морају да буду наведени следећи подаци: [followed by a list of required information]",
#         "Subsection References": ["спољње паковање", "лек", "обележавање", "информације"],
#         "Subsection Topics": ["обележавање", "информације"]
#       }
#     ]
#   }
# ]



# please summarize all most important information from given text related to this question
# extract all important information from given text related to this question
# extract enlist and summarize all important information from given text related to this question

class PromptTemplateCreator:


    def __init__(self):
        print()

    # def create_similar_sentences_prompt(self, question:str, references_list: List[ScoredPoint]) -> tuple[str, str]:
    #
    #     references_text = ""
    #
    #     for i, reference in enumerate(references_list, start=1):
    #         text = reference.payload["text"].strip()
    #         references_text += f"\n[{i}]: {text}"
    #
    #     key_value_to_change ={
    #         "question": question.strip(),
    #         "references": references_text,
    #     }
    #
    #     prompt = self.prepare_template(QUESTION_PROMPT_TEMPLATE, key_value_to_change)
    #
    #     return prompt, references_text

    #
    # def create_recommended_sentences_prompt(self, questions_list:str, references_list: List[ScoredPoint]) -> tuple[str, str]:
    #
    #     questions_text = ""
    #
    #     for i, question in enumerate(questions_list, start=1):
    #         text = question.payload["question"].strip()
    #         questions_text += f"\n[{i}]: {text}"
    #
    #     references_text = ""
    #
    #     for i, reference in enumerate(references_list, start=1):
    #         text = reference.payload["text"].strip()
    #         references_text += f"\n[{i}]: {text}"
    #
    #     key_value_to_change ={
    #         "questions": questions_text,
    #         "references": references_text,
    #     }
    #
    #     prompt = self.prepare_template(RECOMMEND_PROMPT_TEMPLATE, key_value_to_change)
    #
    #     return prompt, references_text


    def prepare_template(self, template: str, **kwargs) -> str:
        prompt_template = Template(template)
        try:
            prepared_prompt = prompt_template.safe_substitute(kwargs)
        except KeyError as e:
            print(e)
        except ValueError as e:
            print(e)

        # mapping = defaultdict(str, key_value_to_change)
        # prepared_prompt = template.format_map(mapping=mapping)
        return prepared_prompt

    def get_document_extraction_evaluation(self, ocr_document_extraction: str, di_document_extraction: str) -> str:
        user_prompt = self.prepare_template(DOCUMENT_EXTRACTION_EVALUATION_V1,
                                            ocr_document_extraction=ocr_document_extraction,
                                            di_document_extraction=di_document_extraction)
        return user_prompt

    def get_document_data_prompt(self, document_content: str) -> str:
        user_prompt = self.prepare_template(EXTRACT_CERTIFICATE_DATA_V1, document_content=document_content)
        return user_prompt

    def get_document_data_prompt_material_groups_list(self, document_content: str, material_groups_list: list) -> str:
        user_prompt = self.prepare_template(EXTRACT_CERTIFICATE_DATA_V2, document_content=document_content, certificate_scope_list=str(material_groups_list))
        return user_prompt

    def get_enrich_dnb_data_prompt(self, screened_person_dnb: str):
        user_prompt = self.prepare_template(ENRICH_DNB_DATA_TEMPLATE, screening_personal_data=screened_person_dnb)
        return user_prompt


    def get_screened_person_additional_data_prompt(self, screening_personal_data: str) -> str:
        user_prompt = self.prepare_template(SCREENING_PERSONAL_DATA_TEMPLATE, screening_personal_data=screening_personal_data)
        return user_prompt


    def get_personal_data_inconsistencies_prompt(self, screening_personal_data: str, potential_matches: str) -> str:
        user_prompt = self.prepare_template(PERSONAL_DATA_INCONSISTENCIES_COMPARISON_TEMPLATE,
                                            screening_personal_data=screening_personal_data,
                                            potential_matches = potential_matches)
        return user_prompt


    def get_screened_person_matches_prompt(self, screening_personal_data: str, potential_matches: str) -> str:
        user_prompt = self.prepare_template(SCREENING_PERSONAL_DATA_COMPARISON_TEMPLATE,
                                            screening_personal_data=screening_personal_data,
                                            potential_matches = potential_matches)
        return user_prompt


    def get_screened_search_more_prompt(self, screening_personal_data: str) -> str:
        user_prompt = self.prepare_template(SCREENING_PERSONAL_SEARCH_MORE_TEMPLATE,
                                            screening_personal_data=screening_personal_data)
        return user_prompt


    def get_title_extract_prompt(self, document_split: str) -> str:
        user_prompt = self.prepare_template(TITLE_TEMPLATE, document_split=document_split)
        return user_prompt

    def get_query_based_text_compression_prompt(self, query: str, document_split: str) -> str:
        user_prompt = self.prepare_template(QUERY_BASED_COMPRESSION_TEMPLATE_V1, query = query, text_to_compress=document_split)
        return user_prompt

    def get_three_question_statements(self, question: str) -> str:
        user_prompt = self.prepare_template(THREE_QUESTION_STATEMENTS_PROMPT_TEMPLATE_V2, question=question)
        return user_prompt

    def get_question_related_information(self, psychological_state: str, section_text: str) -> str:
        user_prompt = self.prepare_template(QUESTION_RELATED_INFORMATION_PROMPT_TEMPLATE_V3,
                                            psychological_state=psychological_state,
                                            section_text=section_text)
        return user_prompt

    def get_document_text_compression_prompt(self, document_split: str) -> str:
        user_prompt = self.prepare_template(DOCUMENT_COMPRESSION_TEMPLATE_V2, text_to_compress=document_split)
        return user_prompt

    def get_document_text_compression_check_prompt(self, document_split: str, previous_response: str) -> str:
        user_prompt = self.prepare_template(DOCUMENT_COMPRESSION_CHECK_TEMPLATE_V1,
                                            text_to_compress=document_split,
                                            previous_response = previous_response)
        return user_prompt


    def get_document_semantic_text_chunks_prompt(self, new_text_to_chunk, last_previous_section) -> str:
        text_to_chunk = new_text_to_chunk+" "+last_previous_section
        user_prompt = self.prepare_template(DOCUMENT_SEMANTIC_TEXT_CHUNKING_TEMPLATE_V1,
                                            text_to_chunk=text_to_chunk)
        return user_prompt