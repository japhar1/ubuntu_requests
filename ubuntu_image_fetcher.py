import os
import requests
import hashlib
from urllib.parse import urlparse, unquote
from pathlib import Path
import re

def fetch_images_with_ubuntu_spirit():
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
    
    # Get multiple URLs from user with community-minded messaging
    print("Please share URLs of images you'd like to preserve (separate with commas or new lines).")
    print("Type 'done' on a new line when finished:")
    
    urls = []
    while True:
        user_input = input().strip()
        if user_input.lower() == 'done':
            break
        if user_input:
            # Split by commas or whitespace
            new_urls = re.split(r'[,\s]+', user_input)
            urls.extend([url.strip() for url in new_urls if url.strip()])
    
    if not urls:
        print("No URLs provided. Remember, we thrive through sharing.")
        return
    
    # Remove duplicates while preserving order
    seen = set()
    urls = [url for url in urls if not (url in seen or seen.add(url))]
    
    print(f"\nPreparing to fetch {len(urls)} unique image URLs...")
    
    # Create directory for community sharing
    directory = "Fetched_Images"
    try:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Community repository '{directory}' is ready")
    except OSError as e:
        print(f"✗ We encountered a problem creating our shared space: {e}")
        return
    
    # Initialize set for tracking image hashes to prevent duplicates
    downloaded_hashes = set()
    
    # Counter for successful downloads
    successful_downloads = 0
    
    # Process each URL with Ubuntu principles
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Processing: {url}")
        
        # Validate URL format before attempting download
        if not is_valid_url(url):
            print("  ✗ This doesn't appear to be a valid URL. Let's respect proper web addresses.")
            continue
            
        # Check if URL points to a potentially dangerous file type
        if is_potentially_dangerous_url(url):
            print("  ✗ This URL appears to point to a potentially dangerous file type. We'll skip it for safety.")
            continue
            
        # Respectfully attempt to fetch the resource
        try:
            print("  Connecting to the global community...")
            headers = {
                'User-Agent': 'UbuntuImageFetcher/1.0 (Community Image Preservation Tool)'
            }
            response = requests.get(url, timeout=15, headers=headers, stream=True)
            response.raise_for_status()  # Check for HTTP errors
            
            # Check HTTP headers for safety and content information
            header_check_result = check_http_headers(response.headers, url)
            if not header_check_result["safe_to_download"]:
                print(f"  ✗ Header check suggests we shouldn't download this: {header_check_result['message']}")
                continue
                
            # Verify we're receiving an image
            content_type = response.headers.get('content-type', '')
            if 'image' not in content_type:
                print("  ✗ The shared resource doesn't appear to be an image. Let's respect content types.")
                continue
                
            # Read content in chunks for large files and hashing
            content = b''
            for chunk in response.iter_content(chunk_size=8192):
                content += chunk
                
            # Check file size to prevent excessively large downloads
            if len(content) > 20 * 1024 * 1024:  # 20MB limit
                print("  ✗ This image is too large for our community repository (max 20MB).")
                continue
                
            # Generate hash to check for duplicates
            content_hash = hashlib.md5(content).hexdigest()
            if content_hash in downloaded_hashes:
                print("  ⓘ This image appears to be a duplicate of one already in our collection.")
                continue
                
            # Extract filename with respect to the original resource
            filename = extract_filename(url, response.headers, content_hash)
            filepath = os.path.join(directory, filename)
            
            # Ensure filename is safe
            filename = make_safe_filename(filename)
            
            # Save the image for community sharing
            try:
                with open(filepath, 'wb') as f:
                    f.write(content)
                
                downloaded_hashes.add(content_hash)
                successful_downloads += 1
                print(f"  ✓ Successfully preserved '{filename}' in our community repository")
                
            except IOError as e:
                print(f"  ✗ We couldn't preserve this resource: {e}")
                print("  Let's ensure we have proper permissions to build our community space.")
            
        except requests.exceptions.RequestException as e:
            print(f"  ✗ We couldn't connect respectfully: {e}")
            print("  Remember, not all connections succeed, but we persist as a community.")
    
    # Final summary in the spirit of Ubuntu
    print("\n" + "=" * 60)
    print("Download Summary")
    print("=" * 60)
    print(f"Total URLs processed: {len(urls)}")
    print(f"Successfully preserved images: {successful_downloads}")
    print(f"Community repository: {os.path.abspath(directory)}")
    print()
    if successful_downloads > 0:
        print("Thank you for contributing to our shared resources!")
    print("In the spirit of Ubuntu: 'I am because we are'")

