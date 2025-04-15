from fastapi import FastAPI
import asyncio
import uvicorn
from main import bot, dp

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.on_event("startup")
async def startup_event():
    """Start the bot when the FastAPI app starts up"""
    print("Starting Telegram bot...")
    # Create a background task for the bot
    asyncio.create_task(dp.start_polling(bot))


if __name__ == "__main__":
    uvicorn.run("worker:app", host="0.0.0.0", port=8000)
