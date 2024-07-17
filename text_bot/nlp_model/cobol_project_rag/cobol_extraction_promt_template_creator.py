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

SYSTEM_MSG_TITLE = """
Izdvoj naslov iz zadatog teksta.
Kompletan odgovor treba da bude u dole zadatom formatu:

```
TITLE: <title you extracted>
```
"""

TITLE_EXTRACT_KEY = "TITLE:"

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
# vectorstore = Pinecone.from_existing_index("rag-fusion", OpenAIEmbeddings())
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


SYSTEM_MSG_COBOL_EXPERT_V1 = """
You are COBOL programming language expert.
"""

FRD_V1 = """
For given COBOL project module description in json format:

COBOL_project_module_description: $cobol_project_description

You should provide a Functional Specification Document based on the provided COBOL_project_module_description.

Functional Specification Document Creation Instructions:

You should create a Functional Specification Document based on the provided COBOL code explanation. 
This document should encapsulate: 
 - the functionality, 
 - logic 
 - internal interactions
 - external relations with external systems, subroutines, and modules
 
This document should include outline the steps to generate the corresponding Java code for the main program logic.

You should find these fields in COBOL_project_module_description:


    - BUSSINES LOGIC DESCRIPTION
    - BUSSINES LOGIC FEATURES LIST
    - FUNCTIONAL LOGIC DESCRIPTION
    - FUNCTIONAL LOGIC FEATURES LIST
    - variables list - name and description
    - errors edge cases list - description
    - dependencies list - name, description, input/output variables
    - declaratives - description
    - CHILD_NODES_BUSSINES_LOGIC_SUMMARIZATION - lower layers connected nodes summarized bussines logic description,
    - CHILD_NODES_FUNCTIONAL_LOGIC_SUMMARIZATION - lower layers connected nodes summarized functional logic description,
    - DEPENDENCY_NODES_BUSSINES_LOGIC_SUMMARIZATION - dependencies summarized bussines logic description,
    - DEPENDENCY_NODES_FUNCTIONAL_LOGIC_SUMMARIZATION - dependencies summarized functional logic description
    - GENERAL_INPUT_AND_OUTPUT_VARIABLES_LIST - inputs that should be given and outputs that we expect for this module, enlisted and explained
    - OVERALL_WORK_FLOW - overall workflow considering dependencies
    - variables_list - list of all variables used with names and descriptions
    - errors_edge_cases_list - list of all errors and edge cases covered by code implementation 
    - declaratives - additional error and edge cases covered
    - dependencies_list - all dependencies explained
  

Your document should include:

- title - "Functional Specification for:" give here brief description that fits in standard title
- subtitle -A descriptive subtitle and introduction to the functionality, one sentecne at most.
- external_calls - A section explaining each external call, its purpose, and how it integrates.
- internal_calls -A section detailing each code chunk call, including why and how the main block interacts with it.
- variables - A description of the variables, their roles, and their scopes.
- logic_flow - A comprehensive walkthrough of the logic flow, including conditionals, loops, any error handling, and overall program structure.
- overall_summarization - A conclusion summarizing the place and purpose of this module within the larger application.

Desired Outcome:

A well-structured and professional Functional Specification Document.
The length should be sufficient to cover all the details but concise enough to avoid redundancy — typically ranging between 3-5 pages.
The format should be clear and organized, with headings, subheadings, bullet points, and diagrams (if necessary) to enhance readability.
The style should be formal and technical, suitable for a developer audience who may later use this document to recreate the logic in Java.

Example Output Format:

Title: 
Subtitle:

Introduction:
 Overview of this module purpose and high-level functionality.

External Calls:
 - ExternalCall1: Description and integration detail.
 - ExternalCall2: Description and integration detail.

Internal Calls:
 - InternalCall1: Description and interaction detail.
 - InternalCall2: Description and interaction detail.

Variable Declarations:
 - Variable1: Description and usage.
 - Variable2: Description and usage.

Logic Flow:
 Step-by-step walkthrough of this module logic.

Java Code Generation Steps Section:

Detail the process of translating this module logic into Java, including:

    Suggested architecture for modern Java app.
    Mapping of COBOL data types to Java data types.
    Conversion of COBOL specific structures to Java constructs.
    Handling file operations and database access in Java.
    Recommendations for replicating COBOL program cycle in Java (if applicable).

Conclusion:
 Summary of this module functionality and its relevance to the larger system.

Appendices:
 (If applicable, include any additional relevant diagrams, tables, or references.)

What to Ensure:

The document MUST reflect the provided COBOL project description accurately.
Technical terms should be used appropriately.
All assumptions about the external environment should be stated.
Cross-referencing within the document for variable usage and call flows is encouraged for clarity.
Clear, step-by-step instructions for the Java code generation.
Please proceed with the creation of the Functional Specification Document as per the instructions and details provided above.

"""

ADD_DEPENDENCIES_SUMMARIZATION_V1 = """
From this COBOL code information extraction:

$current_cobol_code_extraction prepared 

And dependencies extractions:

Children description list:

$children_description_extraction_list:


Dependencies description list:

$dependencies_description_extraction_list:


Extract information below:

CHILD_NODES_BUSSINES_LOGIC_SUMMARIZATION - lower layers connected nodes summarized bussines logic description,
CHILD_NODES_FUNCTIONAL_LOGIC_SUMMARIZATION - lower layers connected nodes summarized functional logic description,


DEPENDENCY_NODES_BUSSINES_LOGIC_SUMMARIZATION - dependencies summarized bussines logic description,
DEPENDENCY_NODES_FUNCTIONAL_LOGIC_SUMMARIZATION - dependencies summarized functional logic description

GENERAL_INPUT_AND_OUTPUT_VARIABLES_LIST - inputs that should be given and outputs that we expect for this module, enlisted and explained

OVERALL_WORK_FLOW - overall workflow considering dependencies

Output should look like this:    


{
      "CHILD_NODES_BUSSINES_LOGIC_SUMMARIZATION": "",
      "CHILD_NODES_FUNCTIONAL_LOGIC_SUMMARIZATION": "",
      "DEPENDENCY_NODES_BUSSINES_LOGIC_SUMMARIZATION": "",
      "DEPENDENCY_NODES_FUNCTIONAL_LOGIC_SUMMARIZATION": "",
      "GENERAL_INPUT_AND_OUTPUT_VARIABLES_LIST": ""
      "OVERALL_WORK_FLOW": ""
"""



