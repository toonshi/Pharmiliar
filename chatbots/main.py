class AssistantManager:
    assistant_id = None
    thread_id = None

    def __init__(self, model=model):
        self.client = client
        self.model = model
        self.assistant = None
        self.thread = None
        self.run = None
        self.summary = None

        # Retrieve existing assistants if IDs are already present and avoid duplication
        if AssistantManager.assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(
                assistant_id=AssistantManager.assistant_id
            )
        if AssistantManager.thread_id:
            self.thread = self.client.beta.threads.retrieve(
                thread_id=AssistantManager.thread_id
            )

    def create_assistant(self, name, instructions, tools):
        if not self.assistant:
            try:
                assistant_obj = self.client.beta.assistants.create(
                    name=name,
                    instructions=instructions,
                    tools=tools,
                    model=self.model
                )
                AssistantManager.assistant_id = assistant_obj.id
                self.assistant = assistant_obj
                print(f"Assistant ID: {self.assistant_id}")
            except Exception as e:
                print(f"Error creating assistant: {e}")
        else:
            print(f"Assistant already created. Assistant ID: {self.assistant_id}")

    def create_thread(self):
        if not self.thread:
            thread_obj = self.client.beta.threads.create()
            AssistantManager.thread_id = thread_obj.id
            self.thread = thread_obj
            print(f"thread:::{self.thread.id}")

    def add_message_to_thread(self, role, content):
        if self.thread:
            self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role=role,
                content=content
            )

    def run_assistant(self, instructions):
        if self.thread and self.assistant:
            try:
                self.run = self.client.beta.threads.runs.create(
                    thread_id=self.thread_id,
                    assistant_id=self.assistant_id,
                    instructions=instructions
                )
                print(f"Run ID: {self.run.id}")
            except Exception as e:
                print(f"Error running assistant: {e}")

    def run_steps(self):
        if self.thread and self.run:
            if self.run.id:
                run_steps = self.client.beta.threads.runs.steps.list(
                    thread_id=self.thread.id,
                    run_id=self.run.id
                )
                print(f"RUN-STEPS :::{run_steps}")
            else:
                print("The 'run' object does not have an 'id' attribute.")
        else:
            print("Assistant or run not initialized. Unable to fetch run steps.")

    def process_message(self):
        if self.thread:
            messages = self.client.beta.threads.messages.list(thread_id=self.thread),
            summary = []

            last_message = messages.data[0]
            role = last_message.role
            response = last_message.content[0].text.value
            summary.append(response)
            self.summary = "\n".join(summary)
            print(f"SUMMARY--->{role.capitalize()}:.....response: {response}")

    def call_required_functions(self, required_actions):
        if not self.run:
            return
        tool_outputs = []
        for action in required_actions["tool_calls"]:
            func_name = action["function"]["name"]
            arguments = json.loads(action["function"]["arguments"])

            if func_name == "get_reviews":
                output = get_reviews_summary()
                tool_outputs.append({"tool_call_id": action["id"], "output": output})
                print("Submitting outputs back to the assistant....")
                self.client.beta.threads.runs.submit_outputs(
                    thread_id=self.thread.id,
                    run_id=self.run.id,
                    tool_outputs=tool_outputs
                )
            else:
                raise ValueError(f"Unknown function: {func_name}")

    def get_summary(self):
        return self.summary

    def wait_for_completion(self):
        if self.thread and self.run:
            while True:
                time.sleep(5)
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread_id, run_id=self.run.id
                )
                print(f"RUN STATUS:::{run_status.model_dump_json(indent=4)}")

                if run_status.status == "completed":
                    self.process_message()
                    break
                elif run_status.status == "requires_action":
                    print("Function calling now")
                    self.call_required_functions(
                        required_actions=run_status.required_action.submit_tool_outputs.model_dump()
                    )

    # Run steps
    def run_steps(self):
        if self.thread and self.run and self.run.id:  # Check if self.run is not None
            run_steps = self.client.beta.threads.runs.steps.list(
                thread_id=self.thread.id,
                run_id=self.run.id
            )
            print(f"RUN-STEPS :::{run_steps}")
        else:
            print("Assistant, run, or run ID not initialized. Unable to fetch run steps.")


