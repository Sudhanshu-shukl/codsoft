import re
import random
from fuzzywuzzy import fuzz
responses = {
    'hello': ["Hello! How can I help you?", "Hi there!", "Greetings! How can I assist?"],
    'how_are_you': ["I'm doing well, thank you! How about you?", "I'm good! How are you?", "I'm great, thanks for asking!"],
    'name': ["I'm your friendly chatbot! What's your name?", "I go by Chatbot. And you are?", "Chatbot at your service. What’s your name?"],
    'goodbye': ["Goodbye! Take care.", "See you later!", "Bye! Have a great day!"],
    'joke': ["Why don't scientists trust atoms? Because they make up everything!", "I told my computer I needed a break, and now it won’t stop sending me Kit-Kats.", "Why was the math book sad? It had too many problems!"]
}
user_name = None
def fuzzy_match(query, options):
    for option in options:
        if fuzz.ratio(query, option) > 70:  
            return option
    return None
def chatbot_response(user_input):
    global user_name
    if not user_name:
        name_pattern = r'\bmy name is (\w+)\b'
        match = re.search(name_pattern, user_input)
        if match:
            user_name = match.group(1)
            return f"Nice to meet you, {user_name}!"
    if user_name:
        user_input = user_input.replace(user_name.lower(), "")
    
    if fuzzy_match(user_input, ['hello', 'hi', 'hey']):
        return random.choice(responses['hello'])
    elif fuzzy_match(user_input, ['how are you', 'how is it going']):
        return random.choice(responses['how_are_you'])
    elif fuzzy_match(user_input, ['your name', 'who are you']):
        return random.choice(responses['name'])
    elif fuzzy_match(user_input, ['bye', 'goodbye', 'see you']):
        return random.choice(responses['goodbye'])
    elif fuzzy_match(user_input, ['tell me a joke', 'joke', 'make me laugh']):
        return random.choice(responses['joke'])
    else:
        return "I'm sorry, I didn't quite catch that. Could you try rephrasing?"
print("Chatbot: Hello! Type 'bye' to exit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'bye':
        print("Chatbot: Goodbye!")
        break
    response = chatbot_response(user_input)
    print("Chatbot:", response)
