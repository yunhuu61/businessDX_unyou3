import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

def test_api():
    # Load .env
    env_path = Path(__file__).parent / ".env"
    print(f"Loading .env from: {env_path}")
    
    if not env_path.exists():
        print(f"ERROR: .env file not found at {env_path}")
        return

    load_dotenv(env_path)
    
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("ERROR: GOOGLE_API_KEY not found in .env")
        # Print all keys to see what's there (safely)
        print("Available env vars keys:", list(os.environ.keys()))
        return
        
    print(f"API Key found: {api_key[:4]}...{api_key[-4:]} (Length: {len(api_key)})")
    
    # Check for whitespace issues
    if api_key.strip() != api_key:
        print("WARNING: API Key has leading/trailing whitespace!")

    try:
        print("Initializing Client...")
        client = genai.Client(api_key=api_key)
        
        print("Testing API connection with model 'gemini-2.0-flash'...")
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Hello, explain what an API is in 10 words.",
        )
        print("\nAPI Call Successful!")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print("\nAPI Call FAILED!")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {e}")
        
        err_str = str(e)
        if "429" in err_str:
            print("-> DIAGNOSIS: Rate Limit Exceeded (Quota).")
        elif "400" in err_str:
            print("-> DIAGNOSIS: Bad Request (Invalid Key or Model).")
        elif "401" in err_str or "403" in err_str:
            print("-> DIAGNOSIS: Authentication/Permission Failed.")

if __name__ == "__main__":
    test_api()
