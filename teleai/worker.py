from fastapi import FastAPI
import asyncio
import uvicorn
from main import bot, dp

app = FastAPI()
bot_task = None  # Store the background task globally


@app.get("/health")
async def health():
    global bot_task
    # Restart the bot if the task is done or doesn't exist
    if bot_task is None or bot_task.done():
        bot_task = asyncio.create_task(dp.start_polling(bot))
        print("Bot restarted during health check")
    return {"status": "ok", "bot_running": not (bot_task.done() if bot_task else True)}


@app.on_event("startup")
async def startup_event():
    """Start the bot when the FastAPI app starts up"""
    global bot_task
    print("Starting Telegram bot...")
    # Create a background task for the bot and store the reference
    bot_task = asyncio.create_task(dp.start_polling(bot))


@app.on_event("shutdown")
async def shutdown_event():
    """Stop the bot when the FastAPI app shuts down"""
    global bot_task
    if bot_task and not bot_task.done():
        print("Shutting down bot...")
        bot_task.cancel()
        try:
            await bot_task
        except asyncio.CancelledError:
            print("Bot task cancelled successfully")

if __name__ == "__main__":
    uvicorn.run("worker:app", host="0.0.0.0", port=8000)