COBOL_IDENTIFICATION_DIVISION_V1 = """
From this COBOL code block:

$cobol_code

Extract information below:

IDENTIFICATION DIVISION: [extract all releavnt IDENTIFICATION DIVISION  info and enlist all subdivisions with its values]
    usual subsections:
    PROGRAM-ID: [extract PROGRAM ID]
    program name: [extract program name]
    author: [export author]
    please check if there more subsections for IDENTIFICATION DIVISION and export all releavnt info and enlist all subdivisions with its values.

Output should look like this:

"identification_division": {
  "general_info": "",
  "program_id": "",
  "program_name": "",
  "author": ""
}

"""

COBOL_ENVIRONMENT_DIVISION_V1 = """
From this COBOL code block:

$cobol_code

Extract information below:


ENVIRONMENT DIVISION: [extract all releavnt ENVIRONMENT DIVISION info and enlist all subdivisions with its values]
    usual subsections:
    CONFIGURATION SECTION: [extract all releavnt CONFIGURATION SECTION info and enlist all subdivisions with its values]
    INPUT-OUTPUT SECTION: [extract all releavnt INPUT-OUTPUT SECTION info and enlist all subdivisions with its values]
        FILE-CONTROL: [extract all releavnt FILE-CONTROL info and enlist all subdivisions with its values, file names and variables]
        I-O-CONTROL: [extract all releavnt I-O-CONTROL info and enlist all subdivisions with its values and all variables]
        please check if there more subsections for ENVIRONMENT DIVISION and export all releavnt info and enlist all subdivisions with its values.



Output should look like this:

"environment_division": {
  "general_info": "",
  "configuration_section": "",
  "input_output_section": {
    "general_info": "",
    "file_control": "",
    "io_control": "",
    "variables_list": [],
    "filenames_list": []
  }
"""

COBOL_DATA_DIVISION_V1 = """      
From this COBOL code block:

$cobol_code

Extract information below:


DATA DIVISION: [extract all releavnt DATA DIVISION info and enlist all subdivisions with its values]
    usual subsections:
    FILE SECTION: [extract all releavnt FILE SECTION info and enlist all subdivisions with its values]
        FD: [extract value (File Description) entry provides the details about the file, including its name and record structure.]
        LABEL RECORDS ARE STANDARD: [extract value Indicates that standard label records are used.]
        BLOCK CONTAINS 0 RECORDS: [extract value Specifies the number of records in each block. A value of 0 means no blocking.]
        RECORD CONTAINS 80 CHARACTERS: [extract value Specifies the length of each record.]
        DATA RECORD IS INPUT-RECORD: [extract value Associates the file with the record description (INPUT-RECORD).]
        01: [Level Records The 01 level defines the record structure within the file.]
            Level Fields: [extract fields Define individual fields within the record.]

    WORKING-STORAGE SECTION: [extract all releavnt WORKING-STORAGE SECTION info and enlist all subdivisions with its values]

    WORKING-STORAGE VARIABLES: [extract all WORKING-STORAGE variables list with variables names and explanation]
    LOCAL-STORAGE SECTION: [extract all releavnt LOCAL-STORAGE SECTION info and enlist all subdivisions with its values]
    LOCAL-STORAGE VARIABLES: [extract all LOCAL-STORAGE variables list with variables names and explanation]
    LINKAGE SECTION: [extract all releavnt LINKAGE SECTION info and enlist all subdivisions with its values]
    LINKAGE SECTION VARIABLES: [extract and enlist all variables with its name and explanation]
    COMMUNICATION SECTION: [extract all releavnt COMMUNICATION SECTION info and enlist all subdivisions with its values]
        LENGTH: [extract value The length of the message.]
        STATUS: [extract value A status variable to hold the result of communication operations.]
        QUEUE: [extract value The name of the queue used for communication.]
        MESSAGE-STATUS: [extract value A variable to store the status code after sending or receiving a message.]
        QUEUE-NAME: [extract value The name of the queue to which messages are sent or from which messages are received.]
        MESSAGE-AREA: [extract value The area in memory where the message content is stored.]
    REPORT SECTION: [extract all releavnt REPORT SECTION info and enlist all subdivisions with its values]

        RD: [(Report Description) Entry]
            PAGE LIMIT 60 LINES: [extract value Specifies the number of lines per page.]
            FIRST DETAIL 10: [extract value The first detail line starts at line 10.]
            LAST DETAIL 50: [extract value The last detail line ends at line 50.]
            CONTROLS ARE DEPARTMENT: [extract value Indicates that the report is controlled by the DEPARTMENT field.]

        01: [Level Report Group]
            TYPE PAGE HEADING: [extract value Defines the layout for the page heading.]
            TYPE DETAIL: [extract value Defines the layout for the detail lines.]
            TYPE SUMMARY: [extract value Defines the layout for summary lines at the end of the report.]

    SCREEN SECTION: [extract all releavnt SCREEN SECTION info and enlist all subdivisions with its values]

        BLANK SCREEN: [extract value Clears the screen before displaying new content.]
        LINE and COLUMN: [extract value Specifies the position of text and fields on the screen.]
        VALUE: [extract value Displays a static text on the screen.]
        PIC and USING: [extract all input fields and variables.]

    please check if there more subsections for DATA DIVISION and export all releavnt info and enlist all subdivisions with its values.


Output should look like this:


"data_division": {
  "general_info": "",
  "file_section": {
    "fd": "",
    "label_records_are_standard": "",
    "block_contains_0_records": "",
    "record_contains_80_characters": "",
    "data_record_is_input_record": "",
    "01": []
  },
  "working_storage_section": {
    "general_info": "",
    "working_storage_variables_list": [
      {
        "variable_name": "",
        "variable_type": "",
        "variable_explanation": "",
        "variable_init_value": ""
      }...
    ]
  },
  "local_storage_section": {
    "general_info": "",
    "local_storage_variables_list": [
      {
        "variable_name": "",
        "variable_type": "",
        "variable_explanation": "",
        "variable_init_value": ""
      }...
    ]
  },
  "linkage_section": {
    "general_info": "",
    "linkage_variables_list": [
      {
        "variable_name": "",
        "variable_type": "",
        "variable_explanation": "",
        "variable_init_value": ""
      }...
    ]
  },
  "communication_section": {
    "general_info": "",
    "length": "",
    "status": "",
    "queue": "",
    "message_status": "",
    "queue_name": "",
    "message_area": ""
  },
  "report_section": {
    "rd": {
      "page_limit_60_lines": "",
      "first_detail_10": "",
      "last_detail_50": "",
      "controls_are_department": ""
    },
    "01": {
      "type_page_heading": "",
      "type_detail": "",
      "type_summary": ""
    }
  },
  "screen_section": {
    "blank_screen": "",
    "line_and_column": "",
    "value": "",
    "pic_and_using": []
  }
}
"""

