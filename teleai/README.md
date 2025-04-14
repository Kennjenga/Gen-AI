# Telegram BOT

A Telegram bot powered by AI.

## Features

- Responds to user queries using AI.
- Utilizes the aiogram library for seamless interaction with the Telegram API.
- Environment variables managed using python-dotenv.
- Integrates with Google Generative AI for advanced responses.

## Requirements

- Python 3.8 or higher
- `python-dotenv`
- `aiogram>=3.0.0`
- `google-generativeai`

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/teleai.git
   cd teleai
   ```

2. Create a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```sh
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your environment variables:
   ```env
   TELEGRAM_TOKEN=your_telegram_token
   GOOGLE_API_KEY=your_google_api_key
   ```

## Usage

1. Activate the virtual environment if not already activated:

   ```sh
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. Run the bot:
   ```sh
   python main.py
   ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact [your email].
