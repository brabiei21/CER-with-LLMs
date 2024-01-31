from langchain.prompts.prompt import PromptTemplate
# TODO: Implement a parser


def get_generation_prompt():
    template = """
    You are mimicking a customer who is interested in a {product} and the features they are interested in are {features}. Write a convincing paragraph as the customer who inquires about {product} recommendations. Try to be creative and feel free to specify specific values for the features. 

    For the sake of clarification, here is an example:


    {example}
    """

    return PromptTemplate(template=template, input_variables=["product", "features"], partial_variables={"example": get_generation_example()}) 

def get_extraction_prompt():
    template = """
    """

    return PromptTemplate(template=template, input_variables=["input", "lang"],
                          partial_variables={"example": get_extraction_example()})

def get_generation_example():
    return """The customer is interested in a laptop and the features they are interested in are [display size, color, memory size]. 

AI: Hi! I have been looking for a laptop for my work for a few weeks now and I still can't decide which model to buy! I really need something with a big display like 16 inches. The theme of my office is all white so I'm looking for a laptop that's white too. Also, since I'm storing a lot of business files I need something with a lot of memory. Ideally a 2 terabyte laptop. Does anyone know what model laptop I should buy?? 

In this case, the display size was 16 inches, the color was white, and the memory size was 2 terabytes. 
"""

def get_extraction_example():
    return """

"""