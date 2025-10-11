#!/usr/bin/env python3
"""
Setup script to help configure environment variables
"""
import os

def setup_environment():
    print("🔧 WaterSafe Backend Environment Setup")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"✅ Found {env_file} file")
    else:
        print(f"❌ {env_file} file not found")
        print("Creating .env file...")
        
        # Create .env file
        with open(env_file, 'w') as f:
            f.write("# OpenAI API Configuration\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n\n")
            f.write("# Database Configuration (if needed)\n")
            f.write("# DATABASE_URL=your_database_url_here\n\n")
            f.write("# Server Configuration\n")
            f.write("HOST=0.0.0.0\n")
            f.write("PORT=8000\n")
        
        print(f"✅ Created {env_file} file")
    
    # Check current API key
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your_openai_api_key_here":
        print(f"✅ OpenAI API Key is configured")
        print(f"   Key starts with: {api_key[:10]}...")
    else:
        print("❌ OpenAI API Key is not configured")
        print("\n📝 To configure your API key:")
        print("1. Get your API key from: https://platform.openai.com/api-keys")
        print("2. Edit the .env file and replace 'your_openai_api_key_here' with your actual key")
        print("3. Or set it as an environment variable: export OPENAI_API_KEY=your_key_here")
    
    print("\n🚀 To start the server:")
    print("   python main.py")
    
    print("\n📚 API Documentation will be available at:")
    print("   http://localhost:8000/docs")

if __name__ == "__main__":
    setup_environment()