COBOL_PROCEDURE_DIVISION_V1 = """
From this COBOL code block:

PROVIDED_COBOL_CODE: $cobol_code 

Extract information below:

If PROVIDED_COBOL_CODE doesnt contain all the info, it is !!!MANDATORY!!! to provide info that are contained!!!

-DEV_COMMENTS - [please extract all already existing comments in code one by one as list],
-BUSSINES_LOGIC_DESCRIPTION - [general description of what this code is used for regarding bussines logic],
-BUSSINES_LOGIC_FEATURES_LIST - [list of features implemented by this code section regarding bussines logic],
-FUNCTIONAL_LOGIC_DESCRIPTION - [general description of what this code is doing regarding functional logic],
-FUNCTIONAL_LOGIC_FEATURES_LIST - [list of all functionalities implemented by this code section from tech perspective],
-WORK_FLOW - [Step-by-step walkthrough of this module logic and external calls logic]

-VARIABLES_LIST - [list of all variables used in this code]
        VARIABLE should contain these info: 
        - NAME - [original variable name],
        - DEFINITION - [list of any of these values that explain variable (internal, external, input, output, implicit, explicit, global, local)]    
        - DESCRIPTION - [variables description],
        - ADAPTED_NAME - [please provide meaningfull and explainatory name for this variable],
        - DATA_STRUCTURE_OR_TYPE - [data structures or type of this variable]
        - VARIABLE_INIT_VALUE - value that variable is initialised with

-DEPENDENCIES_LIST - [list of all dependencies, external sections, paragraphs and procedures called from this code],
        DEPENDENCIES should contain these info:
        DEPENDENCY_NAME - [name of paragraph, or procedure, or section performed or called from this code block]
        DEPENDENCY_VARIABLES - [list of all input or output variables passed during this dependency call or perform]
        DEPENDENCY_TYPE - [internal or external]

-ERRORS_EDGE_CASES_LIST - [list of all code errors and edge cases]    
    ERROR_EDGE_CASE should contain:
    - CODE - [code that implements this error or edge case handling]
    - DESCRIPTION - [description of error edge case]
    - HANDLING - [description of handling process ]

DECLARATIVES: [extract all releavnt DECLARATIVES info and enlist all subdivisions with its values
declaratives types:
    ERROR-HANDLING SECTION: [A section named for handling errors.]
    USE AFTER STANDARD ERROR PROCEDURE ON INPUT-FILE: [Specifies that the code in ERROR-PARA should be executed after a standard error on INPUT-FILE.]
    ERROR-PARA:[ A paragraph that handles the error by displaying a message, performing termination steps, and stopping the program.]]

If PROVIDED_COBOL_CODE doesnt contain all the info, it is !!!MANDATORY!!! to provide info that are contained!!!

Output should look like this:    

"procedure_division": {
  "general_info": "",
  "procedures_list": [
    {
      "DEV_COMMENTS": "",
      "BUSSINES_LOGIC_DESCRIPTION": "",
      "BUSSINES_LOGIC_FEATURES_LIST": "",
      "FUNCTIONAL_LOGIC_DESCRIPTION": "",
      "FUNCTIONAL_LOGIC_FEATURES_LIST": "",
      "WORK_FLOW": "",
      "variables_list": [
        {
          "NAME": "",
          "DEFINITION": "",
          "DESCRIPTION": "",
          "ADAPTED_NAME": "",
          "DATA_STRUCTURE_OR_TYPE": "",
          "VARIABLE_INIT_VALUE":""
        },
        ...
      ],
      "errors_edge_cases_list": [
        {
          "CODE": "",
          "DESCRIPTION": "",
          "HANDLING": ""
        },
        ...
      ],
      "dependencies_list": [
        {
          "dependency_name": "",
          "dependency_variables": [
            {
              "NAME": "",
              "DEFINITION": "",
              "DESCRIPTION": "",
              "ADAPTED_NAME": "",
              "DATA_STRUCTURE_OR_TYPE": "",
              "DEPENDENCY_TYPE":""
            },
            ...
          ]
        },
        ...
      ],
      "declaratives": [
        {
          "code_implementation": "",
          "explanation": "",
          "declarative_type": ""
        },
        ...
      ]
    },
    ...
  ]
}
"""

COBOL_DIVISION_V1 = """

for this COBOL DIVISION: cobol_division
and this COBOL SECTION: cobol_section

extract all the most important information related to 
business logic
functional logic - what is this part of code used for 
variables
extract some very important informtions about this part of code implementation


-NAME - COBOL code referent name of this structure chunk   
-TYPE - COBOL code structure chunk type  
-CODE- original source code where we extracted the rest of info from
-DEV_COMMENTS - already existing comments in code,
-BUSSINES_LOGIC_DESCRIPTION - bussines logic general description,
-BUSSINES_LOGIC_FEATURES_LIST - list of features implemented by this code section from bussines perspective,
-FUNCTIONAL_LOGIC_DESCRIPTION -functional logic general description,
-FUNCTIONAL_LOGIC_FEATURES_LIST - list of functionalities implemented by this code section from tech perspective,
-EDGE_CASES_LIST - list of edge cases explanations, covered in this COBOL code chunk implementation,
-ERROR_HANDLING_LIST - error handling covered by cobol code chunk,
-CHILD_AND_DEPENDENCY_NODES_BUSSINES_LOGIC_SUMMARIZATION - lower layers connected nodes and dependencies summarized bussines logic description,
-CHILD_AND_DEPENDENCY_NODES_FUNCTIONAL_LOGIC_SUMMARIZATION - lower layers connected nodes and dependencies summarized functional logic description,
- list of all dependencies added as references
- list of all variables added as references
- list of all inputs and outputs added as references
- list of all code subsections added as references
podsetnik - list of all code chunks variables exchange  and connections, same data sources access, db etc
 
VARIABLE_NODE
reference to parent node - internal, external, input, output, implicit, explicit

    - NAME - original variable name,
    - DESCRIPTION - internal variables list description,
    - ADAPTED_NAME - internal variables meaningfull and explainatory names mapping, cammel case,
    - DATA_STRUCTURE_OR_TYPE - internal variables map of used data structures and types
    
DATA_STRUCTURE_NODE
    - FIELDS_LIST - field names list
    - FIELDS_TYPES_LIST - field types list
    - FIELDS_DESCRIPTION_LIST - field description list
    - FIELD_ADAPTED_NAME_LIST - field adapted names list"""



