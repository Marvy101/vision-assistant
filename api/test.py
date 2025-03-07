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

if __name__ == "__main__":
    # Test case 1: Basic image description
    image_path = "testimage1.jpg"
    print("\nTest Case 1: Basic Image Description")
    test_describe_image(image_path)
    
    # Test case 2: Image description with context
    print("\nTest Case 2: Image Description with Context")
    test_describe_image(
        image_path,
        past_context="This is a busy intersection with multiple lanes of traffic. There are cars moving in both directions and pedestrian crossings with traffic signals."
    ) 