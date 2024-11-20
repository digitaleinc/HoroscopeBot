import traceback
from datetime import datetime
from typing import Optional

import openai

from tgtarologistbot.src.core import logger, Config


class OpenAIService:
    def __init__(self):
        self.prompt_horoscope = """"""

        self.prompt_taro = """"""

        self.config = Config()
        self.api_key = self.config.open_ai_api_key
        openai.api_key = self.api_key

    async def _send_request(self, user_content: str) -> Optional[str]:
        """
        Отправляет запрос к OpenAI API

        :return: Ответ от OpenAI
        """
        try:
            response = await openai.chat.completions.create(
                model=self.config.open_ai_model,
                messages=[
                    {"role": "system", "content": "Ты ассистент, помогающий с обработкой запросов."},
                    {"role": "user", "content": self.prompt_horoscope}
                ],
                max_tokens=int(self.config.open_ai_max_tokens),
                temperature=int(self.config.open_ai_temperature)
            )

            return response["choices"][0]["message"]["content"]

        except openai.OpenAIError as e:
            logger.error(f"Произошла ошибка во время запроса к ИИ:\n{traceback.print_exception(e)}")
            return None

    async def send_request_horoscope(self, date_of_birth: datetime) -> Optional[str]:
        """
        Отправляет запрос к OpenAI API, добавляя дату рождения в prompt, который рассчитан на гороскоп

        :param date_of_birth: Дата рождения как объект datetime
        :return: Ответ от OpenAI
        """
        formatted_date = date_of_birth.strftime("%Y-%m-%d")

        self.prompt_horoscope += f"Дата рождения: {formatted_date}\n"

        return await self._send_request(formatted_date)

    async def send_request_taro(self) -> Optional[str]:
        """
        Отправляет запрос к OpenAI API, добавляя дату рождения в prompt, который рассчитан на таро

        :return: Ответ от OpenAI
        """

        return await self._send_request(self.prompt_taro)
