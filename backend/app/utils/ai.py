import os
import requests
import time
import random
import string
from openai import OpenAI
from PIL import Image
from io import BytesIO
import asyncio

# Initialize OpenAI client with fallback to environment variables
try:
    from app.config.settings import settings
    api_key = settings.OPENAI_API_KEY
    meme_storage_path = settings.MEME_STORAGE_PATH
except ImportError:
    # Fallback for Vercel environment
    api_key = os.environ.get('OPENAI_API_KEY')
    meme_storage_path = os.environ.get('MEME_STORAGE_PATH', './meme_images')

# Safeguard for missing API key
if not api_key:
    print("WARNING: OpenAI API key is not set!")

# Check for Vercel Blob token
BLOB_TOKEN = os.environ.get('BLOB_READ_WRITE_TOKEN')
IN_VERCEL = os.environ.get('VERCEL') == '1'

if IN_VERCEL and not BLOB_TOKEN:
    print("WARNING: Running in Vercel but BLOB_READ_WRITE_TOKEN is not set!")
else:
    os.environ["BLOB_READ_WRITE_TOKEN"] = BLOB_TOKEN

# Initialize OpenAI client
try:
    client = OpenAI(api_key=api_key)
    print(f"OpenAI client initialized successfully with API key starting with: {api_key[:4] if api_key else 'None'}")
except Exception as e:
    print(f"Error initializing OpenAI client: {str(e)}")
    # Create a dummy client that will raise clear errors
    class DummyClient:
        def __getattr__(self, name):
            def method(*args, **kwargs):
                raise ValueError("OpenAI client is not properly initialized. Check OPENAI_API_KEY.")
            return method
    
    client = DummyClient()

def generate_random_name(prefix="MemeSoldier"):
    """Generate a random name for a meme soldier"""
    random_suffix = ''.join(random.choice(string.ascii_lowercase) for _ in range(5))
    return f"{prefix}_{random_suffix}"

def clean_and_parse_prompt(prompt):
    """Clean and parse the user prompt to identify distinct items for meme generation
    
    If multiple items are detected, return the first two. If only one item is found,
    use creative prompt engineering to derive a second related item.
    """
    try:
        # First try to use GPT to parse and limit the prompt
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are a prompt parser for a meme image generation system. Your task is to identify exactly 2 distinct items from the user's input.

IMPORTANT RULE: When the user mentions a broad theme or category (e.g., "theme of taiwan food"), don't return the theme itself. Instead, identify 2 specific, concrete examples that represent that theme (e.g., "Bubble tea" and "Taiwanese hot pot").

If the user mentions more than 2 items, select the 2 most interesting or distinctive ones.
If the user mentions only 1 specific item, create a second related item that would pair well with it.

Examples:
- Input: "A theme of taiwan food" → Output: ["Bubble tea", "Taiwanese hot pot"]
- Input: "Make memes about cats" → Output: ["Cat knocking things off a table", "Cat sleeping in a weird position"]
- Input: "Anime character, superhero" → Output: ["Anime character with big eyes", "Muscular superhero in colorful costume"]

Return ONLY a JSON array with exactly 2 strings, nothing else."""},
                {"role": "user", "content": f"Parse this request and give me exactly 2 distinct items to generate: '{prompt}'"}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        parsed_text = response.choices[0].message.content.strip()
        
        # Try to extract JSON list or fallback to simple parsing
        try:
            # Handle various formats the AI might return
            if parsed_text.startswith('[') and parsed_text.endswith(']'):
                import json
                items = json.loads(parsed_text)
                if isinstance(items, list) and len(items) >= 2:
                    return items[:2]
            
            # If we couldn't parse JSON, use fallback parsing
            if '1.' in parsed_text and '2.' in parsed_text:
                lines = [line.strip() for line in parsed_text.split('\n') if line.strip()]
                items = []
                for line in lines:
                    if line.startswith('1.') or line.startswith('2.'):
                        items.append(line.split('.', 1)[1].strip())
                if len(items) >= 2:
                    return items[:2]
        except:
            pass
        
        # If all else fails, do simple fallback parsing
        if ',' in prompt:
            items = [item.strip() for item in prompt.split(',')]
            if len(items) >= 2:
                return items[:2]
            else:
                return [items[0], f"Pixel art {items[0]} in a different style"]
        else:
            return [prompt, f"Pixel art variant of {prompt}"]
        
    except Exception:
        # Ultimate fallback
        if ',' in prompt:
            items = [item.strip() for item in prompt.split(',')]
            return items[:2] if len(items) >= 2 else [prompt, f"Pixel art variant of {prompt}"]
        else:
            return [prompt, f"Pixel art variant of {prompt}"]

async def upload_to_vercel_blob(image_data, filename):
    """Upload image data to Vercel Blob storage"""
    try:
        # Set environment variable
        os.environ["BLOB_READ_WRITE_TOKEN"] = BLOB_TOKEN
        
        # Import the Vercel Blob SDK
        from vercel_blob import put, PutOptions
        
        # Upload to Vercel Blob
        blob = await put(filename, image_data, PutOptions(access="public"))
        
        # Return the URL
        return {
            "success": True,
            "url": blob.url
        }
    except Exception as e:
        print(f"Error uploading to Vercel Blob: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

async def generate_meme_image(prompt):
    """Generate meme images using OpenAI DALL-E based on parsed prompt"""
    try:
        # Parse the prompt into 2 distinct items
        parsed_prompts = clean_and_parse_prompt(prompt)
        results = []
        
        # Check if we're running in Vercel
        in_vercel = os.environ.get('VERCEL') == '1'
        
        for idx, item_prompt in enumerate(parsed_prompts):
            try:
                # Format the prompt to specifically request an icon-style image
                icon_prompt = f"""Create a simple, clean, pixel art icon of {item_prompt}. 
