#!/usr/bin/env python3

def get_instagram_prompt(topic, power_words, emotion, cta, niche):
    """
    Generate a structured prompt for Claude to create Instagram carousel content
    """
    claude_prompt = f"""
    Generate 3 Instagram Carousels about {topic} that will engage and provide value to the audience.
    
    Follow these guidelines for each carousel:
    
    1. AIDA Model Structure:
       - Attention: Hook the reader instantly
       - Interest: Build curiosity
       - Desire: Show benefits/value
       - Action: Clear next steps
    
    2. Use these power words: "{power_words}"
    
    3. Target emotion to evoke: {emotion}
    
    4. End with this call to action (CTA): "{cta}"
    
    5. Include exactly 5 trending hashtags related to: {niche}
    
    For each carousel, provide:
    1. Compelling headline
    2. Clear description of what each slide should show visually
    3. Engaging copy that follows the AIDA model
    
    Format each carousel as:
    [Headline]
    [Slide 1-5 Visual Descriptions]
    [Copy]
    [Hashtags]
    
    Make sure each carousel is separated by '---'
    """
    return claude_prompt

# Example usage
if __name__ == "__main__":
    example_prompt = get_instagram_prompt(
        topic="Digital Marketing Tips",
        power_words="exclusive, proven, secret, powerful, transform",
        emotion="curiosity and motivation",
        cta="DM 'TIPS' for our free marketing guide",
        niche="digital marketing"
    )
    print(example_prompt)