def is_valid_url(url):
    """Check if the URL has a valid format."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def is_potentially_dangerous_url(url):
    """Check if URL points to potentially dangerous file types."""
    dangerous_extensions = {
        '.exe', '.bat', '.cmd', '.sh', '.php', '.js', '.html', '.htm',
        '.vbs', '.scr', '.pif', '.com', '.jar', '.bin', '.cpl', '.hta'
    }
    
    path = urlparse(url).path.lower()
    return any(path.endswith(ext) for ext in dangerous_extensions)

def check_http_headers(headers, url):
    """
    Check HTTP headers for safety and content information.
    Returns a dictionary with safety assessment and message.
    """
    result = {
        "safe_to_download": True,
        "message": "Headers appear appropriate"
    }
    
    content_type = headers.get('content-type', '').lower()
    content_length = headers.get('content-length')
    
    # Check for HTML content disguised as image
    if 'text/html' in content_type and 'image' not in content_type:
        result["safe_to_download"] = False
        result["message"] = "Content-Type indicates HTML, not image"
        return result
    
    # Check for extremely large files
    if content_length and int(content_length) > 20 * 1024 * 1024:  # 20MB limit
        result["safe_to_download"] = False
        result["message"] = f"Content-Length indicates file is too large ({int(content_length) / (1024*1024):.1f}MB)"
        return result
    
    # Check for unexpected content types
    expected_image_types = {
        'image/jpeg', 'image/png', 'image/gif', 'image/webp', 
        'image/bmp', 'image/tiff', 'image/svg+xml'
    }
    
    if content_type and not any(img_type in content_type for img_type in expected_image_types):
        result["safe_to_download"] = False
        result["message"] = f"Content-Type '{content_type}' doesn't match expected image types"
        return result
    
    # Check for security headers that might indicate issues
    x_content_type_options = headers.get('x-content-type-options', '').lower()
    if x_content_type_options == 'nosniff' and not content_type:
        result["safe_to_download"] = False
        result["message"] = "X-Content-Type-Options: nosniff header without Content-Type"
        return result
    
    return result

def extract_filename(url, headers, content_hash):
    """
    Extract a filename from the URL or headers with respect to the source.
    Implements Ubuntu's principle of respecting origins while adapting to community needs.
    """
    # First try to get filename from Content-Disposition header
    content_disp = headers.get('content-disposition', '')
    if 'filename=' in content_disp:
        filename = content_disp.split('filename=')[1]
        # Remove quotes and any additional parameters
        filename = filename.split(';')[0].strip('"\'')
        return unquote(filename)
    
    # Otherwise, extract from URL path
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = os.path.basename(path)
    
    if not filename or '.' not in filename:
        # Generate a respectful filename if none is available
        extension = get_extension_from_content_type(headers.get('content-type', ''))
        filename = f"ubuntu_image_{content_hash[:8]}{extension}"
    else:
        filename = unquote(filename)
    
    return filename

def get_extension_from_content_type(content_type):
    """
    Map content type to appropriate file extension
    """
    content_type = content_type.lower()
    mapping = {
        'image/jpeg': '.jpg',
        'image/jpg': '.jpg',
        'image/png': '.png',
        'image/gif': '.gif',
        'image/webp': '.webp',
        'image/bmp': '.bmp',
        'image/tiff': '.tiff',
        'image/svg+xml': '.svg'
    }
    
    for pattern, extension in mapping.items():
        if pattern in content_type:
            return extension
    
    return '.bin'  # Default binary extension

def make_safe_filename(filename):
    """
    Ensure the filename is safe to use by removing or replacing problematic characters.
    """
    # Remove directory path attempts
    filename = os.path.basename(filename)
    
    # Replace problematic characters with underscores
    filename = re.sub(r'[\\/*?:"<>|]', "_", filename)
    
    # Limit length
    if len(filename) > 100:
        name, ext = os.path.splitext(filename)
        filename = name[:100-len(ext)] + ext
    
    return filename

if __name__ == "__main__":
    fetch_images_with_ubuntu_spirit()