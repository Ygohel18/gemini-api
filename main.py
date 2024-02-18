import pathlib
import textwrap
import google.generativeai as genai
import time
import json
import time
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Google API
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Define FastAPI app
app = FastAPI()

# Define request body model
class PromptRequest(BaseModel):
    prompt: str

# Prompt generation function
def generate_response(prompt: str) -> str:
    # Generate content
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            candidate_count=1,
            max_output_tokens=6000,
            temperature=1.0
        )
    )

    content = response.text

    # Constructing the desired JSON structure
    json_response = {
        "choices": [
            {
                "finish_reason": "",
                "index": 0,
                "message": {
                    "content": f"${content}",
                    "role": "model"
                },
                "logprobs": None
            }
        ],
        "created": int(time.time()),
        "id": str(uuid4()),
        "model": "gpt-3.5-turbo-0613",
        "object": "chat.completion",
        "usage": {
            "completion_tokens": len(content.split()),
            "prompt_tokens": 1,
            "total_tokens": len(content.split()) + 1
        }
    }

    # Convert dictionary to JSON
    return json.dumps(json_response, indent=4)


# Define FastAPI endpoint
@app.post("/generate-response")
def generate_response_endpoint(prompt_request: PromptRequest):
    response_json_str = generate_response(prompt_request.prompt)
    return json.loads(response_json_str)
