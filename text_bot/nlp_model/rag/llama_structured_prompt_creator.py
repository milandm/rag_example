import json

from pydantic import BaseModel


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

STRUCTURED_OUTPUT_SYSTEM_PROMPT = """You are a bot that ONLY responds with an instance of JSON without any additional information. You have access to a JSON schema, which will determine how the JSON should be structured."""

class LlamaStructuredPromptCreator:


    def get_generate_json_structured_output_prompt(self,
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