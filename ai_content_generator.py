#!/usr/bin/env python3
import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic
from openai import OpenAI
from templates.claude_prompt import get_instagram_prompt
from templates.openai_prompt import get_instagram_prompt_openai, get_story_prompt_openai

# Load environment variables from .env file
load_dotenv()

class AIContentGenerator:
    def __init__(self):
        self.claude_client = None
        self.openai_client = None
        self._initialize_clients()

    def _initialize_clients(self):
        """Initialize AI clients with API keys from environment"""
        claude_key = os.getenv('CLAUDE_API_KEY')
        openai_key = os.getenv('OPENAI_API_KEY')

        if claude_key:
            self.claude_client = Anthropic(api_key=claude_key)
            print("✅ Claude client initialized")
        else:
            print("⚠️ Claude API key not found")

        if openai_key:
            self.openai_client = OpenAI(api_key=openai_key)
            print("✅ OpenAI client initialized")
        else:
            print("⚠️ OpenAI API key not found")

    def generate_with_claude(self, topic, power_words, emotion, cta, niche):
        """Generate content using Claude AI"""
        if not self.claude_client:
            raise ValueError("Claude client not initialized")

        prompt = get_instagram_prompt(topic, power_words, emotion, cta, niche)

        message = self.claude_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        return {
            "provider": "Claude",
            "content": message.content[0].text,
            "model": "claude-3-sonnet-20240229"
        }

    def generate_with_openai(self, topic, power_words, emotion, cta, niche):
        """Generate content using OpenAI"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")

        prompt = get_instagram_prompt_openai(topic, power_words, emotion, cta, niche)

        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            max_tokens=2000,
            temperature=0.7
        )

        return {
            "provider": "OpenAI",
            "content": response.choices[0].message.content,
            "model": "gpt-3.5-turbo"
        }

    def generate_stories_openai(self, topic, style="casual"):
        """Generate Instagram Stories using OpenAI"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")

        prompt = get_story_prompt_openai(topic, style)

        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            max_tokens=1500,
            temperature=0.8
        )

        return {
            "provider": "OpenAI",
            "content": response.choices[0].message.content,
            "model": "gpt-3.5-turbo",
            "type": "stories"
        }

    def compare_outputs(self, topic, power_words, emotion, cta, niche):
        """Generate content with both AI providers for comparison"""
        results = {}

        try:
            if self.claude_client:
                results['claude'] = self.generate_with_claude(topic, power_words, emotion, cta, niche)
        except Exception as e:
            results['claude'] = {"error": str(e)}

        try:
            if self.openai_client:
                results['openai'] = self.generate_with_openai(topic, power_words, emotion, cta, niche)
        except Exception as e:
            results['openai'] = {"error": str(e)}

        return results

# Example usage and testing
if __name__ == "__main__":
    generator = AIContentGenerator()

    # Test parameters
    test_params = {
        "topic": "Instagram Growth Strategies",
        "power_words": "proven, explosive, secret, ultimate, guaranteed",
        "emotion": "motivation and urgency",
        "cta": "Save this post for later!",
        "niche": "social media marketing"
    }

    print("🚀 Generating content with both AI providers...\n")

    # Compare both providers
    results = generator.compare_outputs(**test_params)

    for provider, result in results.items():
        print(f"{'='*50}")
        print(f"🤖 {provider.upper()} RESULT")
        print(f"{'='*50}")
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"Model: {result['model']}")
            print(f"Content:\n{result['content']}")
        print("\n")
