import os
from dotenv import load_dotenv
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

# Check OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY is not set in the .env file")
    sys.exit(1)

from app.utils.ai import generate_meme_image, generate_meme_soldier_name, clean_and_parse_prompt

def test_prompt_parsing():
    """Test prompt parsing and cleansing"""
    prompts = [
        "A theme of taiwan food",
        # "Generate memes with cats, dogs, and birds",
        # "Pixel art of a samurai"
    ]
    
    for prompt in prompts:
        print(f"\nTesting prompt parsing for: '{prompt}'")
        parsed = clean_and_parse_prompt(prompt)
        print(f"Parsed into 2 items: {parsed}")

def test_meme_generation():
    """Test meme image generation with multi-item support"""
    prompt = "A theme of taiwan food"
    print(f"\nGenerating memes with prompt: '{prompt}'")
    
    result = generate_meme_image(prompt)
    
    if result["success"]:
        print(f"Success! Generated {len(result['items'])} items:")
        for idx, item in enumerate(result["items"]):
            print(f"\nItem {idx+1}:")
            print(f"  Prompt: {item['prompt']}")
            print(f"  Image saved at: {item['image_path']}")
            print(f"  Image URL would be: {item['image_url']}")
            print(f"  Coin icon URL would be: {item['coin_icon_url']}")
    else:
        print(f"Error: {result['error']}")
    
    return result["success"]

def test_name_generation():
    """Test meme soldier name generation"""
    prompts = ["A bowl of Taiwan beef noodles", "Bubble tea drink"]
    
    print("\nTesting name generation:")
    for prompt in prompts:
        name = generate_meme_soldier_name(prompt)
        print(f"  Prompt: '{prompt}' → Name: '{name}'")

if __name__ == "__main__":
    # Create meme_images directory if it doesn't exist
    os.makedirs("meme_images", exist_ok=True)
    
    print("=== Testing Prompt Parsing ===")
    test_prompt_parsing()
    
    print("\n=== Testing Meme Generation ===")
    meme_success = test_meme_generation()
    
    if meme_success:
        print("\n=== Testing Name Generation ===")
        test_name_generation() 