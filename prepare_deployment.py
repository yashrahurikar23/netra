#!/usr/bin/env python3
"""
Prepare Netra app for deployment to Streamlit Community Cloud (FREE).
This script optimizes the app for the free tier and creates necessary files.
"""

import os
import shutil
from pathlib import Path

def create_packages_txt():
    """Create packages.txt for system dependencies."""
    packages_content = """libgl1-mesa-glx
libglib2.0-0
"""
    with open("packages.txt", "w") as f:
        f.write(packages_content)
    print("✓ Created packages.txt")

def create_secrets_template():
    """Create secrets template for Streamlit Cloud."""
    secrets_content = """# Secrets for Streamlit Community Cloud
# Add these in your Streamlit Cloud dashboard under "Secrets"

[general]
email = "your-email@example.com"

[openai]
api_key = "your-openai-api-key-here"

[simulation]
default_mission_duration = 3600
default_time_step = 1.0

[rag]
chroma_db_path = "./data/chroma_db"
collection_name = "space_missions"
"""
    
    streamlit_dir = Path(".streamlit")
    streamlit_dir.mkdir(exist_ok=True)
    
    with open(streamlit_dir / "secrets_template.toml", "w") as f:
        f.write(secrets_content)
    print("✓ Created .streamlit/secrets_template.toml")

def optimize_requirements():
    """Create optimized requirements for deployment."""
    optimized_requirements = """# Netra - Optimized for Streamlit Community Cloud
streamlit>=1.31.0
plotly>=5.17.0
pandas>=2.0.0
numpy>=1.24.0
python-dotenv>=1.0.0
protobuf==3.20.3

# RAG dependencies (comment out if not using OpenAI)
llama-index>=0.10.0
llama-index-llms-openai>=0.1.0
llama-index-embeddings-openai>=0.1.0
llama-index-vector-stores-chroma>=0.1.0
chromadb>=0.4.0
openai>=1.12.0

# Additional utilities
requests>=2.31.0
pydantic>=2.5.0
"""
    
    with open("requirements_deploy.txt", "w") as f:
        f.write(optimized_requirements)
    print("✓ Created requirements_deploy.txt (optimized for deployment)")

def create_app_entry():
    """Create main app.py for Streamlit Cloud."""
    app_content = """#!/usr/bin/env python3
\"\"\"
Main entry point for Netra on Streamlit Community Cloud.
Optimized for free tier deployment.
\"\"\"

import os
import sys
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Set environment variables for deployment
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    \"\"\"Launch the Netra application.\"\"\"
    try:
        # Import and run the main app
        from ui.main_app import main as streamlit_main
        streamlit_main()
    except ImportError as e:
        import streamlit as st
        st.error(f"Import error: {e}")
        st.write("Please check that all dependencies are installed correctly.")
        st.code("pip install -r requirements.txt")
    except Exception as e:
        import streamlit as st
        st.error(f"Application error: {e}")
        st.write("Please check the logs for more details.")

if __name__ == "__main__":
    main()
"""
    
    with open("streamlit_app.py", "w") as f:
        f.write(app_content)
    print("✓ Created streamlit_app.py (entry point for Streamlit Cloud)")

def update_config_for_deployment():
    """Update Streamlit config for deployment."""
    config_content = """[global]
developmentMode = false
showWarningOnDirectExecution = false

[server]
headless = true
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = false
toolbarMode = "minimal"
"""
    
    config_path = Path(".streamlit/config.toml")
    with open(config_path, "w") as f:
        f.write(config_content)
    print("✓ Updated .streamlit/config.toml for deployment")

def create_gitignore():
    """Create/update .gitignore for deployment."""
    gitignore_content = """# Netra deployment .gitignore

# Virtual environment
.venv/
venv/
env/

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd
.Python

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Secrets and environment
.env
.streamlit/secrets.toml

# Data directories (too large for git)
data/chroma_db/
data/processed/
data/synthetic/

# Logs
*.log
logs/

# Temporary files
tmp/
temp/
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    print("✓ Created/updated .gitignore")

def create_readme_deployment():
    """Create deployment-specific README."""
    readme_content = """# 🚀 Netra - Deployment Ready

This version is optimized for deployment to **Streamlit Community Cloud** (FREE).

## Quick Deploy to Streamlit Cloud

1. **Make sure your repository is public on GitHub**

2. **Go to [share.streamlit.io](https://share.streamlit.io)**

3. **Connect your GitHub account and select this repository**

4. **Set the main file path to:** `streamlit_app.py`

5. **Add your secrets in the Streamlit Cloud dashboard:**
   - Copy contents from `.streamlit/secrets_template.toml`
   - Paste into "Secrets" section in your app dashboard
   - Add your actual OpenAI API key

6. **Deploy!** Your app will be available at `https://your-username-netra-main-streamlit-app.streamlit.app`

## Local Testing

```bash
# Test with deployment configuration
streamlit run streamlit_app.py

# Or use the original entry point
streamlit run src/ui/main_app.py
```

## Files for Deployment

- `streamlit_app.py` - Main entry point for Streamlit Cloud
- `requirements_deploy.txt` - Optimized dependencies
- `packages.txt` - System packages for Streamlit Cloud
- `.streamlit/config.toml` - Production configuration
- `.streamlit/secrets_template.toml` - Template for secrets

## Troubleshooting

If you encounter issues:

1. **Protobuf errors:** The app sets `PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python` automatically
2. **Memory errors:** The app is optimized for the 1GB limit on free tier
3. **Missing secrets:** Make sure to add your OpenAI API key in the Streamlit Cloud dashboard

## Cost

**Completely FREE** on Streamlit Community Cloud!

- No credit card required
- Public repositories only
- 1GB RAM, 1 CPU core
- Apps sleep after 7 days of inactivity

Perfect for demos, portfolios, and open-source projects.
"""
    
    with open("README_DEPLOYMENT.md", "w") as f:
        f.write(readme_content)
    print("✓ Created README_DEPLOYMENT.md")

def main():
    """Prepare the app for deployment."""
    print("🚀 Preparing Netra for Streamlit Community Cloud deployment...\n")
    
    # Create deployment files
    create_packages_txt()
    create_secrets_template()
    optimize_requirements()
    create_app_entry()
    update_config_for_deployment()
    create_gitignore()
    create_readme_deployment()
    
    print(f"\n✅ Deployment preparation complete!")
    print(f"\n📋 Next Steps:")
    print(f"1. Push your code to GitHub (public repository)")
    print(f"2. Go to https://share.streamlit.io")
    print(f"3. Connect your GitHub repo")
    print(f"4. Set main file: streamlit_app.py")
    print(f"5. Add secrets from .streamlit/secrets_template.toml")
    print(f"6. Deploy! 🚀")
    print(f"\n💡 Your app will be FREE on Streamlit Community Cloud!")
    print(f"\n📖 See README_DEPLOYMENT.md for detailed instructions.")

if __name__ == "__main__":
    main()
