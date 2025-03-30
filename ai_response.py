from openai import OpenAI

try:
    from keys import ai_key
    ai_key_final = ai_key
except:
    import os
    ai_key_final = os.environ.get("ai_key", "fallback_secret")


def ai_response(name, genre, plot, target_audience, writing_style, prev_story, choice):
    if prev_story == None:
        prev = "There's no previous story so generate a fresh one"
    else:
        prev = prev_story

    client = OpenAI(
        base_url="https://api.studio.nebius.ai/v1/",
        api_key=ai_key_final
    )

    completion = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-70B-Instruct",
        messages=[
            {"role": "system", "content": f"You are an AI model that generates an incomplete (will be completed later) single-paragraph of a story (~100 words) based on user input. Follow these instructions carefully: Use the user's name ('{name}') as the main character or any role they specify. Write the story in the '{genre}' genre and base it on the given plot description. Ensure the story aligns with the target audience: '{target_audience}', and follows the requested writing style: '{writing_style}'. If a previous story paragraph is provided, use it as a continuation while maintaining consistency and integrating the impact of the user's last choice: '{choice}'. If previous story is 'None', generate a fresh paragraph starting the story. STRICT FORMAT RULES (DO NOT IGNORE): 1. ALWAYS start with a 5-word scene description, then exactly one '&' symbol. Example: 'A storm rages over the city & The wind howled through the deserted streets as Bhavya tightened his cloak...'. 2. DO NOT add any extra text or explanations—just the story. 3. MUST end with exactly two choices, each separated by a single '&' symbol. Example: '& [Choice 1] & [Choice 2]'. 4. DO NOT add any words like 'Do they:', 'Options:', 'Choices:', etc. The choices must appear immediately after the story and be separated only by '&'. 5. The final output must be structured like this: '[5-word scene description] & [Story paragraph] & [Choice 1] & [Choice 2]'. 6. If continuing from a previous paragraph, incorporate the user's last choice: '{choice}'. Failure to follow these rules exactly will result in incorrect output. Generate the response with absolute precision. Description of the story: {plot}]. Previous paragraph generated: {prev}. User chose '{choice}' in previous paragraph."}
        ],
        temperature=0.7,
    )

    result = str(completion.choices[0].message.content)

    title  = result.split('&')[0]
    paragraph = result.split('&')[1]
    choice1  = result.split('&')[2]
    choice2 = result.split('&')[3]

    return title, paragraph, choice1, choice2


def generate_image(prompt):
    client = OpenAI(
        base_url="https://api.studio.nebius.ai/v1/",
        api_key=ai_key_final
    )

    response = client.images.generate(
        model="black-forest-labs/flux-schnell",
        prompt=prompt,
        response_format="url",
        extra_body={
            "response_extension": "webp",
            "width": 512,
            "height": 512,
            "num_inference_steps": 16,
            "seed": -1,
            "negative_prompt": "Giraffes, night sky"
        }
    )
    
    url = response.data[0].url

    return url
