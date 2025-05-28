# Instagram Bot with n8n and Dual AI Support

An advanced Instagram automation bot using n8n for workflow automation with dual AI support (Claude AI + OpenAI) for intelligent content generation, comparison, and fallback capabilities.

## ✨ Features

- 🤖 **Dual AI Support**: Claude AI + OpenAI for content generation
- 🔄 **Smart Fallback**: Automatic switching between AI providers
- 📊 **Content Comparison**: Generate with both AIs and choose the best
- 🐳 **Docker Integration**: Containerized n8n workflow automation
- 🌐 **Ngrok Support**: External webhook access with auto-URL updates
- 📱 **Instagram Integration**: Full Instagram API support
- 🛡️ **Secure Setup**: Environment-based configuration
- 🔧 **Easy Deployment**: One-command setup with Docker Compose

## Prerequisites

- Docker and Docker Compose
- Ngrok account and installation
- Meta Developer Account (for Instagram API)
- AI API Keys (choose one or both):
  - Anthropic API Key (for Claude AI)
  - OpenAI API Key (for GPT models)

## Setup Instructions

### Initial Setup

1. Clone the repository:

   ```bash
   git clone <your-repo-url>
   cd instagram-bot
   ```

2. Environment Setup

   Copy `.env.example` to `.env` and fill in your real values (never commit secrets):

   ```bash
   cp .env.example .env
   ```

   > **Note:** Both n8n and Python scripts use the same `.env` file for configuration. No sensitive keys are hardcoded in code. Always keep your `.env` file out of version control.

### Ngrok Configuration

