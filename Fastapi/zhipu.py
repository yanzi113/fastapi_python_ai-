import os
from langchain_openai import ChatOpenAI
if __name__ == '__main__':
    # glm4 Model
    glm4_model = ChatOpenAI(
        model_name="gLm-4-air",
        openai_api_base="https://open.bigmodel.cn/api/paas/v4",
        openai_api_key="839815e495bcc411b3005d0a8f8ff15f.sM3vvPVaJLv1y998",
        streaming=True,
        verbose=True,
    )
    for chunk in glm4_model.stream("你好,你是谁？"):
        print('------')
        print(chunk)

    pass