The image should:
- Be a single object or character with a simple background
- Have a clean, minimalist design suitable for an icon
- Use pixel art style with clear outlines and flat colors
- NOT be a comic panel, scene, or conversational image
- Centered composition with the subject taking up most of the frame
- Be suitable for use as a game character icon or token"""
                
                # Generate image with DALL-E
                response = client.images.generate(
                    model="dall-e-2",
                    prompt=icon_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                
                # Get the image URL
                image_url = response.data[0].url
                file_name = f"{int(time.time())}_{idx}_{generate_random_name()}.png"
                
                if in_vercel:
                    # In Vercel environment, use Blob storage if possible
                    if BLOB_TOKEN:
                        try:
                            # Download the image from DALL-E
                            image_response = requests.get(image_url)
                            if image_response.status_code == 200:
                                # Upload to Vercel Blob
                                blob_result = await upload_to_vercel_blob(image_response.content, file_name)
                                if blob_result["success"]:
                                    # We have successfully uploaded to Blob storage
                                    results.append({
                                        "prompt": item_prompt,
                                        "image_path": "vercel_blob",
                                        "image_url": blob_result["url"],
                                        "coin_icon_url": blob_result["url"]  # For now, use same URL
                                    })
                                    continue
                        except Exception as blob_error:
                            print(f"Error using Blob storage: {str(blob_error)}")
                            # Fallback to using DALL-E URL directly
                    
                    # Fallback: use DALL-E URL directly
                    results.append({
                        "prompt": item_prompt,
                        "image_path": "dalle_direct",
                        "image_url": image_url,  # Use the DALL-E URL directly
                        "coin_icon_url": image_url  # Use the same URL for coin icon
                    })
                else:
                    # For local development, save to filesystem
                    image_response = requests.get(image_url)
                    if image_response.status_code != 200:
                        continue
                    
                    # Save the image
                    os.makedirs(meme_storage_path, exist_ok=True)
                    file_path = os.path.join(meme_storage_path, file_name)
                    
                    with open(file_path, "wb") as f:
                        f.write(image_response.content)
                    
                    # Create a coin icon (simplified version of the image)
                    create_coin_icon(image_response.content, file_name)
                    
                    results.append({
                        "prompt": item_prompt,
                        "image_path": file_path,
                        "image_url": f"/images/{file_name}",
                        "coin_icon_url": f"/images/coin_{file_name}"
                    })
            except Exception as item_error:
                print(f"Error generating item {idx}: {str(item_error)}")
                # Continue with next item
                continue
        
        # If we didn't generate any items successfully, return an error
        if not results:
            return {
                "success": False,
                "error": "Failed to generate any images"
            }
            
        return {
            "success": True,
            "items": results
        }
    except Exception as e:
        print(f"AI Error: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

def create_coin_icon(image_data, original_filename):
    """Create a circular coin icon from the meme image"""
    # Skip in Vercel environment
    if IN_VERCEL:
        return False
        
    try:
        # Open the image
        img = Image.open(BytesIO(image_data))
        
        # Create a square crop
        width, height = img.size
        size = min(width, height)
        left = (width - size) // 2
        top = (height - size) // 2
        right = left + size
        bottom = top + size
        img = img.crop((left, top, right, bottom))
        
        # Resize to coin size
        img = img.resize((256, 256))
        
        # Save the coin icon
        coin_filename = f"coin_{original_filename}"
        coin_path = os.path.join(meme_storage_path, coin_filename)
        img.save(coin_path)
        
        return True
    except Exception:
        return False

def generate_meme_soldier_name(prompt):
    """Generate a creative name for a meme soldier based on the prompt"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative meme name generator. Generate a short, catchy, memorable name for a meme character based on the prompt. The name should be 1-3 words only."},
                {"role": "user", "content": f"Generate a catchy meme soldier name based on this description: {prompt}"}
            ],
            max_tokens=20
        )
        
        name = response.choices[0].message.content.strip()
        # Remove quotes if present
        name = name.strip('"\'')
        
        return name if name else generate_random_name()
    except Exception:
        # Fallback to random name
        return generate_random_name() 


