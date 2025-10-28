from dotenv import load_dotenv

from utils import save_storyboard, save_config, save_storyboard_prompt, strip_code_block, load_prompt_template
load_dotenv(dotenv_path=".env", override=True)
from openai import OpenAI
from langsmith import traceable
from langsmith.wrappers import wrap_openai
from state import GraphState
import json


def generate_storyboard(state: GraphState):
    """
    Generate response
    Args:
        state (dict): The current graph state
    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """

    print("======== Step 1: Generating Storyboard ========")
    topic = state.topic
    example = state.example
    
    # 动态加载 prompt 模板
    storyboard_prompt = load_prompt_template(
        state.config.storyboard_prompt_version, 
        'storyboard'
    )
    prompt = storyboard_prompt.substitute(topic=topic, example=example)

    client = wrap_openai(OpenAI())
    response =  client.responses.create(
        model=state.config.storyboard_model,
        input=prompt
    )
    storyboard = strip_code_block(response.output_text)
    print(storyboard)
    
    # 保存 storyboard 和 config
    if state.current_path:
        save_storyboard(storyboard, state.current_path)
        save_config(state.config.model_dump(), state.current_path)
        save_storyboard_prompt(prompt, state.current_path)

    return {"storyboard": storyboard}
