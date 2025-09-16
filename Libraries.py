import requests
import os
from urllib.parse import urlparse
import hashlib
from datetime import datetime

def is_valid_image_content_type(headers):
    """Check if the content type is an image."""
    content_type = headers.get('Content-Type', '').lower()
    return content_type.startswith('image/')

def get_unique_filename(filepath):
    """Generate a unique filename if the file already exists."""
    if not os.path.exists(filepath):
        return filepath
    base, ext = os.path.splitext(filepath)
    counter = 1
    while True:
        new_filepath = f"{base}_{counter}{ext}"
        if not os.path.exists(new_filepath):
            return new_filepath
        counter += 1

def calculate_file_hash(filepath):
    """Calculate SHA-256 hash of a file to check for duplicates."""
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()

def fetch_and_save_image(url, output_dir="Fetched_Images"):
    """Fetch an image from a URL and save it, handling errors and duplicates."""
    try:
        # Validate URL scheme
        parsed_url = urlparse(url)
        if parsed_url.scheme not in ('http', 'https'):
            print(f"✗ Invalid URL scheme for {url}: Must be http or https")
            return False

        # Fetch the image with safety precautions
        response = requests.get(url, timeout=10, headers={'User-Agent': 'UbuntuImageFetcher/1.0'})
        response.raise_for_status()  # Raise exception for bad status codes

        # Check Content-Type header to ensure it's an image
        if not is_valid_image_content_type(response.headers):
            print(f"✗ URL {url} does not point to an image (Content-Type: {response.headers.get('Content-Type')})")
            return False

        # Check Content-Length to avoid overly large files (e.g., >10MB)
        content_length = response.headers.get('Content-Length')
        if content_length and int(content_length) > 10 * 1024 * 1024:
            print(f"✗ File at {url} is too large (exceeds 10MB)")
            return False

        # Extract filename or generate one
        filename = os.path.basename(parsed_url.path)
        if not filename or not '.' in filename:
            content_type = response.headers.get('Content-Type', 'image/jpeg')
            ext = content_type.split('/')[-1] if '/' in content_type else 'jpg'
            filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)

        # Check for duplicates using content hash
        temp_filepath = os.path.join(output_dir, f"temp_{filename}")
        with open(temp_filepath, 'wb') as f:
            f.write(response.content)

        file_hash = calculate_file_hash(temp_filepath)
        for existing_file in os.listdir(output_dir):
            if existing_file.startswith('temp_'):
                continue
            existing_filepath = os.path.join(output_dir, existing_file)
            if os.path.isfile(existing_filepath) and calculate_file_hash(existing_filepath) == file_hash:
                print(f"✗ Image from {url} is a duplicate of {existing_file}")
                os.remove(temp_filepath)
                return False

        # Save the image with a unique filename
        filepath = get_unique_filename(filepath)
        os.rename(temp_filepath, filepath)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error for {url}: {e}")
        return False
    except Exception as e:
        print(f"✗ An error occurred for {url}: {e}")
        return False

def main():
    """Main function to run the Ubuntu Image Fetcher."""
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Get URLs from user (comma-separated or single URL)
    urls_input = input("Please enter image URL(s) (comma-separated for multiple): ")
    urls = [url.strip() for url in urls_input.split(',') if url.strip()]

    if not urls:
        print("✗ No valid URLs provided.")
        return

    # Process each URL
    successful_fetches = 0
    for url in urls:
        if fetch_and_save_image(url):
            successful_fetches += 1

    print(f"\nConnection strengthened. Community enriched. ({successful_fetches}/{len(urls)} images fetched)")

if __name__ == "__main__":
    main()