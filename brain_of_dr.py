#step1:set up GROQ API key
import os
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

#step2: convert image to required format
import base64 #convert bits to byte

# image_file=open(image_path,"rb")
def encode_image(image_path):
    image_file = open(image_path, "rb")
    return base64.b64encode(image_file.read()).decode("utf-8")


#step3: set up multimodel LLM
from groq import Groq

query = "is their something with my face"
model = "qwen/qwen3.6-27b"


def analyze_image_with_query(query, model, encoded_image):
    client = Groq()

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
        }
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model
    )

    return chat_completion.choices[0].message.content