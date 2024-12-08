from llm.workflow import workflow

compiled_workflow = workflow.compile()

class LLMApp:

    def __init__(self):
        self.__llm_app = compiled_workflow
        self.__result = None

    def invoke(self, input: dict, **kwargs):
        user_input = input or kwargs
        self.__result = self.__llm_app.invoke(user_input)
        return self

    async def ainvoke(self, input: dict, **kwargs):
        user_input = input or kwargs
        self.__result = await self.__llm_app.ainvoke(user_input)
        return self
    
    @property
    def result(self):
        return self.__result
        
