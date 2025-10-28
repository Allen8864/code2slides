from dotenv import load_dotenv
load_dotenv(dotenv_path=".env", override=True)
from openai import OpenAI
from langsmith import traceable
from langsmith.wrappers import wrap_openai
from state import GraphState
from utils import save_code, save_code_prompt, strip_code_block, load_prompt_template

def generate_code(state: GraphState):
    """
    Generate code based on storyboard
    Args:
        state (GraphState): The current graph state
    Returns:
        dict: Updated state with generated code
    """

    print("======== Step 2: Generating Code ========")
    
    storyboard = state.storyboard
    
    # 动态加载 prompt 模板
    code_prompt = load_prompt_template(
        state.config.code_prompt_version, 
        'code'
    )
    prompt = code_prompt.substitute(storyboard=storyboard)

    client = wrap_openai(OpenAI())
    response =  client.responses.create(
        model=state.config.code_model,
        input=prompt
    )
    code = strip_code_block(response.output_text)
    print(code)
    
    # 保存代码
    if state.current_path:
        save_code(code, state.current_path)
        save_code_prompt(prompt, state.current_path)
    
    return {"code": code}