1. Download from [Ngrok website](https://ngrok.com/download)
2. Authenticate:

   ```bash
   ngrok config add-authtoken YOUR_NGROK_TOKEN
   ```

3. (Recommended) Use the automation script to keep ngrok running and your .env updated:

   ```powershell
   .\keep_ngrok_alive.ps1
   ```

   This script will:
   - Start ngrok if not running
   - Monitor the public URL
   - Automatically update your .env file with the latest ngrok URL for n8n
   - Ensure your webhooks and editor URL always work externally

4. (Manual alternative) Start tunnel directly:

   ```bash
   ngrok http 5678
   ```

   If you use this method, remember to update your .env file with the new URL each time ngrok restarts.

### Launch n8n

```bash
docker-compose up -d
```

#### Access Points

- Local: `http://localhost:5678`
- Public: Your Ngrok URL (see your ngrok terminal or the Ngrok Dashboard: `http://localhost:4040`)

## Configuration

### Instagram Setup

1. Create Meta Developer account
2. Configure Instagram Basic Display API
3. Generate access token
4. Update `.env` file

### AI Setup

#### Claude AI Setup
1. Get API key from [Anthropic](https://console.anthropic.com/)
2. Update `.env` file with `CLAUDE_API_KEY`

#### OpenAI Setup
1. Get API key from [OpenAI](https://platform.openai.com/api-keys)
2. Update `.env` file with `OPENAI_API_KEY`

#### Dual AI Support
- Use both Claude and OpenAI for content generation
- Compare outputs and choose the best results
- Fallback support if one service is unavailable

## 🚀 Usage

### Testing Your Setup

1. **Test Environment Variables**:
   ```bash
   python test_env.py
   ```

2. **Test AI Connections**:
   ```bash
   # Test Claude AI
   python test_claude.py

   # Test OpenAI
   python test_openai.py
   ```

3. **Generate Content with Both AIs**:
   ```bash
   python ai_content_generator.py
   ```

### Using the AI Content Generator

```python
from ai_content_generator import AIContentGenerator

# Initialize the generator
generator = AIContentGenerator()

# Generate content with Claude
claude_result = generator.generate_with_claude(
    topic="Instagram Growth Tips",
    power_words="proven, explosive, secret",
    emotion="excitement and urgency",
    cta="Save this post!",
    niche="social media marketing"
)

# Generate content with OpenAI
openai_result = generator.generate_with_openai(
    topic="Instagram Growth Tips",
    power_words="proven, explosive, secret",
    emotion="excitement and urgency",
    cta="Save this post!",
    niche="social media marketing"
)

# Compare both outputs
comparison = generator.compare_outputs(
    topic="Instagram Growth Tips",
    power_words="proven, explosive, secret",
    emotion="excitement and urgency",
    cta="Save this post!",
    niche="social media marketing"
)
```

### n8n Workflow Integration

1. Access n8n interface at `http://localhost:5678`
2. Import workflows from the n8n-data directory
3. Configure workflow settings with your API keys
4. Set up Python script nodes to call the AI generators
5. Activate workflows for automated content generation

## 📁 Project Structure

```
instagram-bot/
├── 📄 ai_content_generator.py      # Main AI content generator with dual support
├── 📄 test_claude.py               # Claude AI connection test
├── 📄 test_openai.py               # OpenAI connection test
├── 📄 test_env.py                  # Environment variables test
├── 📄 docker-compose.yml           # n8n container configuration
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env.example                 # Environment template
├── 📄 .gitignore                   # Git ignore rules
├── 📄 README.md                    # This file
├── 📄 LICENSE                      # MIT license
├── 📁 templates/                   # AI prompt templates
│   ├── claude_prompt.py            # Claude-specific prompts
│   └── openai_prompt.py            # OpenAI-specific prompts
├── 📁 n8n-data/                    # n8n workflows and data (auto-created)
└── 📁 keep_*_alive.*               # Automation scripts for ngrok/n8n
```

### Key Files Explained

- **`ai_content_generator.py`**: Main class for generating content with both AI providers
- **`test_*.py`**: Individual test scripts for each component
- **`templates/`**: Structured prompts optimized for each AI provider
- **`docker-compose.yml`**: Runs n8n with all necessary environment variables
- **`.env.example`**: Template showing all required environment variables

## Security Guidelines

- Never commit `.env` file
- Secure API keys and tokens
- Use HTTPS connections
- Rotate access tokens regularly

## 💰 AI Billing Setup

Both AI services require billing setup for API access:

### Claude AI (Anthropic)
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Go to "Plans & Billing"
3. Add payment method and purchase credits
4. **Recommended**: Start with $5-20 for testing

### OpenAI
1. Visit [OpenAI Platform](https://platform.openai.com/account/billing)
2. Add payment method
3. Set usage limits to control costs
4. **Recommended**: Start with $5-20 for testing

### Cost Optimization Tips
- Set monthly usage limits
- Monitor usage in respective dashboards
- Use Claude for creative content (often better results)
- Use OpenAI for technical content or as fallback
- Test with small amounts first

## 🛠️ Troubleshooting

### Common Issues

1. **"insufficient_quota" or "credit balance too low"**
   - Add billing/credits to your AI service accounts
   - Check usage limits and billing status

2. **"model_not_found" error**
   - Verify you have access to the requested model
   - Try using `gpt-3.5-turbo` instead of `gpt-4` for OpenAI

3. **Environment variables not loading**
   - Ensure `.env` file exists (copy from `.env.example`)
   - Run `python test_env.py` to verify setup

4. **Docker container issues**
   - Restart with `docker-compose down && docker-compose up -d`
   - Check logs with `docker-compose logs`

## ⚠️ Important Disclaimers

- **Use Your Own Credentials**: This project requires your own Instagram API tokens, AI API keys, and ngrok account
- **Separate Instances**: Each installation runs independently - your setup won't affect others and vice versa
- **Compliance**: Ensure your usage complies with Instagram's Terms of Service and API guidelines
- **Rate Limits**: Be mindful of Instagram API rate limits to avoid account restrictions
- **Testing**: Test thoroughly in a development environment before using with production accounts
- **AI Costs**: Monitor your AI usage to avoid unexpected charges

## Contributing

1. Fork repository
2. Create feature branch
3. Make changes
4. Submit pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
