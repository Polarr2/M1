from bot import M1
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    bot = M1()
    bot.run(os.getenv("TOKEN"))