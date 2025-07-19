import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from functions.functions_list import available_functions
from call_function import call_function
from config import MAX_ITER

def parse_args():
    args = sys.argv[1:]
    verbose = False
    if '--verbose' in args:
        verbose = True
        args.remove('--verbose')
    if not args:
        print('Error: No prompt provided. Please run the script like this:')
        print("Usage: uv run main.py <your prompt here> [--verbose]")
        sys.exit(1)
    user_prompt = " ".join(args)
    return user_prompt, verbose

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not found in the environment, please set it in the .env file.")
        sys.exit(1)

    user_prompt, verbose = parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    client = genai.Client(api_key=api_key)
    
    iter = 0
    while True:
        iter += 1
        if iter > MAX_ITER:
            print(f"Maximum iterations ({MAX_ITER}) reached.")
            sys.exit(1)

        try: 
            response = client.models.generate_content(
                model ='gemini-2.0-flash-001',
                contents = messages,
                config=types.GenerateContentConfig(
                    tools= [available_functions],
                    system_instruction=system_prompt
                )
            )

            if verbose and response.usage_metadata is not None:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)
        

            if response.function_calls:
                for function_call_part in response.function_calls:
                    call_result = call_function(function_call_part, verbose=verbose)
                    messages.append(types.Content(role="tool", parts= call_result.parts))

                    if  hasattr(call_result.parts[0], "function_response") and hasattr(call_result.parts[0].function_response, "response"):
                        if verbose:
                            print(f"-> {call_result.parts[0].function_response.response}")
                    else:
                        raise Exception("No function response found in the call result")

            if response.text and not response.function_calls :
                print("\nFinal response:")
                print(response.text)
                break 

        except Exception as e:
            print(f"Error in generate_content: {e}")
            sys.exit(1)
if __name__ == "__main__":
    main()
