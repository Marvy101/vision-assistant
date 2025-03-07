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
    url = 'http://127.0.0.1:5000/text-to-speech'
    
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
        "J'aime Dada! Ceci est un test de la fonctionnalité de synthèse vocale avec la voix nova. Laissez-moi divaguer un moment. Le temps aujourd'hui est assez agréable, avec une brise légère et un ciel dégagé. C'est le jour parfait pour une promenade dans le parc ou un pique-nique avec des amis. Avez-vous déjà remarqué comment les feuilles bruissent dans le vent, créant un son apaisant qui peut être très relaxant? La nature a une façon de calmer l'esprit et d'apporter la paix à nos vies occupées. En parlant de nature, saviez-vous qu'il y a plus de 391 000 espèces de plantes dans le monde? Chacune joue un rôle crucial dans le maintien de l'équilibre de notre écosystème. C'est fascinant de penser à la diversité et à la complexité de la vie sur notre planète. Quoi qu'il en soit, je m'égare. Revenons au test de la fonctionnalité de synthèse vocale avec la voix nova.",
        voice="nova"
    ) 