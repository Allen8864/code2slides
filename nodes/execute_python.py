import subprocess
import os
from pathlib import Path
from state import GraphState

def execute_python(state: GraphState):
    """
    Execute Python code using manim-slides render command
    Args:
        state (GraphState): The current graph state
    Returns:
        dict: Updated state with execution results
    """
    print("======== Step 3: Executing Python Code ========")
    if not state.current_path:
        return {
            "stderr": "Error: No current_path set in state"
        }
    
    # 获取 example.py 的完整路径
    example_file = Path(state.current_path) / "example.py"
    
    if not example_file.exists():
        return {
            "stderr": f"Error: {example_file} does not exist"
        }
    
    try:
        # 获取当前环境变量的副本
        env = os.environ.copy()
        
        # 确保 PATH 包含常见的 LaTeX 安装路径
        additional_paths = [
            '/usr/local/bin',
            '/usr/local/texlive/2023/bin/universal-darwin',  # macOS TeX Live
            '/usr/local/texlive/2024/bin/universal-darwin',
            '/Library/TeX/texbin',  # macOS MacTeX
            '/opt/homebrew/bin',  # Apple Silicon Homebrew
        ]
        
        current_path = env.get('PATH', '')
        for path in additional_paths:
            if path not in current_path and os.path.exists(path):
                env['PATH'] = f"{path}:{env['PATH']}"
        
        # 运行 manim-slides render 命令
        # -ql: 低质量渲染
        # --media_dir: 指定输出目录到 current_path
        # 在 current_path 目录下执行，所以只需传入相对路径
        result = subprocess.run(
            ["manim-slides", "render", "-ql", "example.py"],
            cwd=state.current_path,
            capture_output=True,
            text=True,
            timeout=300,  # 5 分钟超时
            env=env  # 传递环境变量
        )
        
        # 执行 convert 命令
        subprocess.run(
            ["manim-slides", "convert", "Example", "example.html"],
            cwd=state.current_path,
            capture_output=True,
            text=True,
            timeout=60,  # 1 分钟超时
            env=env  # 传递环境变量
        )
        
        print(result.stderr)
        # 更新 state - 只返回 stderr
        return {
            "stderr": result.stderr
        }
        
    except subprocess.TimeoutExpired:
        return {
            "stderr": "Execution timeout (5 minutes exceeded)"
        }
    except Exception as e:
        return {
            "stderr": f"Execution error: {str(e)}"
        }
