import django
from django.core.files.base import ContentFile
from hospitals.models import UserReview, Institution
import openai
import os
import requests
import json
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Pharmiliar.settings") 
django.setup()


# load_dotenv()
# openai.api_key = os.environ.get("OPENAI_API_KEY")
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:
# client = OpenAI(
#   api_key=os.environ.get("CUSTOM_ENV_NAME"),
# )

client = openai.OpenAI()
model = "gpt-3.5-turbo-16k"

def get_reviews_summary():
    reviews = UserReview.objects.all()
    if reviews.exists():
        summary = ""
        for review in reviews:
            summary += review.review + "\n"
        return summary
    else:
        return "There are no reviews yet."

# Main class definition
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


def main():
    # Create an instance of the AssistantManager class
    assistant_manager = AssistantManager()

    # Define instructions and tools for the assistant
    instructions = "You are a personal review summarizer assistant who knows how to summarize reviews for institutions"
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_reviews",
                "description": "Summarize reviews from the function",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "reviews": {"type": "string"}
                    }
                },
                "required": ["reviews"],
            },
        },
    ]

    # Create the assistant
    assistant_manager.create_assistant(
        name="Ixnay",
        instructions=instructions,
        tools=tools
    )

    # Create a thread
    assistant_manager.create_thread()

    # Add a message to the thread and run the assistant
    assistant_manager.add_message_to_thread(
        role="user",
        content="Summarize reviews"
    )
    assistant_manager.run_assistant("Summarize reviews")

    # Wait for completion and process the messages
    assistant_manager.wait_for_completion()

    # Get the summary
    summary = assistant_manager.get_summary()
    print(summary)

    # Run steps
    assistant_manager.run_steps()


if __name__ == "__main__":
    main()
