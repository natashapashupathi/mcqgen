import openai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

# Initialize the OpenAI language model
def init_openai_model(api_key):
    openai.api_key = api_key
    return openai

# Define the prompt template for generating MCQs
def create_quiz_prompt():
    template = """
    Text: {text}
    You are an expert MCQ maker. Given the above text, it is your job to \
    create a quiz of {number} multiple choice questions for {subject} students in {tone} tone. 
    Make sure the questions are not repeated and check all the questions to be conforming to the text as well.
    Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
    Ensure to make {number} MCQs.
    ### RESPONSE_JSON
    {response_json}
    """

    quiz_generation_prompt = PromptTemplate(
        input_variables=["text", "number", "subject", "tone", "response_json"],
        template=template
    )
    
    return quiz_generation_prompt

# Define the prompt template for evaluating the MCQs
def create_review_prompt():
    template = """
    You are an expert English grammarian and writer. Given a Multiple Choice Quiz for {subject} students,\
    you need to evaluate the complexity of the questions and give a complete analysis of the quiz. \
    Only use a maximum of 50 words for complexity analysis. 
    If the quiz is not at par with the cognitive and analytical abilities of the students,\
    update the quiz questions that need to be changed and adjust the tone accordingly.
    Quiz_MCQs:
    {quiz}

    Provide your expert review of the above quiz:
    """

    quiz_evaluation_prompt = PromptTemplate(
        input_variables=["subject", "quiz"], 
        template=template
    )
    
    return quiz_evaluation_prompt

# Function to generate and evaluate MCQs
def generate_evaluate_chain(data):
    """
    This function takes input data (text, number of MCQs, subject, tone, and response_json) and 
    generates MCQs using OpenAI's API, followed by an evaluation of the MCQs.
    """

    # Create the prompt templates
    quiz_prompt = create_quiz_prompt()
    review_prompt = create_review_prompt()

    # Initialize the language model
    llm = openai

    # Create the chains
    quiz_chain = LLMChain(llm=llm, prompt=quiz_prompt, output_key="quiz", verbose=True)
    review_chain = LLMChain(llm=llm, prompt=review_prompt, output_key="review", verbose=True)

    # Sequential chain to run the two chains in sequence
    sequential_chain = SequentialChain(
        chains=[quiz_chain, review_chain], 
        input_variables=["text", "number", "subject", "tone", "response_json"],
        output_variables=["quiz", "review"],
        verbose=True
    )

    # Run the chain with the input data
    result = sequential_chain.run(data)

    return result
