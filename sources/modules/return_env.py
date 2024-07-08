#classe para retornar as informações do .env
from dotenv import dotenv_values
import os
class return_envData():

    def return_data(self, bank: str) -> dict:
        # env_values = dotenv_values(f"../{bank.lower()}/data/.env")
        env_path = os.path.abspath(f'../crefisa/data/.env')
        env_values = dotenv_values(env_path)
        return env_values