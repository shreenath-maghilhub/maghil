pip install google-generativeai
import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
 
# Function to read data from uploaded CSV file
def read_csv_file(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return None
# Function to display prompt
def display_prompt(df):
    if df is not None:
        # Fetch column names
        columns = df.columns.tolist()
       
        # Fetch a limited number of rows for preview
        rows = df.values.tolist()
       
        # Construct the prompt including column names and sample rows
        prompt_with_columns = ", ".join(columns)
        prompt_with_sample_rows = ""
        for row in rows:
            prompt_with_sample_rows += "\t" + "\t".join(map(str, row)) + "\n"
       
        # Combine all components into the final prompt
        prompt = (
            "You're a chatbot specialized in food menus named Cheeku. Your role involves interactively responding to menu-related inquiries using an uploaded CSV file. Here's the schema of your data:"
            + prompt_with_columns
            + prompt_with_sample_rows
            + "\nYou should answer the given questions, and your answer should be comphrehensive, like it is to a foodie."
        )
        return prompt
    else:
        return ""
 
genai.configure(api_key='AIzaSyBXJ4zHkZLEdEmAIt3kLP2ifHbJWUMjl5I')
 
# Initialize Gemini model
model_name = "gemini-pro"
model = genai.GenerativeModel(model_name)
 
# Function to get Gemini's response
def get_gemini_response(question, chat, prompt):
    response = chat.send_message([question, prompt], stream=True)
    return response
 
# Initialize Streamlit app
st.header("Chatbot")
 
# Upload CSV file
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
 
# If file uploaded
if uploaded_file is not None:
    # Read data from CSV file
    df = read_csv_file(uploaded_file)
   
    # Display prompt
    prompt = display_prompt(df)
   
    # Initialize session state for chat history and gemini_chat
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
        st.session_state['gemini_chat'] = model.start_chat(history=[])
   
    # Get user input and submit button
    input_text = st.text_input("Input: ", key="input")
    submit_button = st.button("Ask the question")
   
    # If user submits input
    if submit_button and input_text:
        # Get Gemini's response
        response = get_gemini_response(input_text, st.session_state['gemini_chat'], prompt)
   
        # Add user query and response to session state chat history
        st.session_state['chat_history'].append(("You", input_text))
        for chunk in response:
            st.session_state['chat_history'].append(("Bot", chunk.text))
   
    # Display conversation history
    st.subheader("The Chat History is")
    st.write("Cheeku : Hello there! I'm Cheeku, your interactive menu assistant, here to make your dining experience even more engaging and enjoyable!")
    for role, text in st.session_state['chat_history']:
        st.write(f"{text}")
 
