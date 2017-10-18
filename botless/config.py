try:
    import dotenv
except ImportError:
    pass  # Using .venv file is optional, if not available environment vars can be used
else:
    # Load environment variables from .env file for local development or usage
    dotenv.load_dotenv(dotenv.find_dotenv())
