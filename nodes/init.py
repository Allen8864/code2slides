from state import GraphState
from utils import create_output_folder


def init(state: GraphState):
    """
    初始化节点：创建项目文件夹并更新state中的路径
    
    Args:
        state (GraphState): 当前图状态
        
    Returns:
        dict: 包含更新后的current_path的字典
    """
    print("======== Step 0: Initializing Project ========")
    
    # 创建输出文件夹
    output_path, attempt_num = create_output_folder(state, base_dir="CASES")
    
    print(f"Created project folder: {output_path}")
    print(f"Attempt number: {attempt_num}")
    
    # 返回更新后的路径
    return {"current_path": str(output_path)}