COBOL_FILE_CONTENT_LISTING_EXTRACTION_TEMPLATE_V1 = """
For this given cobol file content : 

$cobol_code 

Extract information below:

BEGINING CODE: [full source code on the beggining of the file that doesnt belong to any section]
IDENTIFICATION DIVISION: [extract all relevant IDENTIFICATION DIVISION  info and enlist all sections with its values]
ENVIRONMENT DIVISION: [extract all relevant ENVIRONMENT DIVISION info and enlist all sections with its values]
DATA DIVISION: [extract all relevant DATA DIVISION info and enlist all sections with its values]
PROCEDURE DIVISION: [extract all relevant PROCEDURE DIVISION info and enlist all sections]
    usual subsections:
    PROCEDUREDS LIST: !!!It is MANDATORY to extract list of ALL EXISTING explicitly enlisted PROCEDURES implemented in code !!! with informations below provided: 
        procedure name: [procedure defined name]
        procedure code is completed: [is this procedure code completed, True/False]
        is_procedure: [is this explicitly entitled as PROCEDURE ]
        sections list: [list of names of all implemented sections ]
            section_name: [SECTION name]
            is_section: [is this explicitly entitled as SECTION ]
        DECLARATIVES: [extract all relevant DECLARATIVES info and enlist all subdivisions with its values

    please check if there more subsections for PROCEDURE DIVISION and export all relevant info and enlist all subdivisions.

PROCEDUREDS LIST: !!!It is MANDATORY to extract ALL EXISTING explicitly enlisted IMPLEMENTED PROCEDURES list with all procedure fields filled up.
PROCEDUREDS LIST: !!!It is MOST IMORTANT to extract list of ALL EXISTING explicitly enlisted  IMPLEMENTED PROCEDURES list with all procedure fields filled up.

PROCEDURE SECTIONS LIST: !!!It is MANDATORY to extract ALL  EXISTING explicitly enlisted  IMPLEMENTED SECTIONS FOR EVERY PROCEDURE list with all section fields filled up for every single procedure.

SECTIONS LIST: !!!It is MOST IMORTANT to extract list of ALL EXISTING explicitly enlisted IMPLEMENTED SECTIONS list with all section fields filled up.

LAST SECTION: [last code section in the file]
  FULL LAST SECTION SOURCE CODE: [full source code of the last section in the file]
  IS SECTION CODE COMPLETED: [is the last character in this section ".", True/False]

FULL LAST SECTION SOURCE CODE:[full last section source code]


!!!If there is NO enlisted PROCEDURE enlist JUST SECTIONS !!!

!!!It is MANDATORY to include ALL EXISTING explicitly enlisted PROCEDURES AND ALL SECTIONS!!!

!!! If there is code on the begging of the file content and section name for this code is not listed, then, it is MANDATORY add all this source code, from the begging of file content to first enlisted section as BEGINING CODE!!!


PLEASE CHECK IF YOU RECOGNIZE ALL ELEMENTS THE RIGHT WAY
PLEASE CHEK IF YOU ENLISTED ELEMENTS THAT ARE NOT EXPLICLTLY ENLISTED
PLEASE CHEK IF YOU RECOGNIZE PROCEDURES AND SECTIONS RIGHT WAY
PLEASE CHEK IF YOU INCLUDE ALL ELEMENTS
PLEASE INCLUDE FULL LAST SECTION SOURCE CODE REGARDLESS IF IT IS TOO LONG
PLEASE INCLUDE BEGGINING SOURCE CODE



Output should look like this:

{
  "begining_code":"",
  "file_meta_info": {
    "identification_division": {
        "general_info": "",
        "program_id": "",
        "program_name": "",
        "author": ""
    },
    "environment_division": {
        "general_info": "",
        "sections_list": []
    },
    "data_division": {
        "general_info": "",
        "sections_list": []
    },
    "procedure_division": {
      "general_info": "",
      "procedures_list": [
        {
          "sections_list": [{
              "section_name": "",
              "is_section": ""
            },
          ]},
          "procedure_name": "",
          "procedure_code_is_completed": "",
          "is_procedure": "",
          "sections_list": [{
                  "section_name": ""
                  "is_section": "",
                },
              ]},
            ...
            ]
          "declaratives": [
            {
              "declarative_name": "",
              "explanation": "",
              "declarative_type": ""
            },
            ...
          ]
        },
        ...
      ],
      "last_section":{
          "section_name":"",
          "full_last_section_source_code":"",
          "is_section_code_completed":""
      }
    }
  }
}
"""

