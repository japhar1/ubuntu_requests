import os
import requests
from urllib.parse import urlparse, unquote
from pathlib import Path

def fetch_image_with_ubuntu_spirit():
    """
    A function that embodies the Ubuntu philosophy: 
    "I am because we are" - connecting to the global community,
    respectfully fetching shared resources, and organizing them
    for later appreciation.
    """
    print("=" * 60)
    print("Ubuntu-Inspired Image Fetcher")
    print("=" * 60)
    print("In the spirit of Ubuntu: connecting communities through shared resources")
    print()
    
    # Get URL from user with community-minded messaging
    url = input("Please share the URL of an image you'd like to preserve: ").strip()
    
    if not url:
        print("No URL provided. Remember, we thrive through sharing.")
        return
    
    # Create directory for community sharing
    directory = "Fetched_Images"
    try:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Community repository '{directory}' is ready")
    except OSError as e:
        print(f"✗ We encountered a problem creating our shared space: {e}")
        return
    
    # Respectfully attempt to fetch the resource
    try:
        print("Connecting to the global community...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check for HTTP errors
        
        # Verify we're receiving an image
        content_type = response.headers.get('content-type', '')
        if 'image' not in content_type:
            print("The shared resource doesn't appear to be an image. Let's respect content types.")
            return
            
    except requests.exceptions.RequestException as e:
        print(f"✗ We couldn't connect respectfully: {e}")
        print("Remember, not all connections succeed, but we persist as a community.")
        return
    
    # Extract filename with respect to the original resource
    filename = extract_filename(url, response.headers)
    filepath = os.path.join(directory, filename)
    
    # Save the image for community sharing
    try:
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"✓ Successfully preserved '{filename}' in our community repository")
        print(f"Full path: {os.path.abspath(filepath)}")
        print()
        print("Thank you for contributing to our shared resources!")
        print("In the spirit of Ubuntu: 'I am because we are'")
    except IOError as e:
        print(f"✗ We couldn't preserve this resource: {e}")
        print("Let's ensure we have proper permissions to build our community space.")

def extract_filename(url, headers):
    """
    Extract a filename from the URL or headers with respect to the source.
    Implements Ubuntu's principle of respecting origins while adapting to community needs.
    """
    # First try to get filename from Content-Disposition header
    content_disp = headers.get('content-disposition', '')
    if 'filename=' in content_disp:
        filename = content_disp.split('filename=')[1].strip('"\'')
        return unquote(filename)
    
    # Otherwise, extract from URL path
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = os.path.basename(path)
    
    if not filename or '.' not in filename:
        # Generate a respectful filename if none is available
        import time
        extension = get_extension_from_content_type(headers.get('content-type', ''))
        filename = f"community_image_{int(time.time())}{extension}"
    else:
        filename = unquote(filename)
    
    return filename

def get_extension_from_content_type(content_type):
    """
    Map content type to appropriate file extension
    """
    content_type = content_type.lower()
    if 'jpeg' in content_type or 'jpg' in content_type:
        return '.jpg'
    elif 'png' in content_type:
        return '.png'
    elif 'gif' in content_type:
        return '.gif'
    elif 'webp' in content_type:
        return '.webp'
    elif 'bmp' in content_type:
        return '.bmp'
    elif 'tiff' in content_type:
        return '.tiff'
    else:
        return '.bin'  # Default binary extension

if __name__ == "__main__":
    fetch_image_with_ubuntu_spirit()