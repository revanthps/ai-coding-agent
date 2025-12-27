import os
from dotenv import load_dotenv
# from openai import OpenAI
import argparse
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage, SystemMessage
from prompts import system_prompt
from call_function import tools, call_function
from langchain_core.messages import ToolMessage

def main():
    load_dotenv()

    api_key = os.environ.get("HF_TOKEN")

    # 1. Setup the underlying LLM (Remote Endpoint)
    llm = HuggingFaceEndpoint(
        repo_id="Qwen/Qwen3-Coder-30B-A3B-Instruct",
        task="text-generation",
        max_new_tokens=512,
        huggingfacehub_api_token=api_key,
    )    

    if api_key:
        print("API Key loaded successfully.")
    else:
        raise RuntimeError("API Key not found. Please set the HF_TOKEN environment variable.")

    # client = OpenAI(api_key=api_key)
    # 2. Wrap it in ChatHuggingFace to handle message formatting
    chat_model = ChatHuggingFace(llm=llm).bind_tools(tools)


    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if args.user_prompt is None:
        raise ValueError("User prompt is required.")
    
    if args.verbose:
        print(f"Prompt: {args.user_prompt}")
    
    # 3. Format messages (Equivalent to your types.Content list)
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=args.user_prompt)
    ]
    
    generate_content(chat_model, messages, args.verbose)
    
    # response = client.responses.create(
    #     model="gpt-4o-mini",
    #     input=message,
    # )


    
def generate_content(chat_model, messages, verbose):

    for i in range(0, 50):
    
        response = chat_model.invoke(messages)
        
        if response is None or response.response_metadata is None:
            print("No response data available.")
            return
        
        
        # Accessing the metadata
        metadata = response.response_metadata.get("token_usage", {})

        input_tokens = metadata.get("prompt_tokens", 0)
        output_tokens = metadata.get("completion_tokens", 0)
        total_tokens = metadata.get("total_tokens", 0)

        if verbose:        
            print(f"Prompt tokens: {input_tokens}")
            print(f"Response tokens: {output_tokens}")
            print(f"Total tokens: {total_tokens}")

        messages.append(response)

        function_responses = []
        if response.tool_calls:
            # print("The model wants to call a tool:")
            for tool_call in response.tool_calls:
                result = call_function(tool_call, verbose)
                if (
                    result is None
                    or result == "" 
                ):
                    raise RuntimeError(f"Empty function response for {tool_call["name"]}")
                else:
                    # print(f" -> {result}")
                    tool_msg = ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call["id"],
                        name=tool_call["name"]
                        )                
                    messages.append(tool_msg)
                
                tool_msg = ToolMessage(
                    content=str(result),
                tool_call_id=tool_call["id"],
                name=tool_call["name"]
                )               
                
                function_responses.append(tool_msg)
        else:
            print("Response:", response.content)
            return

if __name__ == "__main__":
    main()
    