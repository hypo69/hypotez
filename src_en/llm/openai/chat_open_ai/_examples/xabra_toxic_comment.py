# https://aistudio.google.com/app/prompts?state=%7B%22ids%22:%5B%221-sltpLDS5IBaM7nitu6wqwh3QDGI4-s2%22%5D,%22action%22:%22open%22,%22userId%22:%22110086287199111465514%22,%22resourceKeys%22:%7B%7D%7D&usp=sharing

from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
load_dotenv()
import header
from src import gs
from src.logger.logger import logger

# None

ENDPOINT = 'openai'
USE_ENV:bool = False # <- it determines where to get the keys from. If false - then from a database with passwords, otherwise from .env
MODE:str = 'PRODUCTION' # <- defines the sales regime.
MODE:str = 'DEV' # <- defines the developer regime.
# None

async def habra_toxic_commenter(author_username: str, model_name: str = "gpt-4o-mini", api_key:str = None):
    """Looking for an article on Habre according to the indicated author, opens it and generates a toxic comment.

    Args:
        Author_USERNAME: The name of the user on Habr.
        Model_name: the name of the Openai language model for use.  By default GPT-4O.

    Returns:
        A line with the result of the agent, containing the name of the article and the generated comment.
        Returns None if an error has occurred."""
    
    try:
        llm = ChatOpenAI(model = model_name,
                         api_key = api_key if api_key else gs.credentials.openai.hypotez.api_key,
                         )
        task = f"""Open the Habr.com, find some article from the user {author_username}
        Open its full version, and offer an option of toxic commentary in Russian,
        related to this article, after publish this commentary on the article."""
        agent = Agent(
            task=task,
            llm=llm,
            
        )
        logger.info(f"Агент начал работу по поиску статьи автора {author_username}")
        result = await agent.run()
        logger.info(f"Агент завершил работу.")
        return result
    except Exception as ex:
        logger.error(f"Произошла ошибка: ",ex)
        return None


async def main():
    """An example of using the Habra_toxic_commenter function."""
    api_key:str = gs.credentials.openai.hypotez.api_key
    model_name:str  = 'gpt-4o-mini'
    author = "ElKornacio"  # Replace in the name of the user whose articles you want to find
    result = await habra_toxic_commenter(author_username = author, model_name = model_name, api_key = api_key)

    if result:
        print("Результат работы агента:")
        print(result)
    else:
        print("Не удалось получить результат.")


if __name__ == "__main__":
    asyncio.run(main())