from dotenv import load_dotenv
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import google.generativeai as genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


class Reference:
    '''
    A class to store previous response from the Gemini API
    '''

    def __init__(self) -> None:
        self.response = ""


reference = Reference()

# Configure the Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Use the specific model format
model = genai.GenerativeModel("gemini-1.5-pro")

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


def clear_past():
    """A function to clear the previous conversation and context.
    """
    reference.response = ""


def get_help_message():
    """Returns the help message with available commands"""
    return """Hi There! Available commands:
/start - Start a new conversation
/clear - Clear past conversation
/help - Show this menu again"""


@dp.message(Command("clear"))
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")


@dp.message(Command("start"))
async def welcome(message: types.Message):
    """
    This handler receives messages with `/start` command
    """
    welcome_text = "Hi! I am Tele Bot created by Engadev. How can I assist you today?"
    await message.reply(welcome_text)
    # Send the help message with commands immediately after welcome
    await message.answer(get_help_message())


@dp.message(Command("help"))
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    await message.reply(get_help_message())


@dp.message()
async def gemini_chat(message: types.Message):
    """
    A handler to process the user's input and generate a response using the Gemini API.
    """
    print(f">>> USER: \n\t{message.text}")

    try:
        # Create a chat session if there's a previous response, otherwise start fresh
        if reference.response:
            chat = model.start_chat(history=[
                {"role": "model", "parts": [reference.response]},
                {"role": "user", "parts": [message.text]}
            ])
            response = chat.send_message(message.text)
        else:
            response = model.generate_content(message.text)

        # Save the response
        reference.response = response.text

        print(f">>> Gemini: \n\t{reference.response}")

        # Check if response is too long for Telegram (max ~4096 chars)
        if len(response.text) > 4000:
            # Split the response into chunks of 4000 characters
            chunks = [response.text[i:i+4000]
                      for i in range(0, len(response.text), 4000)]
            for i, chunk in enumerate(chunks):
                if i == 0:
                    await message.reply(chunk)
                else:
                    await message.answer(f"(Continued {i+1}/{len(chunks)})\n{chunk}")
        else:
            await message.reply(response.text)

    except Exception as e:
        # Truncate long error messages
        error_message = f"Error: {str(e)[:100]}..."
        print(f"Full error: {str(e)}")
        await message.reply("Sorry, I encountered an error. Try the /help command.")


async def main():
    print("Starting Telegram bot...")
    # Start the bot
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
