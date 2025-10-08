import requests

def fetch_image(url, save_path="downloaded_image.jpg"):
    try:
        response = requests.get(url)
        response.raise_for_status()  # check for request errors
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"Image saved to {save_path}")
    except Exception as e:
        print(f"Failed to fetch image: {e}")

# Example usage
fetch_image("https://place.dog/300/200", "my_image.jpg")