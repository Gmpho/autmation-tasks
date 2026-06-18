#!/usr/bin/env python3

def build_instagram_prompt(topic, power_words, emotion, cta, niche):
    prompt = f"""
    Create 3 engaging Instagram carousel posts about {topic} that will captivate and provide value to the audience.

    Requirements for each carousel:

    1. Structure using AIDA Framework:
       - Attention: Create an irresistible hook
       - Interest: Build genuine curiosity
       - Desire: Demonstrate clear value/benefits
       - Action: Include compelling next steps

    2. Incorporate these power words naturally: "{power_words}"

    3. Evoke this emotion: {emotion}

    4. Include this call to action: "{cta}"

    5. Add exactly 5 trending hashtags for: {niche}

    For each carousel, provide:
    - Eye-catching headline
    - Visual description for each of 5 slides
    - Engaging copy following AIDA structure
    - Strategic hashtag placement

    Format:
    **Carousel [Number]**
    Headline: [Title]

    Slide Visuals:
    1. [Description]
    2. [Description]
    3. [Description]
    4. [Description]
    5. [Description]

    Copy:
    [AIDA-structured content]

    Hashtags: [5 hashtags]

    ---

    Make content authentic, valuable, and scroll-stopping.
    """
    return prompt


def build_story_prompt(topic, style="casual"):
    prompt = f"""
    Create 5 Instagram Story slides about {topic}.

    Style: {style}

    For each story slide, provide:
    1. Visual description
    2. Text overlay (keep under 50 characters)
    3. Interactive element suggestion (poll, question, etc.)

    Make stories engaging and encourage interaction.

    Format each as:
    **Story [Number]**
    Visual: [Description]
    Text: [Overlay text]
    Interactive: [Element type and question]
    ---
    """
    return prompt


if __name__ == "__main__":
    example = build_instagram_prompt(
        topic="Digital Marketing Tips",
        power_words="exclusive, proven, secret, powerful, transform",
        emotion="curiosity and motivation",
        cta="DM 'TIPS' for our free marketing guide",
        niche="digital marketing"
    )
    print(example)
