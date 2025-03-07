import requests
import json

def test_describe_image(image_path, past_context=None):
    """
    Test the describe-image endpoint with a local image file.
    
    Args:
        image_path (str): Path to the image file
        past_context (str, optional): Previous context to consider when describing the image
    """
    # API endpoint URL (assuming Flask is running locally on default port)
    url = 'https://vision-assistant-sepia.vercel.app/vision'
    
    
    # Prepare the files and data for the request
    files = {
        'image': open(image_path, 'rb')
    }
    
    # Add past_context to form data if provided
    data = {}
    if past_context:
        data['past_context'] = past_context

    headers = { 
        'key': 'wearewinningthiscompetition'
    }
    
    try:
        # Make the POST request
        response = requests.post(url, files=files, data=data, headers=headers)
        
        # Check if request was successful
        response.raise_for_status()
        
        # Print the formatted response
        print("\nAPI Response:")
        print(json.dumps(response.json(), indent=4))
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
    finally:
        # Make sure to close the file
        files['image'].close()

def test_text_to_speech(text: str, voice: str = None):
    """
    Test the text-to-speech endpoint.
    
    Args:
        text (str): The text to convert to speech
        voice (str, optional): The voice to use. If not provided, uses default voice.
    """
    # API endpoint URL (local Flask server)
    # url = 'http://127.0.0.1:5000/text-to-speech'
    url = 'https://vision-assistant-sepia.vercel.app/text-to-speech'
    
    # Prepare the request data
    data = {'text': text}
    if voice:
        data['voice'] = voice
    
    headers = {
        'Content-Type': 'application/json',
        'key': 'wearewinningthiscompetition'
    }
    
    try:
        # Make the POST request
        response = requests.post(url, json=data, headers=headers)
        
        # Check if request was successful
        response.raise_for_status()
        
        # Save the audio file
        filename = f'test_speech_{voice or "default"}.mp3'
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"\nAudio saved to {filename}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        if hasattr(e.response, 'json'):
            print("Error details:", e.response.json())

if __name__ == "__main__":
    # Test case 1: Basic image description
    # image_path = "testimage1.jpg"
    # print("\nTest Case 1: Basic Image Description")
    # test_describe_image(image_path)
    
    # # Test case 2: Image description with context
    # print("\nTest Case 2: Image Description with Context")
    # test_describe_image(
    #     image_path,
    #     past_context="This is a busy intersection with multiple lanes of traffic. There are cars moving in both directions and pedestrian crossings with traffic signals."
    # )
    
    # Test case 3: Text-to-speech with default voice
    # print("\nTest Case 3: Text-to-speech with default voice")
    # test_text_to_speech(
    #     "Hello! This is a test of the text-to-speech functionality with the default voice."
    # )
    
    # # Test case 4: Text-to-speech with custom voice
    print("\nTest Case 4: Text-to-speech with custom voice (nova)")
    test_text_to_speech(
        "أحب دادا! هذا اختبار لوظيفة تحويل النص إلى كلام باستخدام الصوت نوفا. دعني أسترسل قليلاً. الطقس اليوم لطيف جداً، مع نسيم خفيف وسماء صافية. إنه اليوم المثالي للتنزه في الحديقة أو القيام بنزهة مع الأصدقاء. هل لاحظت من قبل كيف تهمس الأوراق في الرياح، مما يخلق صوتاً مهدئاً يمكن أن يكون مريحاً جداً؟ الطبيعة لديها طريقة لتهدئة العقل وجلب السلام إلى حياتنا المزدحمة. بالحديث عن الطبيعة، هل تعلم أن هناك أكثر من 391,000 نوع من النباتات في العالم؟ كل منها يلعب دوراً حيوياً في الحفاظ على توازن نظامنا البيئي. من المثير التفكير في التنوع والتعقيد في الحياة على كوكبنا. على أي حال، أسترسل. لنعد إلى اختبار وظيفة تحويل النص إلى كلام باستخدام الصوت نوفا.",
        voice="nova"
    ) 