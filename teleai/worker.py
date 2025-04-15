from fastapi import FastAPI
import asyncio
from main import bot, dp

app = FastAPI()


@app.get("/health")
async def health():
    return {"status": "ok"}


async def main():
    print("Starting Telegram bot...")
    asyncio.create_task(dp.start_polling(bot))

if __name__ == "__main__":
    import uvicorn
    asyncio.run(main())
    uvicorn.run(app, host="0.0.0.0", port=8000)