COBOL_FILE_META_EXTRACTION_TEMPLATE_V1 = """
For this given cobol file content : 

$cobol_code 

Extract information below:

IDENTIFICATION DIVISION: [extract all relevant IDENTIFICATION DIVISION  info and enlist all subdivisions with its values]
    usual subsections:
    PROGRAM-ID: [extract PROGRAM ID]
    program name: [extract program name]
    author: [export author]
    please check if there more subsections for IDENTIFICATION DIVISION and export all relevant info and enlist all subdivisions with its values.
ENVIRONMENT DIVISION: [extract all relevant ENVIRONMENT DIVISION info and enlist all subdivisions with its values]
    usual subsections:
    CONFIGURATION SECTION: [extract all relevant CONFIGURATION SECTION info and enlist all subdivisions with its values]
    INPUT-OUTPUT SECTION: [extract all relevant INPUT-OUTPUT SECTION info and enlist all subdivisions with its values]
        FILE-CONTROL: [extract all relevant FILE-CONTROL info and enlist all subdivisions with its values]
        I-O-CONTROL: [extract all relevant I-O-CONTROL info and enlist all subdivisions with its values]
        please check if there more subsections for ENVIRONMENT DIVISION and export all relevant info and enlist all subdivisions with its values.
DATA DIVISION: [extract all relevant DATA DIVISION info and enlist all subdivisions with its values]
    usual subsections:
    FILE SECTION: [extract all relevant FILE SECTION info and enlist all subdivisions with its values]
        FD: [extract value (File Description) entry provides the details about the file, including its name and record structure.]
        LABEL RECORDS ARE STANDARD: [extract value Indicates that standard label records are used.]
        BLOCK CONTAINS 0 RECORDS: [extract value Specifies the number of records in each block. A value of 0 means no blocking.]
        RECORD CONTAINS 80 CHARACTERS: [extract value Specifies the length of each record.]
        DATA RECORD IS INPUT-RECORD: [extract value Associates the file with the record description (INPUT-RECORD).]
        01: [Level Records The 01 level defines the record structure within the file.]
            Level Fields: [extract fields Define individual fields within the record.]
    WORKING-STORAGE SECTION: [extract all relevant WORKING-STORAGE SECTION info and enlist all subdivisions with its values]
    WORKING-STORAGE VARIABLES: [extract all WORKING-STORAGE variables list with variables names and explanation]
    LOCAL-STORAGE SECTION: [extract all relevant LOCAL-STORAGE SECTION info and enlist all subdivisions with its values]
    LOCAL-STORAGE VARIABLES: [extract all LOCAL-STORAGE variables list with variables names and explanation]
    LINKAGE SECTION: [extract all relevant LINKAGE SECTION info and enlist all subdivisions with its values]
    LINKAGE SECTION VARIABLES: [extract and enlist all variables with its name and explanation]
    COMMUNICATION SECTION: [extract all relevant COMMUNICATION SECTION info and enlist all subdivisions with its values]
        LENGTH: [extract value The length of the message.]
        STATUS: [extract value A status variable to hold the result of communication operations.]
        QUEUE: [extract value The name of the queue used for communication.]
        MESSAGE-STATUS: [extract value A variable to store the status code after sending or receiving a message.]
        QUEUE-NAME: [extract value The name of the queue to which messages are sent or from which messages are received.]
        MESSAGE-AREA: [extract value The area in memory where the message content is stored.]
    REPORT SECTION: [extract all relevant REPORT SECTION info and enlist all subdivisions with its values]

        RD: [(Report Description) Entry]
            PAGE LIMIT 60 LINES: [extract value Specifies the number of lines per page.]
            FIRST DETAIL 10: [extract value The first detail line starts at line 10.]
            LAST DETAIL 50: [extract value The last detail line ends at line 50.]
            CONTROLS ARE DEPARTMENT: [extract value Indicates that the report is controlled by the DEPARTMENT field.]

        01: [Level Report Group]
            TYPE PAGE HEADING: [extract value Defines the layout for the page heading.]
            TYPE DETAIL: [extract value Defines the layout for the detail lines.]
            TYPE SUMMARY: [extract value Defines the layout for summary lines at the end of the report.]

    SCREEN SECTION: [extract all relevant SCREEN SECTION info and enlist all subdivisions with its values]

        BLANK SCREEN: [extract value Clears the screen before displaying new content.]
        LINE and COLUMN: [extract value Specifies the position of text and fields on the screen.]
        VALUE: [extract value Displays a static text on the screen.]
        PIC and USING: [extract all input fields and variables.]

    please check if there more subsections for DATA DIVISION and export all relevant info and enlist all subdivisions with its values.
PROCEDURE DIVISION: [extract all relevant PROCEDURE DIVISION info and enlist all subdivisions]
    usual subsections:
    PROCEDUREDS LIST: !!!It is MANDATORY to extract list of ALL PROCEDURES implemented in code !!! with informations below provided: 
        procedure name: [procedure defined name]
        procedure code explanation Summary: [Brief summary or key points of procedure code implementation]
        procedure code full explanation: [Key points of procedure code implementation]
        procedure code feature explanation Summary: [Brief summary this procedure code role and function and value ot brings]
        procedure code feature explanation: [This procedure code role and function and value ot brings]
        procedure explicit inputs and outputs:[explicitly used procedure inputs and outputs, enlist all values and its explanation]
        procedure implicit inputs and outputs:[implicitly used procedure inputs and outputs, global variables, enlist all values and its explanation]
        procedure code is completed: [is this procedure code completed, True/False]
        procedure dependencies:[List of all procedures with their input variables called from current procedure]
        procedure edge cases:[List of edge cases covered by procedure]
        sections list: []
                section name: [section defined name]
                section source code: [Full cobol source code of the section]
                section code explanation Summary: [Brief summary or key points of section code implementation]
                section code full explanation: [Key points of section code implementation]
                section code feature explanation Summary: [Brief summary this section code role and function and value ot brings]
                section code feature explanation: [This section code role and function and value ot brings]
                section explicit inputs and outputs:[explicitly used section inputs and outputs, enlist all values and its explanation]
                section implicit inputs and outputs:[implicitly used section inputs and outputs, global variables, enlist all values and its explanation]
                section dependencies:[List of all section with their input variables called from current section]
                section paragraphs:[List of all section with their input variables called from current section]
                    paragraph sentences:[List of all paragraph sentences with explanation field and is this sentence code completed field, ends with dot, True/False]
                section sentences:[List of all section sentences with explanation field and is this sentence code completed field, ends with dot, True/False]
                section edge cases:[List of edge cases covered by section]
                    Paragraphs: [list of paragraph of section, a paragraph is a named block of code that performs a specific task.]
        DECLARATIVES: [extract all relevant DECLARATIVES info and enlist all subdivisions with its values
            declaratives types:
                ERROR-HANDLING SECTION: [A section named for handling errors.]
                USE AFTER STANDARD ERROR PROCEDURE ON INPUT-FILE: [Specifies that the code in ERROR-PARA should be executed after a standard error on INPUT-FILE.]
                ERROR-PARA:[ A paragraph that handles the error by displaying a message, performing termination steps, and stopping the program.]]

    please check if there more subsections for PROCEDURE DIVISION and export all relevant info and enlist all subdivisions.

PROCEDUREDS LIST: !!!It is MANDATORY to extract ALL IMPLEMENTED PROCEDURES list with all procedure fields filled up.
PROCEDUREDS LIST: !!!It is MOST IMORTANT to extract list of ALL IMPLEMENTED PROCEDURES list with all procedure fields filled up.

PROCEDURE SECTIONS LIST: !!!It is MANDATORY to extract ALL IMPLEMENTED SECTIONS FOR EVERY PROCEDURE list with all section fields filled up for every single procedure.
PROCEDURE SECTIONS LIST: !!!It is MOST IMORTANT to extract list of ALL IMPLEMENTED SECTIONS FOR EVERY PROCEDURE list with all section fields filled up for every single procedure.

!!!It is MANDATORY to include ALL PROCEDURES AND ALL SECTIONS!!!

Output should look like this:

{
  "file_meta_info": {
    "identification_division": {
      "general_info": "",
      "program_id": "",
      "program_name": "",
      "author": ""
    },
    "environment_division": {
      "general_info": "",
      "configuration_section": "",
      "input_output_section": {
        "general_info": "",
        "file_control": "",
        "io_control": ""
      }
    },
    "data_division": {
      "general_info": "",
      "file_section": {
        "fd": "",
        "label_records_are_standard": "",
        "block_contains_0_records": "",
        "record_contains_80_characters": "",
        "data_record_is_input_record": "",
        "01": []
      },
      "working_storage_section": {
        "general_info": "",
        "working_storage_variables_list": [
          {
            "variable_name": "",
            "variable_type": "",
            "variable_explanation": ""
          }
        ]
      },
      "local_storage_section": {
        "general_info": "",
        "local_storage_variables_list": []
      },
      "linkage_section": {
        "general_info": "",
        "linkage_variables_list": []
      },
      "communication_section": {
        "general_info": "",
        "length": "",
        "status": "",
        "queue": "",
        "message_status": "",
        "queue_name": "",
        "message_area": ""
      },
      "report_section": {
        "rd": {
          "page_limit_60_lines": "",
          "first_detail_10": "",
          "last_detail_50": "",
          "controls_are_department": ""
        },
        "01": {
          "type_page_heading": "",
          "type_detail": "",
          "type_summary": ""
        }
      },
      "screen_section": {
        "blank_screen": "",
        "line_and_column": "",
        "value": "",
        "pic_and_using": []
      }
    },
    "procedure_division": {
      "general_info": "",
      "procedures_list": [
        {
          "procedure_name": "",
          "procedure_code_explanation_summary": "",
          "procedure_code_full_explanation": "",
          "procedure_code_feature_explanation_summary": "",
          "procedure_code_feature_explanation": "",
          "procedure_code_is_completed": "",
          "procedure_explicit_inputs": [
            {
              "variable_name": "",
              "variable_explanation": ""
            },
            ...
          ],
          "procedure_explicit_outputs": [
            {
              "variable_name": "",
              "variable_explanation": ""
            },
            ...
          ],
          "procedure_implicit_inputs": [
            {
              "variable_name": "",
              "variable_explanation": ""
            },
            ...
          ],
          "procedure_implicit_outputs": [
            {
              "variable_name": "",
              "variable_explanation": ""
            },
            ...
          ],
          "procedure_dependencies": [
            {
              "procedure_name": "",
              "procedure_inputs": [
                {
                  "variable_name": "",
                  "variable_explanation": ""
                },
                ...
              ],
              "procedure_outputs": [
                {
                  "variable_name": "",
                  "variable_explanation": ""
                },
                ...
              ]
            },
            ...
          ],
          "procedure_edge_cases": [
            {
              "code_implementation": "",
              "explanation": ""
            },
            ...
          ],
          "sections_list": [{
              "section_name": "",
              "section_source_code": "",
              "section_code_explanation_summary": "",
              "section_code_full_explanation": "",
              "section_code_feature_explanation_summary": "",
              "section_code_feature_explanation": "",
              "section_paragraphs": [
                {
                  "variable_name": "",
                  "variable_explanation": ""
                  "paragraphs_sentences": [
                    {
                      "variable_name": "",
                      "variable_explanation": ""
                    },
                    ...
                  ],
                },
                ...
              ],
              "section_sentences": [
                {
                  "variable_name": "",
                  "variable_explanation": ""
                },
                ...
              ],
              "section_explicit_inputs": [
                {
                  "variable_name": "",
                  "variable_explanation": ""
                },
                ...
              ],
              "section_explicit_outputs": [
                {
                  "variable_name": "",
                  "variable_explanation": ""
                },
                ...
              ],
              "section_implicit_inputs": [
                {
                  "variable_name": "",
                  "variable_explanation": ""
                },
                ...
              ],
              "section_implicit_outputs": [
                {
                  "variable_name": "",
                  "variable_explanation": ""
                },
                ...
              ],
              "section_dependencies": [
                {
                  "section_name": "",
                  "section_inputs": [
                    {
                      "variable_name": "",
                      "variable_explanation": ""
                    },
                    ...
                  ],
                  "section_outputs": [
                    {
                      "variable_name": "",
                      "variable_explanation": ""
                    },
                    ...
                  ]
                },
              ],
              "section_edge_cases": [
                {
                  "code_implementation": "",
                  "explanation": ""
                },
                ...
          ]},
            ...
            ],
          "declaratives": [
            {
              "code_implementation": "",
              "explanation": "",
              "declarative_type": ""
            },
            ...
          ]
        },
        ...
      ]
    }
  }
}
"""


