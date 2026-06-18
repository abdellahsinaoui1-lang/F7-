import discord
from discord.ext import commands
import ollama
import json
from groq import Groq as G


MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

def get_token():
    with open("data.json", "r") as file:
        token = json.load(file)["TOKEN"]
        return str(token)
    
def get_key():
    with open("data.json", "r") as file:
        key = json.load(file)["KEY"]
        return str(key)
    

disor = G(api_key=get_key())
    
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot("!", intents=intents)

AiAbout = """
You are a Discord bot named Disor 1.
- Talk in Arabic only, NEVER use any other language
- Max 35 words per message
- You help users manage their Discord server
"""


async def run_commands(commands: list, guild: discord.Guild):
    for command in commands:
        for key in command:
            if key.startswith("CreateChannel"):
                print(f"Running command: Creating channel")
                if command[key]["Type"] == "text":
                    await guild.create_text_channel(name=command[key]["Name"])

    


@bot.event
async def on_ready():
    print(f"Logged as: {bot.user}")

@bot.event
async def on_message(m: discord.Message):
    if m.author.id == bot.user.id:
        return
    
    if m.channel.id == 1515944280684892253:
        if bot.user.mention in m.content:
            
            final = m.content.replace(bot.user.mention, "")

            async with m.channel.typing():
                response = disor.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": f"Look at the user message and see if he wants to talk or want action\nAbout you: {AiAbout}\nDON'T chat with the user just take his message and return: 'USER_IS_MESSAGING' or 'USER_WANTS_ACTION' ONLY"},

                        {"role": "user", "content": "عامل اي يسطا"},
                        {"role": "assistant", "content": "USER_IS_MESSAGING"},

                        {"role": "user", "content": "ممكن تطرد الشخص ده من سيرفر"},
                        {"role": "assistant", "content": "USER_WANTS_ACTION"},

                        {"role": "user", "content": "الو"},
                        {"role": "assistant", "content": "USER_IS_MESSAGING"},

                        {"role": "user", "content": "اعملي روم سميه chat"},
                        {"role": "assistant", "content": "USER_WANTS_ACTION"},

                        {"role": "user", "content": "اهلا"},
                        {"role": "assistant", "content": "USER_IS_MESSAGING"},


                        {"role": "user", "content": final},
                    ]
                )

                print(response.choices[0].message.content)
                if response.choices[0].message.content.startswith("USER_IS_MESSAGING"):
                    chatbot = disor.chat.completions.create(
                        model=MODEL,
                        messages=[
                            {"role": "system", "content": f"تحدث إلى المستخدم وساعده أو قدم له أي مساعدة يطلبها...\nAbout you: {AiAbout}"},
                            {"role": "user", "content": final}
                        ]
                    )

                    await m.reply(chatbot.choices[0].message.content)

                elif response.choices[0].message.content.startswith("USER_WANTS_ACTION"):
                    actioner = disor.chat.completions.create(
                        model=MODEL,
                        messages=[
                            {"role": "system", "content": f"""You tell the user you will TRY to do the action, but you're not sure if it will succeed.
                            - Say things like 'let me try' or 'give me a sec' or 'on it'
                            - NEVER say 'done' or 'completed' because you don't know yet
                            - Keep it short, one sentence only
                            About you: {AiAbout}"""},

                            {"role": "user", "content": "اعملي روم اسمه chat"},
                            {"role": "assistant", "content": "لحظات هعمله"},

                            {"role": "user", "content": "اطرد هذا الشخص"},
                            {"role": "assistant", "content": "دعني اقوم بذلك"},

                            {"role": "user", "content": "احذف هذا الروم"},
                            {"role": "assistant", "content": "حسنا ثواني..."},

                            {"role": "user", "content": final}


                        ]
                    )

                    await m.reply(actioner.choices[0].message.content)

                    commands = []

                    parser = disor.chat.completions.create(
                        model=MODEL,
                        messages=[
                            {"role": "system", "content": f"Take the user input and reply with JSON only NEVER CHANGE THE JSON FORMAT: {{\"CreateChannel0\": {{\"Name\": \"...\", \"Type\": \"...\"}}, \"CreateChannel1\": {{\"Name\": \"...\", \"Type\": \"...\"}}}} \nAbout you: {AiAbout}"}, 
                            {"role": "user", "content": "اعملي روم سميه chat"},
                            {"role": "assistant", "content": "{\"CreateChannel0\": {\"Name\": \"chat\", \"Type\": \"text\"}}"},

                            {"role": "user", "content": "اعملي روم سميه chat و روم تاني اسمه welcome"},
                            {"role": "assistant", "content": "{\"CreateChannel0\": {\"Name\": \"chat\", \"Type\": \"text\"}, \"CreateChannel1\": {\"Name\": \"welcome\", \"Type\": \"text\"}}"},


                            {"role": "user", "content": final}
                        ]
                    )



                

                    raw = json.loads(parser.choices[0].message.content)
                    for key, value in raw.items():
                        commands.append({key: value})

                    print(parser.choices[0].message.content)

                    await run_commands(commands, m.guild)

            
        
bot.run(get_token())