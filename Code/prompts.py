from langchain.prompts.prompt import PromptTemplate


def get_blurb_prompt():
    template = """
    Write a few random sentences from any perspective (i.e. a review, a question, a feedback, etc.) about some product including the following topics:

    {features}

    Specifically with the following values:

    {values}

    Make sure to keep it relatively short and only discuss the topics mention and nothing more. 
    """
    
    # template = '''
    # You are a customer chatting with an agent at an online home improvement store. Write a sentence that includes the following features: {features} and the corresponding values: {values}. 
    # make sure to mention all values that are given.
    # '''

    return PromptTemplate(template=template, input_variables=["features", "values"])

    # you are a customer at a home improvement store, write a senstense
    #You are a customer chatting with an agent at an online home improvement store. Write a sentence that includes...
def get_eval_with_feature_prompt(with_feature=True):
  
    if with_feature:
        template = """
        Given the following, what are the features mentioned about the product? These would be considered all possible features: 
        
        {features}
        
        Text: 
        
        {post}
        
        Format your response like this: 
        
        ATTR1_NAME::ATTR1_VALUE;;
        ATTR2_NAME::ATTR2_VALUE;;
        
        If a feature is not mentioned, just leave it out. In other words, do not include something like ATTR_NAME::;; in your response.
        """
        return PromptTemplate(template=template, input_variables=["features", "post"])
    
    else:
        template = """
        Given the following, what are the features mentioned about the product? 
        
        Text: 
        
        {post}
        
        Format your response like this: 
        
        ATTR1_NAME::ATTR1_VALUE;;
        ATTR2_NAME::ATTR2_VALUE;;
        """
        return PromptTemplate(template=template, input_variables=["post"])



























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
    return """"""

def get_generation_prompt_initial():
    template = """
    You are mimicking a customer who is interested in a product and they are mentioning the following topics: {features}. 
    Write a convincing sentence or two as a customer who inquires about product recommendations. Try to be creative and make 
    sure to specify specific values for the topics they mention. Do not leave the topics as place holders. At the end of your 
    sentence, state what you wrote for {positives}. Make sure to exactly write the words in {positives} in your sentence. For 
    example instead of "display size" put "dimensions" if "dimensions" is in {positives}.

    For the sake of clarification, here is an example:
    "{example}"
    """

    return PromptTemplate(template=template, input_variables=["features", "positives"], partial_variables={"example": get_generation_example_initial()}) 

def get_generation_example_initial():
    return """
    Hello, I am looking for a 1x2x13 black laptop. I want it to be affordable (around $800). If you have something in mind call me at 888-888-8888. Thanks! 

    color: black
    dimensions: 1x2x13 """