COBOL_FILE_CONTENT_EXTRACTION_TEMPLATE_V1 = """
For this given cobol file content : 

$cobol_code 

Extract information below:

IDENTIFICATION DIVISION: [extract all relevant IDENTIFICATION DIVISION  info and enlist all subdivisions with its values]
    usual subsections:
    PROGRAM-ID: [extract PROGRAM ID]
    program name: [extract program name]
    author: [export author]
    please check if there more subsections for IDENTIFICATION DIVISION and export all relevant info and enlist all subdivisions with its values.
ENVIRONMENT DIVISION: [extract all relevant ENVIRONMENT DIVISION info and enlist all subdivisions with its values]
    usual subsections:
    CONFIGURATION SECTION: [extract all relevant CONFIGURATION SECTION info and enlist all subdivisions with its values]
    INPUT-OUTPUT SECTION: [extract all relevant INPUT-OUTPUT SECTION info and enlist all subdivisions with its values]
        FILE-CONTROL: [extract all relevant FILE-CONTROL info and enlist all subdivisions with its values]
        I-O-CONTROL: [extract all relevant I-O-CONTROL info and enlist all subdivisions with its values]
        please check if there more subsections for ENVIRONMENT DIVISION and export all relevant info and enlist all subdivisions with its values.
DATA DIVISION: [extract all relevant DATA DIVISION info and enlist all subdivisions with its values]
    usual subsections:
    FILE SECTION: [extract all relevant FILE SECTION info and enlist all subdivisions with its values]
        FD: [extract value (File Description) entry provides the details about the file, including its name and record structure.]
        LABEL RECORDS ARE STANDARD: [extract value Indicates that standard label records are used.]
        BLOCK CONTAINS 0 RECORDS: [extract value Specifies the number of records in each block. A value of 0 means no blocking.]
        RECORD CONTAINS 80 CHARACTERS: [extract value Specifies the length of each record.]
        DATA RECORD IS INPUT-RECORD: [extract value Associates the file with the record description (INPUT-RECORD).]
        01: [Level Records The 01 level defines the record structure within the file.]
            Level Fields: [extract fields Define individual fields within the record.]
    WORKING-STORAGE SECTION: [extract all relevant WORKING-STORAGE SECTION info and enlist all subdivisions with its values]
    WORKING-STORAGE VARIABLES: [extract all WORKING-STORAGE variables list with variables names and explanation]
    LOCAL-STORAGE SECTION: [extract all relevant LOCAL-STORAGE SECTION info and enlist all subdivisions with its values]
    LOCAL-STORAGE VARIABLES: [extract all LOCAL-STORAGE variables list with variables names and explanation]
    LINKAGE SECTION: [extract all relevant LINKAGE SECTION info and enlist all subdivisions with its values]
    LINKAGE SECTION VARIABLES: [extract and enlist all variables with its name and explanation]
    COMMUNICATION SECTION: [extract all relevant COMMUNICATION SECTION info and enlist all subdivisions with its values]
        LENGTH: [extract value The length of the message.]
        STATUS: [extract value A status variable to hold the result of communication operations.]
        QUEUE: [extract value The name of the queue used for communication.]
        MESSAGE-STATUS: [extract value A variable to store the status code after sending or receiving a message.]
        QUEUE-NAME: [extract value The name of the queue to which messages are sent or from which messages are received.]
        MESSAGE-AREA: [extract value The area in memory where the message content is stored.]
    REPORT SECTION: [extract all relevant REPORT SECTION info and enlist all subdivisions with its values]
    
        RD: [(Report Description) Entry]
            PAGE LIMIT 60 LINES: [extract value Specifies the number of lines per page.]
            FIRST DETAIL 10: [extract value The first detail line starts at line 10.]
            LAST DETAIL 50: [extract value The last detail line ends at line 50.]
            CONTROLS ARE DEPARTMENT: [extract value Indicates that the report is controlled by the DEPARTMENT field.]

        01: [Level Report Group]
            TYPE PAGE HEADING: [extract value Defines the layout for the page heading.]
            TYPE DETAIL: [extract value Defines the layout for the detail lines.]
            TYPE SUMMARY: [extract value Defines the layout for summary lines at the end of the report.]
    
    SCREEN SECTION: [extract all relevant SCREEN SECTION info and enlist all subdivisions with its values]
    
        BLANK SCREEN: [extract value Clears the screen before displaying new content.]
        LINE and COLUMN: [extract value Specifies the position of text and fields on the screen.]
        VALUE: [extract value Displays a static text on the screen.]
        PIC and USING: [extract all input fields and variables.]
    
    please check if there more subsections for DATA DIVISION and export all relevant info and enlist all subdivisions with its values.
PROCEDURE DIVISION: [extract all relevant PROCEDURE DIVISION info and enlist all subdivisions]
    usual subsections:
    PROCEDUREDS LIST: !!!It is MANDATORY to extract list of ALL PROCEDURES implemented in code !!! with informations below provided: 
        procedure name: [procedure defined name]
        procedure code explanation Summary: [Brief summary or key points of procedure code implementation]
        procedure code full explanation: [Key points of procedure code implementation]
        procedure code feature explanation Summary: [Brief summary this procedure code role and function and value ot brings]
        procedure code feature explanation: [This procedure code role and function and value ot brings]
        procedure explicit inputs and outputs:[explicitly used procedure inputs and outputs, enlist all values and its explanation]
        procedure implicit inputs and outputs:[implicitly used procedure inputs and outputs, global variables, enlist all values and its explanation]
        procedure code is completed: [is this procedure code completed, True/False]
        procedure dependencies:[List of all procedures with their input variables called from current procedure]
        procedure edge cases:[List of edge cases covered by procedure]
        sections list: []
                section name: [section defined name]
                section source code: [Full cobol source code of the section]
                section code explanation Summary: [Brief summary or key points of section code implementation]
                section code full explanation: [Key points of section code implementation]
                section code feature explanation Summary: [Brief summary this section code role and function and value ot brings]
                section code feature explanation: [This section code role and function and value ot brings]
                section explicit inputs and outputs:[explicitly used section inputs and outputs, enlist all values and its explanation]
                section implicit inputs and outputs:[implicitly used section inputs and outputs, global variables, enlist all values and its explanation]
                section dependencies:[List of all section with their input variables called from current section]
                section paragraphs:[List of all section with their input variables called from current section]
                    paragraph sentences:[List of all paragraph sentences with explanation field and is this sentence code completed field, ends with dot, True/False]
                section sentences:[List of all section sentences with explanation field and is this sentence code completed field, ends with dot, True/False]
                section edge cases:[List of edge cases covered by section]
                    Paragraphs: [list of paragraph of section, a paragraph is a named block of code that performs a specific task.]
        DECLARATIVES: [extract all relevant DECLARATIVES info and enlist all subdivisions with its values
            declaratives types:
                ERROR-HANDLING SECTION: [A section named for handling errors.]
                USE AFTER STANDARD ERROR PROCEDURE ON INPUT-FILE: [Specifies that the code in ERROR-PARA should be executed after a standard error on INPUT-FILE.]
                ERROR-PARA:[ A paragraph that handles the error by displaying a message, performing termination steps, and stopping the program.]]

    please check if there more subsections for PROCEDURE DIVISION and export all relevant info and enlist all subdivisions.

PROCEDUREDS LIST: !!!It is MANDATORY to extract ALL IMPLEMENTED PROCEDURES list with all procedure fields filled up.
PROCEDUREDS LIST: !!!It is MOST IMORTANT to extract list of ALL IMPLEMENTED PROCEDURES list with all procedure fields filled up.

PROCEDURE SECTIONS LIST: !!!It is MANDATORY to extract ALL IMPLEMENTED SECTIONS FOR EVERY PROCEDURE list with all section fields filled up for every single procedure.
PROCEDURE SECTIONS LIST: !!!It is MOST IMORTANT to extract list of ALL IMPLEMENTED SECTIONS FOR EVERY PROCEDURE list with all section fields filled up for every single procedure.

!!!It is MANDATORY to include ALL PROCEDURES AND ALL SECTIONS!!!

Output should look like this:

{
  "file_meta_info": {
    "identification_division": {
      "general_info": "",
      "program_id": "",
      "program_name": "",
      "author": ""
    },
    "environment_division": {
      "general_info": "",
      "configuration_section": "",
      "input_output_section": {
        "general_info": "",
        "file_control": "",
        "io_control": ""
      }
    },
    "data_division": {
      "general_info": "",
      "file_section": {
        "fd": "",
        "label_records_are_standard": "",
        "block_contains_0_records": "",
        "record_contains_80_characters": "",
        "data_record_is_input_record": "",
        "01": []
      },
      "working_storage_section": {
        "general_info": "",
        "working_storage_variables_list": [
          {
            "variable_name": "",
            "variable_type": "",
            "variable_explanation": ""
          }
        ]
      },
      "local_storage_section": {
        "general_info": "",
        "local_storage_variables_list": []
      },
      "linkage_section": {
        "general_info": "",
        "linkage_variables_list": []
      },
      "communication_section": {
        "general_info": "",
        "length": "",
        "status": "",
        "queue": "",
        "message_status": "",
        "queue_name": "",
        "message_area": ""
      },
      "report_section": {
        "rd": {
          "page_limit_60_lines": "",
          "first_detail_10": "",
          "last_detail_50": "",
          "controls_are_department": ""
        },
        "01": {
          "type_page_heading": "",
          "type_detail": "",
          "type_summary": ""
        }
      },
      "screen_section": {
        "blank_screen": "",
        "line_and_column": "",
        "value": "",
        "pic_and_using": []
      }
    },
    "procedure_division": {
      "general_info": "",
      "procedures_list": [
        {
          "procedure_name": "",
          "procedure_code_explanation_summary": "",
          "procedure_code_full_explanation": "",
          "procedure_code_feature_explanation_summary": "",
          "procedure_code_feature_explanation": "",
          "procedure_code_is_completed": "",
          "procedure_explicit_inputs": [
            {
              "variable_name": "",
              "variable_explanation": ""
            },
            ...
          ],
          "procedure_explicit_outputs": [
            {
              "variable_name": "",
              "variable_explanation": ""
            },
            ...
          ],
          "procedure_implicit_inputs": [
            {
              "variable_name": "",
              "variable_explanation": ""
            },
            ...
          ],
          "procedure_implicit_outputs": [
            {
              "variable_name": "",
              "variable_explanation": ""
            },
            ...
          ],
          "procedure_dependencies": [
            {
              "procedure_name": "",
              "procedure_inputs": [
                {
                  "variable_name": "",
                  "variable_explanation": ""
                },
                ...
              ],
              "procedure_outputs": [
                {
                  "variable_name": "",
                  "variable_explanation": ""
                },
                ...
              ]
            },
            ...
          ],
          "procedure_edge_cases": [
            {
              "code_implementation": "",
              "explanation": ""
            },
            ...
          ],
          "sections_list": [{
              "section_name": "",
              "section_source_code": "",
              "section_code_explanation_summary": "",
              "section_code_full_explanation": "",
              "section_code_feature_explanation_summary": "",
              "section_code_feature_explanation": "",
              "section_paragraphs": [
                {
                  "variable_name": "",
                  "variable_explanation": ""
                  "paragraphs_sentences": [
                    {
                      "variable_name": "",
                      "variable_explanation": ""
                    },
                    ...
                  ],
                },
                ...
              ],
              "section_sentences": [
                {
                  "variable_name": "",
                  "variable_explanation": ""
                },
                ...
              ],
              "section_explicit_inputs": [
                {
                  "variable_name": "",
                  "variable_explanation": ""
                },
                ...
              ],
              "section_explicit_outputs": [
                {
                  "variable_name": "",
                  "variable_explanation": ""
                },
                ...
              ],
              "section_implicit_inputs": [
                {
                  "variable_name": "",
                  "variable_explanation": ""
                },
                ...
              ],
              "section_implicit_outputs": [
                {
                  "variable_name": "",
                  "variable_explanation": ""
                },
                ...
              ],
              "section_dependencies": [
                {
                  "section_name": "",
                  "section_inputs": [
                    {
                      "variable_name": "",
                      "variable_explanation": ""
                    },
                    ...
                  ],
                  "section_outputs": [
                    {
                      "variable_name": "",
                      "variable_explanation": ""
                    },
                    ...
                  ]
                },
              ],
              "section_edge_cases": [
                {
                  "code_implementation": "",
                  "explanation": ""
                },
                ...
          ]},
            ...
            ],
          "declaratives": [
            {
              "code_implementation": "",
              "explanation": "",
              "declarative_type": ""
            },
            ...
          ]
        },
        ...
      ]
    }
  }
}
"""

