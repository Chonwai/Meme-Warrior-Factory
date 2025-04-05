from app.main import app

# This file serves as the entry point for Vercel deployment
# For Vercel deployment, we're using a streamlined set of requirements
# in requirements-vercel.txt to avoid build issues with aiohttp and web3

# Entry point for Vercel
handler = app
 