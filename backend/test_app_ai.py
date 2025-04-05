import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY is not set in the .env file")
    sys.exit(1)

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Create meme_images directory if it doesn't exist
os.makedirs("meme_images", exist_ok=True)

# Import AI utilities from the app
from app.utils.ai import generate_meme_image, generate_meme_soldier_name, clean_and_parse_prompt
from app.config.settings import settings

def test_prompt(prompt):
    """Test a specific prompt with the AI utilities"""
    print(f"\n=== Testing Prompt: '{prompt}' ===")
    
    # Test prompt parsing
    print("\nParsing prompt...")
    parsed_prompts = clean_and_parse_prompt(prompt)
    print(f"Parsed into: {parsed_prompts}")
    
    # Test image generation
    print("\nGenerating meme images...")
    image_result = generate_meme_image(prompt)
    
    if not image_result["success"]:
        print(f"Error: {image_result.get('error', 'Unknown error')}")
        return False
    
    # Display results
    print(f"\nGenerated {len(image_result['items'])} meme items:")
    for idx, item in enumerate(image_result["items"]):
        print(f"\nItem {idx+1}:")
        print(f"  Prompt: {item['prompt']}")
        print(f"  Image path: {item['image_path']}")
        print(f"  Image URL: {item['image_url']}")
        print(f"  Coin icon URL: {item['coin_icon_url']}")
        
        # Generate and display name
        name = generate_meme_soldier_name(item["prompt"])
        print(f"  Generated name: {name}")
    
    return True

if __name__ == "__main__":
    # Test prompts to try
    test_prompts = [
        "A theme of taiwan food",
        "Make memes about cats",
        "Anime character, superhero",
        "Pixel art game characters"
    ]
    
    # Use command line argument if provided, otherwise use the first test prompt
    prompt = sys.argv[1] if len(sys.argv) > 1 else test_prompts[0]
    
    # Test the specified prompt
    test_prompt(prompt) 