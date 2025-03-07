from werkzeug.datastructures import FileStorage
from typing import Dict, Any, Tuple, Union
import os
import tempfile
from openaiUtils import describe_image, text_to_speech

# List of supported languages with their codes
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'nl': 'Dutch',
    'pl': 'Polish',
    'ru': 'Russian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh': 'Chinese',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'tr': 'Turkish'
}

def process_file(file: FileStorage, past_context: str = None, language: str = "en") -> Dict[str, Any]:
    """
    Process the uploaded image file and return the description using OpenAI.
    
    Args:
        file (FileStorage): The uploaded image file object from Flask
        past_context (str, optional): Previous context to consider when describing the image
        language (str, optional): Language code for the response. Defaults to 'en'
    
    Returns:
        Dict[str, Any]: Dictionary containing the image description and optional text
    """
    # Validate language
    if language not in SUPPORTED_LANGUAGES:
        return {'error': f'Unsupported language code. Supported languages are: {", ".join(f"{k} ({v})" for k, v in SUPPORTED_LANGUAGES.items())}'}, 400

    # Create a temporary file to store the image
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
        file.save(temp_file.name)
        try:
            # Process the image using OpenAI utils with specified language
            result = describe_image(temp_file.name, past_context, language)
            return result
        finally:
            # Clean up the temporary file
            os.unlink(temp_file.name)

def process_text_to_speech(text: str, voice: str = "alloy", language: str = "en") -> Tuple[Union[bytes, Dict[str, str]], int]:
    """
    Process text to speech conversion request.
    
    Args:
        text (str): The text to convert to speech
        voice (str, optional): The voice to use. Defaults to "alloy"
        language (str, optional): Language code for the speech. Defaults to 'en'
    
    Returns:
        Tuple[Union[bytes, Dict[str, str]], int]: Audio data and status code, or error message and status code
    """
    # Validate language
    if language not in SUPPORTED_LANGUAGES:
        return {'error': f'Unsupported language code. Supported languages are: {", ".join(f"{k} ({v})" for k, v in SUPPORTED_LANGUAGES.items())}'}, 400

    # Validate voice option
    valid_voices = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer', 'coral', 'sage']
    if voice not in valid_voices:
        return {'error': f'Invalid voice. Must be one of: {", ".join(valid_voices)}'}, 400

    try:
        # Get audio data from OpenAI with specified language
        audio_data = text_to_speech(text, voice, language)
        return audio_data, 200
    except Exception as e:
        return {'error': str(e)}, 500

