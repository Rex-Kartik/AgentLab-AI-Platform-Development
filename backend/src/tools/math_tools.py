from pydantic import BaseModel, Field
from src.tools.interfaces import Tool, ToolUIConfig

class MathInput(BaseModel):
    a: float = Field(description="First number")
    b: float = Field(description="Second number")

class AddTool(Tool):
    id = "math_add"
    name = "Add"
    description = "Adds two numbers together."
    category = "compute"
    ui_config = ToolUIConfig(icon="plus", accent_color="#FB923C")
    input_schema = MathInput

    async def execute(self, a: float, b: float, **kwargs) -> float:
        return a + b

class MultiplyTool(Tool):
    id = "math_multiply"
    name = "Multiply"
    description = "Multiplies two numbers together."
    category = "compute"
    ui_config = ToolUIConfig(icon="x", accent_color="#FB923C")
    input_schema = MathInput

    async def execute(self, a: float, b: float, **kwargs) -> float:
        return a * b
