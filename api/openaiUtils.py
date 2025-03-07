import base64
import json
from openai import OpenAI

client = OpenAI()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def describe_image(image_path, past_context=None):
    # Encode the image
    encoded_image = encode_image(image_path)
    
    # Base system prompt
    system_prompt = """You are an AI assistant designed to help visually impaired individuals by providing descriptions of images live from their camera. Your primary role is to describe the picture, focusing on key visual details such as objects, people, colors, actions, expressions, and context. If the image conveys an emotion, theme, or notable artistic style, include that as well.  Since you're basically the impaired person's eyes, use present language. for example, 'You're looking at...'

If there is past context provided, relate your current description to that context. For example, if the past context was a question about crossing the road, focus your description on relevant safety details and navigation information. Make sure your description addresses any concerns or questions from the past context.

If the image contains a significant amount of text that is important to understanding the image (e.g., a document, a sign, a screenshot of a message, or a page with dense text), transcribe the text and present it in a structured manner. Otherwise, prioritize describing the overall content rather than reading the text verbatim. When there's text to transcribe, minimize the description to only necessary details.

here's the json structure you should follow:

{
  "description": "<detailed description of what the person is seeing, incorporating and addressing any past context if provided>",
  "read_out": "<optional: transcribed text if it enhances understanding>"
}

Only include "read_out" when the text is a crucial part of the image. If the text is minor or incidental, focus on describing its visual context instead."""

    # Prepare messages
    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": system_prompt
                }
            ]
        }
    ]

    # Add past context if provided and not too large (limiting to 2000 characters)
    if past_context:
        past_context = past_context[:2000]  # Truncate if too long
        messages.append({
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": f"Previous context: {past_context}"
                }
            ]
        })

    # Add the image
    messages.append({
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{encoded_image}"
                }
            }
        ]
    })

    # Make the API call
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        response_format={"type": "json_object"},
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Parse and return the JSON response
    return json.loads(response.choices[0].message.content)



path = "/Users/pelumidada/Documents/code/vision-assistant/testimage2.jpg"


# response = describe_image(path, "I am about to cross the road what should I look out for?")
# print(json.dumps(response, indent=4))