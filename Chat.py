import speech_recognition as sr
import pyttsx3
import openai
import Events

openai.api_key = ""

engine = pyttsx3.init() 
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

conversation = "" # Var not working yet
user_name = "Marijan"
bot_name = "Pixel"

while True:
    with mic as source:
        print("\n Listening...")
        r.adjust_for_ambient_noise(source, duration=0.2)
        audio = r.listen(source)
    print("no longer listening")

    try:
        user_input = r.recognize_google(audio)
    except:
        continue

    if "Remind me" in user_input:
        Events.event_text = user_input.replace("Remind me to, ", "")
        Events.eventsevent_text = Events.event_text.replace(" to ", " | ")
        Events.event_text = Events.event_text.replace(" at ", " o'clock | ")
        Events.events[len(Events.events)+1] = Events.event_text
        response_str = "Okay, ich habe das Ereignis gespeichert."

    if "What events do i have" in user_input:
        print_events()
        response_str = "Hier sind deine gespeicherten Ereignisse."
    

    prompt = user_name+":"+user_input + "\n"+bot_name+":"
    conversation += prompt

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=conversation,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    def print_events():
        print("Gespeicherte Ereignisse:")
        for event_num, event_text in Events.events.items():
            print(f"{event_num}: {event_text}")



    response_str = response["choices"][0]["text"].replace("\n", "")
    response_str =response_str.split(
        user_name + ":" ,1)[0].split(bot_name+ ":",1)[0]

    conversation+= response_str +"\n"
    print(response_str)

    engine.say(response_str)
    engine.runAndWait()