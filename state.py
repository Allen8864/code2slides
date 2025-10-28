from pydantic import BaseModel
from typing import Optional, Dict, Any

class Config(BaseModel):
    storyboard_model: str = "anthropic/claude-sonnet-4.5"
    code_model: str = "anthropic/claude-sonnet-4.5"
    storyboard_prompt_version: str = "v1"
    code_prompt_version: str = "v1"
    max_retries: int = 3

class GraphState(BaseModel):
    topic: str
    example: str = ""
    storyboard: str = ""
    code: str = ""
    stderr:str = ""
    config: Config = Config()
    current_path: Optional[str] = None  # 当前尝试的路径
    retry_count: int = 0  # 修复错误的次数