# 🚀 Netra - Deployment Ready

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