DOCUMENT_SYSTEM_MSG_QUESTION_STATEMENT_V1 = """
You are expert for clinical trial research and you should check if given response is correct.
"""

QUESTION_STATEMENT_PROMPT_TEMPLATE_V1 = """
Formulate this question as a statement:
$question 
"""

THREE_QUESTION_STATEMENTS_PROMPT_TEMPLATE_V1 = """
Formulate given question as a statement in three different ways. 
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

class CobolExtractionPromptTemplateCreator:

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

    def get_title_extract_prompt(self, document_split: str) -> str:
        user_prompt = self.prepare_template(TITLE_TEMPLATE, document_split=document_split)
        return user_prompt

    def get_query_based_text_compression_prompt(self, query: str, document_split: str) -> str:
        user_prompt = self.prepare_template(QUERY_BASED_COMPRESSION_TEMPLATE_V1, query=query,
                                            text_to_compress=document_split)
        return user_prompt

    def get_three_question_statements(self, question: str) -> str:
        user_prompt = self.prepare_template(THREE_QUESTION_STATEMENTS_PROMPT_TEMPLATE_V1, question=question)
        return user_prompt

    def get_question_related_information(self, question: str, section_text: str) -> str:
        user_prompt = self.prepare_template(QUESTION_RELATED_INFORMATION_PROMPT_TEMPLATE_V1,
                                            question=question,
                                            section_text=section_text)
        return user_prompt

    def get_document_text_compression_prompt(self, document_split: str) -> str:
        user_prompt = self.prepare_template(DOCUMENT_COMPRESSION_TEMPLATE_V2, text_to_compress=document_split)
        return user_prompt

    def get_document_text_compression_check_prompt(self, document_split: str, previous_response: str) -> str:
        user_prompt = self.prepare_template(DOCUMENT_COMPRESSION_CHECK_TEMPLATE_V1,
                                            text_to_compress=document_split,
                                            previous_response=previous_response)
        return user_prompt

    def get_extract_cobol_code_chunk_prompt(self, new_code_chunk, last_previous_code_section) -> str:
        code_chunk = new_code_chunk + " " + last_previous_code_section
        user_prompt = self.prepare_template(COBOL_FILE_CONTENT_EXTRACTION_TEMPLATE_V1,
                                            cobol_code=code_chunk)
        return user_prompt

    def get_extract_cobol_code_chunk_info_prompt(self, division_name, code_chunk) -> str:
        user_prompt = ""
        if "IDENTIFICATION" in division_name:
            user_prompt = self.prepare_template(COBOL_IDENTIFICATION_DIVISION_V1,cobol_code=code_chunk)
        elif  "ENVIRONMENT" in division_name:
            user_prompt = self.prepare_template(COBOL_ENVIRONMENT_DIVISION_V1, cobol_code=code_chunk)
        elif "DATA" in division_name:
            user_prompt = self.prepare_template(COBOL_DATA_DIVISION_V1, cobol_code=code_chunk)
        elif "PROCEDURE" in division_name:
            user_prompt = self.prepare_template(COBOL_PROCEDURE_DIVISION_V1, cobol_code=code_chunk)
        return user_prompt


    def get_summarize_dependencies_info_prompt(self, current_cobol_code_extraction,
                                               children_description_extraction_list,
                                               dependencies_description_extraction_list) -> str:
        user_prompt = self.prepare_template(ADD_DEPENDENCIES_SUMMARIZATION_V1,
                                                    current_cobol_code_extraction=current_cobol_code_extraction,
                                                    children_description_extraction_list=children_description_extraction_list,
                                                    dependencies_description_extraction_list=dependencies_description_extraction_list)
        return user_prompt

    def get_frd_prompt(self, cobol_project_description) -> str:
        user_prompt = self.prepare_template(FRD_V1,cobol_project_description=cobol_project_description)
        return user_prompt
