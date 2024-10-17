import json

from pydantic import BaseModel
from string import Template

class Step(BaseModel):
    '''Required steps to answer the question.'''
    explanation: str

class ChainOfThought(BaseModel):
    '''Final answer with the list of steps.'''
    steps: list[Step]
    final_answer: str


generation_args = {
    "temp": 0.1,
    "repetition_penalty": 1.2,
    "repetition_context_size": 20,
    "top_p": 0.95,
}

STRUCTURED_OUTPUT_SYSTEM_PROMPT = """
You are a bot that ONLY responds with an instance of JSON without any additional information. 
You have access to a JSON schema, which will determine how the JSON should be structured.
Respond only with valid JSON. Do not write an introduction or summary."""

system_message = """
            Extract coherent text chunks directly from the specified page based on semantic similarity.
            Retain only existing titles for each chunk without modifying the text and generating new titles.
            """


human_message = """
            Please split page text into semantic chunks.
            Create output in json format {{num: int, chunk_text: str}}
            Do not add or delete anything.

            {page}

            """




class LlamaStructuredPromptCreator:


    def get_generate_json_structured_output_prompt_v1(self,
                                                  system_msg: str = STRUCTURED_OUTPUT_SYSTEM_PROMPT,
                                                  user_prompt: str = "",
                                                  structured_output_model: BaseModel = None):
        schema = json.dumps(structured_output_model.model_json_schema().get("required", None))

        prompt = f"""
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>
        
        {system_msg}<|eot_id|>
        
        <|start_header_id|>user<|end_header_id|>
        Make sure to return ONLY an instance of the JSON, NOT the schema itself. Do not add any additional information.
        JSON schema:
        {schema}
        
        Task: {user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """
        return prompt


# probati srpski
# probati engleski

    def get_generate_json_structured_output_prompt_v2(self,
                                                   system_msg: str = STRUCTURED_OUTPUT_SYSTEM_PROMPT,
                                                   user_prompt: str = "",
                                                   structured_output_model: BaseModel = None):
        schema = json.dumps(structured_output_model.model_json_schema().get("required", None))

        """
        Respond only with valid JSON. Do not write an introduction or summary.
        """

        """<|start_header_id|>system<|end_header_id|>

            The user an inventory of different products. For the following text, 
            write only a JSON document containing how the inventory has changed 
            by the user's actions. Be very concise and output only the JSON data
            <|eot_id|><|start_header_id|>user<|end_header_id|>
            
            used 2 pounds of wax to make 16 candles
            
            <|start_header_id|>assistant<|end_header_id|>JSON:
            
            Or if they really are attached to "instruction, input, response", 
            they could use those in place of "system, user, assistant" 
            and I expect the model would perform just fine. 
        """

        LLAMA_JSON_STRUCTURED_OUTPUT = """
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>

        $system_msg<|eot_id|>

        <|start_header_id|>user<|end_header_id|>
        Make sure to return ONLY an instance of the JSON, NOT the schema itself. 
        Do not add any additional information.
        JSON schema:
        $schema

        Task: $user_prompt<|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """

        user_prompt = self.prepare_template(LLAMA_JSON_STRUCTURED_OUTPUT, system_msg=system_msg, schema=schema,user_prompt=user_prompt )

        return user_prompt

    def get_generate_json_structured_output_prompt_v3(self,
                                                   system_msg: str = STRUCTURED_OUTPUT_SYSTEM_PROMPT,
                                                   user_prompt: str = "",
                                                   structured_output_model: BaseModel = None):

        LLAMA_JSON_STRUCTURED_OUTPUT = """
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>

        $system_msg<|eot_id|>

        <|start_header_id|>user<|end_header_id|>
        Make sure to return ONLY an instance of the JSON, NOT the schema itself. 
        Do not add any additional information.

        JSON schema:
        [
          {
            "language": "Romani",
            "word": "Džavipen"
          },
          {
            "language": "Romani",
            "word": "bajrarikeribaskoro"
          },...]


        Task: $user_prompt<|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """

        user_prompt = self.prepare_template(LLAMA_JSON_STRUCTURED_OUTPUT, system_msg=system_msg,
                                            user_prompt=user_prompt)

        return user_prompt



    def get_generate_json_structured_output_prompt(self,
                                                   system_msg: str = STRUCTURED_OUTPUT_SYSTEM_PROMPT,
                                                   user_prompt: str = "",
                                                   structured_output_model: BaseModel = None):

        LLAMA_JSON_STRUCTURED_OUTPUT = """
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>

        $system_msg<|eot_id|>

        <|start_header_id|>user<|end_header_id|>
        Make sure to return ONLY an instance of the JSON, NOT the schema itself. 
        Do not add any additional information.
        
        JSON schema:
        [
          {
            "language": "Romani",
            "words_list": ["Džavipen", ...]
          },
          {
            "language": "Romani",
            "words_list": ["bajrarikeribaskoro, ..."]
          },...]


        Task: $user_prompt<|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """

        user_prompt = self.prepare_template(LLAMA_JSON_STRUCTURED_OUTPUT, system_msg=system_msg,
                                            user_prompt=user_prompt)

        return user_prompt


    def get_masking_prompt(self, masked_sentence):

        # prompt = f"""
        # Please create export as json format list containing words in Romani language
        # that should replace [MASK] words:  {masked_sentence}"""

        prompt = f"""
        Please create export as json format list containing words in Romani language
        that should replace [MASK] words. For every single masked word, please provide
        list of TOP 5 candidate words that can replace [MASK]:  
        {masked_sentence}"""
        return prompt


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
