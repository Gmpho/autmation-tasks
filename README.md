# Instagram Bot with n8n and Claude AI

An automated Instagram bot using n8n for workflow automation and Claude AI for content generation.

## Prerequisites

- Docker and Docker Compose
- Ngrok
- Meta Developer Account (for Instagram API)
- Anthropic API Key (for Claude AI)

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

### Claude AI Setup

1. Get API key from Anthropic
2. Update `.env` file

## Usage

1. Access n8n interface
2. Import workflows
3. Configure workflow settings
4. Activate workflows

## Security Guidelines

- Never commit `.env` file
- Secure API keys and tokens
- Use HTTPS connections
- Rotate access tokens regularly

## ⚠️ Important Disclaimers

- **Use Your Own Credentials**: This project requires your own Instagram API tokens, Claude API keys, and ngrok account
- **Separate Instances**: Each installation runs independently - your setup won't affect others and vice versa
- **Compliance**: Ensure your usage complies with Instagram's Terms of Service and API guidelines
- **Rate Limits**: Be mindful of Instagram API rate limits to avoid account restrictions
- **Testing**: Test thoroughly in a development environment before using with production accounts

## Contributing

1. Fork repository
2. Create feature branch
3. Make changes
4. Submit pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
