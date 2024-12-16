from llm.workflow import workflow

compiled_workflow = workflow.compile()

class LLMApp:

    def __init__(self):
        self.__llm_app = compiled_workflow
        self.__result = None

    def invoke(self, input: dict, **kwargs):
        user_input = input or kwargs
        if not user_input:
            raise ValueError("input is required")
        self.__result = self.__llm_app.invoke(user_input)
        return self.__result

    async def ainvoke(self, input: dict, **kwargs):
        user_input = input or kwargs
        if not user_input:
            raise ValueError("input is required")
        self.__result = await self.__llm_app.ainvoke(user_input)
        return self.__result
    
    @property
    def result(self):
        return self.__result
        
