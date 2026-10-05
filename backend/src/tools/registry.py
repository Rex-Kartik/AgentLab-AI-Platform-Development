from typing import Dict, List, Any
from .interfaces import Tool
from src.core.errors import ToolNotFoundError

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        self._tools[tool.id] = tool

    def unregister(self, tool_id: str):
        if tool_id in self._tools:
            del self._tools[tool_id]

    def get_tool(self, tool_id: str) -> Tool:
        tool = self._tools.get(tool_id)
        if not tool:
            raise ToolNotFoundError(tool_id)
        return tool

    def get_available_tools(self) -> List[Tool]:
        return list(self._tools.values())

    def get_all_schemas(self) -> List[Dict[str, Any]]:
        return [tool.get_schema() for tool in self._tools.values()]
    
    def get_ui_metadata(self) -> List[Dict[str, Any]]:
        return [{
            "id": tool.id,
            "name": tool.name,
            "description": tool.description,
            "category": tool.category,
            "icon": tool.ui_config.icon,
            "accentColor": tool.ui_config.accent_color
        } for tool in self._tools.values()]

    def discover_custom_tools(self):
        import os
        import importlib.util
        import inspect
        
        custom_dir = os.path.join(os.path.dirname(__file__), "custom")
        if not os.path.exists(custom_dir):
            return
            
        for filename in os.listdir(custom_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                file_path = os.path.join(custom_dir, filename)
                
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    for name, obj in inspect.getmembers(module):
                        if inspect.isclass(obj) and issubclass(obj, Tool) and obj is not Tool:
                            try:
                                self.register(obj())
                                print(f"Auto-registered custom tool: {obj.__name__}")
                            except Exception as e:
                                print(f"Failed to register {obj.__name__}: {e}")

registry = ToolRegistry()
registry.discover_custom_tools()
