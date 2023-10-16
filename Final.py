import streamlit as st

import openai

import os

from github import Github
from PIL import Image

from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("Open_Ai_key")

openai.api_key = api_key
# Function to interact with the OpenAI API and maintain conversation history
if 'messages' not in st.session_state:
    st.session_state.messages = []
def interact_with_openai(messages):
    print(messages)
    print(st.session_state.messages)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
    )
    return response['choices'][0]['message']['content']

def get_all_files_recursive(repo, path=""):
    all_files = []

    contents = repo.get_contents(path)

    for content in contents:

        if content.type == "file":

            all_files.append(content)

        else:

            # If it's a directory, recursively retrieve files inside it

            all_files.extend(get_all_files_recursive(repo, content.path))

    return all_files


# Replace with your GitHub username, repository, and directory path

username = "Ninaad-Patil"

repository_name = "trial"

directory_path = "components"

# Replace with your GitHub token

github_token = "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"

# Authenticate with GitHub

g = Github(github_token)

repo = g.get_repo(f"{username}/{repository_name}")

all_files = get_all_files_recursive(repo, directory_path)

file_names = [file.path for file in all_files]


mapping_dict = {
    "RedHat Enterprise Linux 8.0": "RHEL8.0.txt",
    "RedHat Enterprise Linux 8.1": "RHEL8.1.txt"
    } 

# end git code files calling
st.set_page_config(layout="wide")

col1, col2= st.columns([1, 2])

with col1:
    
    
    logo = Image.open('logo.png').resize((200, 200))
    st.image(logo)

with col2:
    st.title("")
    st.title("OS Update Manager")


col1, col2 ,col3 = st.columns(3)

with col1:
    
    
# Dropdown menu to select a file
    
    
    options_choice = ["RedHat Linux", "Windows 11", "Other"]
    second_dropdown_options = ["RedHat Enterprise Linux 8.0", "RedHat Enterprise Linux 8.1"]
    selected_model = col1.selectbox("Select Menu", options_choice, index=None)
    selected_option_2 = None   
    selected_option_2 = col1.selectbox("Select Version", second_dropdown_options, index=None)
    selected_file = st.selectbox("Select a file", file_names)
    st.write("**Addational Prompt:** ")
    user_input = st.text_area("Enter your text here")  

#if selected_model:        
    #respbt=st.button("Get Response")
    
with col2:
    if selected_option_2:
        if user_input:
            if selected_model:
                with open(mapping_dict[selected_option_2], "r") as file:
                    file_contents = file.read()
                if file_contents:
                    st.session_state.messages.append({"role": "user",
                                 "content": f"{user_input}:\n{file_contents} "})
            else:
                    st.session_state.messages.append({"role": "user","content": f"{user_input} "})
        else:

            with open(mapping_dict[selected_option_2], "r") as file:

                file_contents = file.read()
                # Create a list of message objects to structure the conversation
                st.session_state.messages.append({"role": "system", "content": "You are a helpful assistant."})
                st.session_state.messages.append({"role": "user", "content": f"Summarize this for me and give me bullet points for it:\n{file_contents} "})

        assistant_reply = interact_with_openai(st.session_state.messages)

        st.session_state.messages.append({"role": "system", "content": assistant_reply})

        # Define CSS styles for the output box

        output_box_style = """padding: 10px;background-color: #f0f0f0;border-radius: 5px;box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);margin: 10px 0;"""

        st.write("Response:")

        # Split assistant_reply into bullet points

        bullet_points = assistant_reply.split('\n')

        formatted_output = '<ul>'

        for point in bullet_points:

            if point.strip():
                formatted_output += f'<li>{point}</li>'

        formatted_output += '</ul>'

        # Apply styles to the output box

        st.markdown(

            f'<div style="{output_box_style}">{formatted_output}</div>',

            unsafe_allow_html=True

        )
        
with col3:
    
    file_content = repo.get_contents(selected_file).decoded_content.decode("utf-8")

    st.text_area("File Content", file_content, height=400)

    if st.button("Get Response2"):  # Create a "Get Response2" button

        st.session_state.messages.append({"role": "user",
             "content": f"Based on the bullet points provided for RedHat Enterprise Linux do an impact analysis on the following code \n{file_content}"})

        assistant_reply2 = interact_with_openai(st.session_state.messages)

        st.session_state.messages.append({"role": "system", "content": assistant_reply2})
        st.write("Analysis:")

        # Split the response into code and text

        code_start = assistant_reply2.find("```")

        code_end = assistant_reply2.rfind("```")

        if code_start != -1 and code_end != -1:

            # Extract the code block

            code_block = assistant_reply2[code_start:code_end + 3]

            # Display code in a different color

            st.markdown(f'<pre style="color: blue;">{code_block}</pre>', unsafe_allow_html=True)

            # Display the remaining text in the normal format

            st.markdown(f'<p>{assistant_reply2[:code_start]}</p>', unsafe_allow_html=True)

        else:

            # If no code block is found, display the entire response in the normal format

            st.markdown(f'<p>{assistant_reply2}</p>', unsafe_allow_html=True)            

    
        