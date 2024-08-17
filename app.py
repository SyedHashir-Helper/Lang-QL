import streamlit as st
from groq import Groq

# Function to generate SQL schema using the provided API
def generate(api_key, sql_type, user_input):
    client = Groq(
        api_key=api_key,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"""
                          # Task 
                        Generate a SQL Schema based on the following input: `{user_input}`

                        ### {sql_type} Database Schema 
                        The schema will be look like the following: 

                        <SQL Table DDL Statements>
                        You are acting as a Database engineer. You are responsible for generating SQL Schema in {sql_type}.

                        Response Should mention the {sql_type}. Don't include in code block.
                        """,
            }
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content

# Get API key from secrets
api_key = "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"

# Page configuration with default Streamlit icon
st.set_page_config(page_title="Lang-QL", page_icon="🧠", layout="wide")

# Session state to store queries and selected query
if 'queries' not in st.session_state:
    st.session_state['queries'] = []
if 'generated_schema' not in st.session_state:
    st.session_state['generated_schema'] = ""

# Sidebar
with st.sidebar:
    st.title("Natural Language to SQL")
    
    sql_type = st.selectbox("Select SQL Type", ["T-SQL", "MySQL", "PostgreSQL"])

    # Text area pre-filled with the selected query
    user_input = st.text_area("Describe your database schema:")
    
    if st.button("Generate Schema", key="generate"):
        if user_input:
            if user_input not in st.session_state['queries']:
                st.session_state['queries'].append(user_input)
            # Call the generate function and store the result in session state
            st.session_state['generated_schema'] = generate(api_key, sql_type, user_input)


    # Display previous queries as clickable buttons
    st.markdown("### Previous Queries")
    if st.session_state['queries']:
        for i, query in enumerate(st.session_state['queries']):
            if st.button(f"Query {i+1}: {query[:30]}...", key=f"query_{i}"):
                st.session_state['generated_schema'] = generate(api_key, sql_type, query)

# Main content
st.markdown("## Lang-QL")

# Display the generated SQL schema
if st.session_state['generated_schema']:
    st.markdown("### Generated SQL Schema")
    st.code(st.session_state['generated_schema'], language='sql')

# Custom CSS for code block aesthetics
st.markdown("""
    <style>
        .stCodeBlock {
            color: #f8f8f2;
            padding: 20px;
            border-radius: 5px;
            font-size: 14px;
            overflow-x: auto;
        }
    </style>
""", unsafe_allow_html=True)