import os
from dotenv import load_dotenv
import openai
import requests
import json

import time
import logging
from datetime import datetime
import streamlit as st


load_dotenv()

client = openai.OpenAI()

model = "gpt-4-1106-preview"  # "gpt-3.5-turbo-16k"


# == Hardcoded ids to be used once the first code run is done and the assistant was created
thread_id = "thread_inGWHWAOfo3yxnwNZCophiXL"
assis_id = "asst_KPhtBJnaLiJaYqGDqnoHn9oP"

# Initialize all the session
if "file_id_list" not in st.session_state:
    st.session_state.file_id_list = []

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None


# Set up our front end page
st.set_page_config(page_title="Study Buddy - Chat and Learn", page_icon=":books:")


# ==== Function definitions etc =====
def upload_to_openai(filepath):
    with open(filepath, "rb") as file:
        response = client.files.create(file=file.read(), purpose="assistants")
    return response.id


# === Sidebar - where users can upload files
file_uploaded = st.sidebar.file_uploader(
    "Upload a file to be transformed into embeddings", key="file_upload"
)

# Upload file button - store the file ID
if st.sidebar.button("Upload File"):
    if file_uploaded:
        with open(f"{file_uploaded.name}", "wb") as f:
            f.write(file_uploaded.getbuffer())
        another_file_id = upload_to_openai(f"{file_uploaded.name}")
        st.session_state.file_id_list.append(another_file_id)
        st.sidebar.write(f"File ID:: {another_file_id}")

# Display those file ids
if st.session_state.file_id_list:
    st.sidebar.write("Uploaded File IDs:")
    for file_id in st.session_state.file_id_list:
        st.sidebar.write(file_id)
        # Associate each file id with the current assistant
        assistant_file = client.beta.assistants.files.create(
            assistant_id=assis_id, file_id=file_id
        )

# Button to initiate the chat session
if st.sidebar.button("Start Chatting..."):
    if st.session_state.file_id_list:
        st.session_state.start_chat = True

        # Create a new thread for this chat session
        chat_thread = client.beta.threads.create()
        st.session_state.thread_id = chat_thread.id
        st.write("Thread ID:", chat_thread.id)
    else:
        st.sidebar.warning(
            "No files found. Please upload at least one file to get started."
        )


# Define the function to process messages with citations
def process_message_with_citations(message):
    """Extract content and annotations from the message and format citations as footnotes."""
    message_content = message.content[0].text
    annotations = (
        message_content.annotations if hasattr(message_content, "annotations") else []
    )
    citations = []

    # Iterate over the annotations and add footnotes
    for index, annotation in enumerate(annotations):
        # Replace the text with a footnote
        message_content.value = message_content.value.replace(
            annotation.text, f" [{index + 1}]"
        )

       
# the main interface ...
st.title("Life Guard")
st.write("The guy for emergencies")


# Check sessions
if st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-4-1106-preview"
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Show existing messages if any...
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # chat input for the user
    if prompt := st.chat_input("What's new?"):
        # Add user message to the state and display on the screen
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # add the user's message to the existing thread
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id, role="user", content=prompt
        )

        # Create a run with additioal instructions
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assis_id,
            instructions="""Please answer the questions using the knowledge provided in the files.
            when adding additional information, make sure to distinguish it with bold or underlined text.""",
        )

        # Show a spinner while the assistant is thinking...
        with st.spinner("Wait... Generating response..."):
            while run.status != "completed":
                time.sleep(1)
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread_id, run_id=run.id
                )
            # Retrieve messages added by the assistant
            messages = client.beta.threads.messages.list(
                thread_id=st.session_state.thread_id
            )
            # Process and display assis messages
            assistant_messages_for_run = [
                message
                for message in messages
                if message.run_id == run.id and message.role == "assistant"
            ]

            for message in assistant_messages_for_run:
                full_response = process_message_with_citations(message=message)
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
                with st.chat_message("assistant"):
                    st.markdown(full_response, unsafe_allow_html=True)

    else:
        # Promopt users to start chat
        st.write(
            "Please upload at least a file to get started by clicking on the 'Start Chat' button"
        )

