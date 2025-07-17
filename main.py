import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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
        print("GEMINI_API_KEY not found in the environment.")
        sys.exit(1)

    user_prompt, verbose = parse_args()

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model ='gemini-2.0-flash-001',
        contents = messages,
    )
    
    if verbose:
        print(f"User prompt: {user_prompt}\n")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    print(response.text)

if __name__ == "__main__":
    main()
