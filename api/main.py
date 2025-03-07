from werkzeug.datastructures import FileStorage
from typing import Dict, Any
import os
import tempfile
from openaiUtils import describe_image

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

