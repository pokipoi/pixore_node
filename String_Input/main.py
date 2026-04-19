"""
String Input Node
提供一个文本输入框, 并在输出口输出字符串值。
"""

class StringInputNode:
    """节点：只包含一个字符串输入框和一个字符串输出口。"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "在此输入文本..."
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "process"
    CATEGORY = "Inputs"
    OUTPUT_NODE = False

    def process(self, text):
        """直接把输入文本传递到输出。"""
        if text is None:
            text = ""
        return (text,)


# 节点注册映射
NODE_CLASS_MAPPINGS = {
    "String_Input": StringInputNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "String_Input": "String Input"
}
