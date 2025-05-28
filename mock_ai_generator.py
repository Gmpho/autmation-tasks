#!/usr/bin/env python3
"""
Mock AI generator for free local testing without API costs
Use this to develop and test your automation workflows before adding real AI
"""

import random
import time

class MockAIGenerator:
    def __init__(self):
        self.sample_posts = [
            "🚀 Boost your Instagram engagement with these proven strategies! Save this post for later. #InstagramGrowth #SocialMedia #DigitalMarketing #ContentCreator #Engagement",
            
            "💡 Secret to viral content: Consistency + Value + Authenticity. Which one do you struggle with most? Comment below! #ContentStrategy #ViralContent #SocialMediaTips #Instagram #Growth",
            
            "📈 Instagram algorithm loves these 5 things: 1) Early engagement 2) Saves & shares 3) Comments 4) Story interactions 5) Consistent posting. Try them today! #Algorithm #InstagramTips #SocialMedia #Growth #Engagement",
            
            "🎯 Stop posting randomly! Plan your content with these tools: 1) Content calendar 2) Analytics tracking 3) Hashtag research 4) Competitor analysis 5) Audience insights #ContentPlanning #SocialMediaStrategy #Instagram #Planning #Success",
            
            "✨ Transform your Instagram bio in 5 steps: 1) Clear value proposition 2) Keywords for discovery 3) Call-to-action 4) Link in bio 5) Personality. What's your bio missing? #InstagramBio #Profile #SocialMedia #Branding #Tips"
        ]
        
        self.sample_stories = [
            "Story 1: Quick tip of the day! Visual: Colorful gradient background with tip text",
            "Story 2: Behind the scenes content. Visual: Workspace or process photo",
            "Story 3: Poll - What content do you want to see more of? Visual: Question sticker",
            "Story 4: User-generated content feature. Visual: Repost with credit",
            "Story 5: Call-to-action for latest post. Visual: Post preview with swipe up"
        ]
    
    def generate_with_claude_mock(self, topic, power_words, emotion, cta, niche):
        """Mock Claude AI response"""
        time.sleep(1)  # Simulate API delay
        
        post = random.choice(self.sample_posts)
        
        return {
            "provider": "Claude (Mock)",
            "content": f"**Mock Claude Response for: {topic}**\n\n{post}\n\nPower words used: {power_words}\nEmotion: {emotion}\nCTA: {cta}\nNiche: {niche}",
            "model": "claude-3-sonnet-mock",
            "cost": "$0.00 (Mock)"
        }
    
    def generate_with_openai_mock(self, topic, power_words, emotion, cta, niche):
        """Mock OpenAI response"""
        time.sleep(1)  # Simulate API delay
        
        post = random.choice(self.sample_posts)
        
        return {
            "provider": "OpenAI (Mock)",
            "content": f"**Mock OpenAI Response for: {topic}**\n\n{post}\n\nPower words: {power_words}\nTarget emotion: {emotion}\nCall-to-action: {cta}\nNiche focus: {niche}",
            "model": "gpt-3.5-turbo-mock",
            "cost": "$0.00 (Mock)"
        }
    
    def generate_stories_mock(self, topic, style="casual"):
        """Mock Instagram Stories"""
        time.sleep(0.5)
        
        stories = random.sample(self.sample_stories, 3)
        
        return {
            "provider": "Mock Stories",
            "content": f"**Mock Stories for: {topic}**\n\n" + "\n".join(stories),
            "model": "stories-mock",
            "type": "stories",
            "cost": "$0.00 (Mock)"
        }
    
    def compare_outputs_mock(self, topic, power_words, emotion, cta, niche):
        """Compare mock outputs from both providers"""
        return {
            'claude': self.generate_with_claude_mock(topic, power_words, emotion, cta, niche),
            'openai': self.generate_with_openai_mock(topic, power_words, emotion, cta, niche)
        }

# Example usage for free testing
if __name__ == "__main__":
    mock_generator = MockAIGenerator()
    
    print("🆓 FREE MOCK AI TESTING")
    print("=" * 50)
    
    # Test parameters
    test_params = {
        "topic": "Instagram Growth Strategies",
        "power_words": "proven, explosive, secret, ultimate, guaranteed",
        "emotion": "motivation and urgency",
        "cta": "Save this post for later!",
        "niche": "social media marketing"
    }
    
    # Test mock comparison
    results = mock_generator.compare_outputs_mock(**test_params)
    
    for provider, result in results.items():
        print(f"\n🤖 {provider.upper()} MOCK RESULT")
        print("-" * 30)
        print(f"Model: {result['model']}")
        print(f"Cost: {result['cost']}")
        print(f"Content:\n{result['content']}")
        print()
    
    # Test stories
    print("\n📱 MOCK INSTAGRAM STORIES")
    print("-" * 30)
    stories = mock_generator.generate_stories_mock("AI Tools for Content Creation")
    print(f"Content:\n{stories['content']}")
    print(f"Cost: {stories['cost']}")
