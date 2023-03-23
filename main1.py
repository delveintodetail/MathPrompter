import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import os

import re



os.environ["openai_api_key"] = st.secrets["password"]


openai_api_key = os.environ["openai_api_key"]




template = """
    Your goal is to Write a mathematical equation and generate the answer format
starting with 'output ='. 

  Below is an example,
  input: Qt: at a restaurant, each adult meal costs A and kids eat free. if a group of B people
came in and C were kids, how much would it cost for the group to eat?
Mapping: A:5, B:15, C:8
  output = 5*(15-8)

  one more example,  
  Qt: At the fair Adam bought A tickets. After riding the ferris wheel he had B tickets left. If each ticket cost
C dollars, how much money did Adam spend riding the ferris wheel?
Mapping: A:10, B:2, C:8
  output = (10-2)*8

    input: {input}

    YOUR Response: 
"""




template1 = """
Your goal is to Write a Python function that return the value to the variable answer.

An example is,
input: at a restaurant, each adult meal costs A and kids eat free. if a group of B people
came in and C were kids, how much would it cost for the group to eat?
Mapping: A:5, B:15, C:8

output:
def get_result(A, B, C):
    out = A*(B-C)
    return out
answer = get_result(5, 15, 8)

One more example is, 
input: Qt: At the fair Adam bought A tickets. After riding the ferris wheel he had B tickets left. If each ticket cost
C dollars, how much money did Adam spend riding the ferris wheel?
Mapping: A:10, B:2, C:8
  
output:
def get_result(A, B, C):
    out = A*(B-C)
    return out
answer = get_result(10, 2, 8)


input: {input}

output: 
"""



prompt = PromptTemplate(
    input_variables=["input"],
    template=template,
)



prompt1 = PromptTemplate(
    input_variables=["input"],
    template=template1,
)



def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="MathPrompt", page_icon=":robot:")
st.header("MathPrompt")




def get_text():
    input_text = st.text_area(label="问题", label_visibility='collapsed', placeholder="Your Email...", key="your problem")
    return input_text

email_input = get_text()

if len(email_input.split(" ")) > 1000:
    st.write("Please enter a shorter email. The maximum length is 1000 words.")
    st.stop()


st.markdown("### 计算结果:")


# Define a function to convert a digit to a letter
def digit_to_letter(match):
    global mappings
    letter = chr(ord('A') + len(mappings))
    mappings[letter] = int(match.group())
    return letter



if email_input:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)


    input_str = email_input
    # Define the dictionary to hold the mappings
    mappings = {}
    # Define the regular expression pattern to match digits
    pattern = r'\d+'

    # Replace each digit in the input string with a letter and update the mappings dictionary
    output_str = re.sub(pattern, digit_to_letter, input_str)

    # Print the output string and the mappings dictionary
    new_input = output_str + "\n" + str(mappings)


    prompt_with_email = prompt.format(input=new_input)
    formatted_email = llm(prompt_with_email)
    print(exec(formatted_email))
    print("output: ", output)

    prompt_with_email1 = prompt1.format(input=new_input)
    formatted_email1 = llm(prompt_with_email1)
    exec(formatted_email1)

    print("answer: ", answer)
    if output == answer:
        final_output = "the result is " + str(answer)
        st.write(final_output)
    else:
        st.write("do not have answer")
