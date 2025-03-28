from django.test import TestCase
# from .choices import *
import openai
from openai import OpenAI
import  choices



def get_headline_examples(selected_style):
    examples = {'forward reference': ['Kinas Økonomiske Fremtid: Usikkerheten som Følger Etter Gullalderen', 'Denne appen endrer måten nordmenn handler mat på', 'Se prisforskjellen som overrasker mellom EX90 og XC90'],
                'metaphor': ['Kinas Økonomiske Skute i Uvær: Rentekutt som Redningsflåte', 'Frifor: Navigatoren i Ultrabehandlet Matens Labyrint', 'Fra Dinosaur til Lyn: Volvos Elektriske Revolusjon Ruller Inn'],
                'question': ['Kan Volvos EX90 virkelig spare deg for 293.000 kroner?', 'Er Kinas økonomiske gullalder over for godt?', 'Kan En App Revolusjonere Måten Vi Velger Mat På?']
                }
    
    return examples [selected_style]

def generate_headlines(headline_style, article_text):
    prompt = ""
    examples= ""
    
    examples = get_headline_examples(headline_style)
    print("Style manipulation = ", headline_style )
    
    style_prompt = f"""Create a headline for the provided article that is designed to maximize engagement and click-through rates. The user has expressed a preference for the headlines: {examples} which use the style: {headline_style}. Try to mimic the writing styles of these headlines to appeal to the user in the best possible way. Ensure that your headline captures the essence of the article while also applying a similar writing styles as the provided examples. Keep the headline to a maximum of 10 words. Article: {article_text}"""
    prompt = style_prompt
    
    try:
        # Adjusted temperature and top_p values as per the "Creative Writing" settings
        completion = openai.chat.completions.create(
            model="gpt-4-0125-preview",
            temperature=0.7,  # Adjust to requirements. Controls 'creativity'
            top_p=0.8,  # Adjust to requirements 'Controls sampling'
            messages=[
                {"role": "system", "content": "You are an AI skilled in generating headlines using different jornalistic headline styles. Your goal is to create engaging headlines in Norwegian language, adhering to specific guidelines designed to enhance curiosity and emotional engagement."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the generated headline from the response
        generated_headline = completion.choices[0].message if completion.choices else "No headline generated."
        new_headline = generated_headline.content
        cleaned_headline = new_headline.strip('"')

        return cleaned_headline
    except Exception as e:
        print(f"Error generating headline: {e}")
        # return original_title  # Use original text as a fallback in case of an error
    
   
# -------------------------- main --------------------------

styles = ['metaphor', 'forward reference', 'question']  
for x in range(3):
    print("x=", x)
    print(choices.preQ_articles[x][0])
    for s in range(3):
        title = generate_headlines(styles[s], choices.preQ_articles[x][1])
        print (title)
        
# title = generate_headlines("metaphor", choices.preQ_articles[1][1])
# print (title)















