# MemeWarriors Backend API

## Overview
This is the backend service for the MemeWarriors project, built with:
- FastAPI
- SQLAlchemy
- Pydantic
- OpenAI for AI image generation

## Getting Started

### 1. Install dependencies
```
pip install -r requirements.txt
```

### 2. Set up environment variables
Copy the `.env.example` file to `.env` and fill in your configuration:
```
cp .env.example .env
```

You'll need to set at least:
- `OPENAI_API_KEY` - Your OpenAI API key for image generation

> ⚠️ **IMPORTANT**: Never commit your `.env` file to version control. It contains sensitive information like API keys. The `.env` file is already in `.gitignore` to prevent accidental commits.

### 3. Initialize the database and run the server
```
python run.py
```

This will:
- Create necessary database tables
- Populate test data
- Start the server on http://localhost:8000

## API Documentation
Once the server is running, you can access the API documentation at:
- http://localhost:8000/docs - Swagger UI
- http://localhost:8000/redoc - ReDoc

## Deployment to Vercel

To deploy this API to Vercel:

1. Make sure you have the Vercel CLI installed:
```
npm i -g vercel
```

2. Login to Vercel:
```
vercel login
```

3. Deploy the project:
```
vercel
```

4. Configure environment variables in the Vercel dashboard:
   - Go to your project settings
   - Add your `OPENAI_API_KEY` and other required variables

5. For production deployment:
```
vercel --prod
```

### Storage in Vercel

Since Vercel has an ephemeral filesystem, you'll need to:
1. Use cloud storage for generated images
2. Use a database service like Vercel Postgres for persistent data

## Testing the Meme Generation API

For frontend testing, there are two ways to test the meme generation without real authentication:

### Option 1: Use the test endpoint
```
POST /meme/generate_test

{
  "prompt": "A theme of taiwan food"
}
```
This endpoint doesn't require authentication and doesn't save to the database.

### Option 2: Use test mode with the regular endpoint
```
POST /meme/generate?test_mode=true

{
  "prompt": "A theme of taiwan food"
}
```
This uses the regular endpoint but with a test user, and it will save the generated memes to the database.

## Project Structure
- `app/` - Main application code
  - `config/` - Configuration settings
  - `models/` - SQLAlchemy database models
  - `routers/` - API route handlers
  - `schemas/` - Pydantic models for request/response validation
  - `utils/` - Utility functions (auth, AI, blockchain)
- `init_db.py` - Database initialization script
- `run.py` - Script to run the server

## Security Considerations

1. **API Keys**: Store your API keys in `.env` and never commit this file
2. **Authentication**: For production, implement proper wallet signature verification
3. **Rate Limiting**: Consider adding rate limiting for AI generation endpoints
