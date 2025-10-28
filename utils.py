import os
import json
import re
from pathlib import Path
from state import GraphState
from string import Template


def strip_code_block(text: str) -> str:
    """
    去掉 markdown 代码块标记（```json, ```python, ```等）
    
    Args:
        text: 可能包含代码块标记的文本
        
    Returns:
        清理后的文本
        
    Examples:
        >>> strip_code_block("```json\\n{...}\\n```")
        '{...}'
        >>> strip_code_block("```python\\nprint('hello')\\n```")
        "print('hello')"
    """
    # 匹配开头的 ```language 或 ```
    text = re.sub(r'^```\w*\n?', '', text.strip())
    # 匹配结尾的 ```
    text = re.sub(r'\n?```$', '', text.strip())
    return text.strip()


def load_prompt_template(version: str, prompt_type: str) -> Template:
    """
    根据版本号动态加载 prompt 模板
    
    Args:
        version: prompt 版本号 (e.g., "v1", "v2")
        prompt_type: prompt 类型 ("storyboard" 或 "code")
        
    Returns:
        Template: 加载的 prompt 模板
    """
    # 获取当前文件所在目录的父目录（项目根目录）
    project_root = Path(__file__).parent
    prompt_path = project_root / 'prompts' / f'{prompt_type}_{version}.txt'
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return Template(f.read())


def get_next_attempt_number(state: GraphState, base_dir: str = "CASES") -> int:
    """
    获取下一个尝试次数
    检查已存在的文件夹，找到最大的次数并加1
    """
    base_path = Path(base_dir) / state.topic
    
    if not base_path.exists():
        return 1
    
    # 找到所有数字命名的子文件夹
    max_num = 0
    for item in base_path.iterdir():
        if item.is_dir() and item.name.isdigit():
            num = int(item.name)
            max_num = max(max_num, num)
    
    return max_num + 1


def create_output_folder(state: GraphState, base_dir: str = "CASES") -> tuple[Path, int]:
    """
    创建输出文件夹
    格式: state.topic/次数
    自动获取下一个尝试次数，并更新 state 中的 current_path
    
    Returns:
        (output_path, attempt_num): 输出路径和尝试次数
    """
    attempt_num = get_next_attempt_number(state, base_dir)
    output_path = Path(base_dir) / state.topic / str(attempt_num)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 更新 state 中的路径
    state.current_path = str(output_path)
    
    return output_path, attempt_num


def save_storyboard(storyboard: str, path: str) -> dict:
    """
    保存 storyboard 到文件
    
    Args:
        storyboard: storyboard 内容
        path: 保存路径（文件夹路径）
    
    Returns:
        包含文件路径的字典
    """
    from pathlib import Path
    output_path = Path(path)
    storyboard_file = output_path / "storyboard.txt"
    
    with open(storyboard_file, 'w', encoding='utf-8') as f:
        f.write(storyboard)
    
    return {
        "path": str(storyboard_file),
        "folder": str(output_path)
    }


def save_code(code: str, path: str) -> dict:
    """
    保存 code 到文件
    
    Args:
        code: 代码内容
        path: 保存路径（文件夹路径）
    
    Returns:
        包含文件路径的字典
    """
    from pathlib import Path
    output_path = Path(path)
    code_file = output_path / "example.py"
    
    with open(code_file, 'w', encoding='utf-8') as f:
        f.write(code)
    
    return {
        "path": str(code_file),
        "folder": str(output_path)
    }


def save_config(config_dict: dict, path: str) -> dict:
    """
    保存 config 配置参数到文件
    
    Args:
        config_dict: config 配置字典
        path: 保存路径（文件夹路径）
    
    Returns:
        包含文件路径的字典
    """
    from pathlib import Path
    output_path = Path(path)
    config_file = output_path / "config.json"
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config_dict, f, indent=2, ensure_ascii=False)
    
    return {
        "path": str(config_file),
        "folder": str(output_path)
    }


def save_storyboard_prompt(prompt: str, path: str) -> dict:
    """
    保存 storyboard 生成时使用的 prompt 到文件
    
    Args:
        prompt: storyboard 生成时使用的 prompt 内容
        path: 保存路径（文件夹路径）
    
    Returns:
        包含文件路径的字典
    """
    from pathlib import Path
    output_path = Path(path)
    prompt_file = output_path / "storyboard_prompt.txt"
    
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    return {
        "path": str(prompt_file),
        "folder": str(output_path)
    }


def save_code_prompt(prompt: str, path: str) -> dict:
    """
    保存 code 生成时使用的 prompt 到文件
    
    Args:
        prompt: code 生成时使用的 prompt 内容
        path: 保存路径（文件夹路径）
    
    Returns:
        包含文件路径的字典
    """
    from pathlib import Path
    output_path = Path(path)
    prompt_file = output_path / "code_prompt.txt"
    
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
    
    return {
        "path": str(prompt_file),
        "folder": str(output_path)
    }

