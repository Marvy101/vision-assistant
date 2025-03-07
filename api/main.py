from werkzeug.datastructures import FileStorage
from typing import Dict, Any, Tuple, Union
import os
import tempfile
from openaiUtils import describe_image, text_to_speech

def process_file(file: FileStorage, past_context: str = None) -> Dict[str, Any]:
    """
    Process the uploaded image file and return the description using OpenAI.
    
    Args:
        file (FileStorage): The uploaded image file object from Flask
        past_context (str, optional): Previous context to consider when describing the image
    
    Returns:
        Dict[str, Any]: Dictionary containing the image description and optional text
    """
    # Create a temporary file to store the image
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
        file.save(temp_file.name)
        try:
            # Process the image using OpenAI utils
            result = describe_image(temp_file.name, past_context)
            return result
        finally:
            # Clean up the temporary file
            os.unlink(temp_file.name)

def process_text_to_speech(text: str, voice: str = "alloy") -> Tuple[Union[bytes, Dict[str, str]], int]:
    """
    Process text to speech conversion request.
    
    Args:
        text (str): The text to convert to speech
        voice (str, optional): The voice to use. Defaults to "alloy"
    
    Returns:
        Tuple[Union[bytes, Dict[str, str]], int]: Audio data and status code, or error message and status code
    """
    # Validate voice option
    valid_voices = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer', 'coral', 'sage']
    if voice not in valid_voices:
        return {'error': f'Invalid voice. Must be one of: {", ".join(valid_voices)}'}, 400

    try:
        # Get audio data from OpenAI
        audio_data = text_to_speech(text, voice)
        return audio_data, 200
    except Exception as e:
        return {'error': str(e)}, 500

