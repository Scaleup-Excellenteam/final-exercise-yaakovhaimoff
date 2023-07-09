import asyncio
import backoff
import openai


class OpenAIAPI:
    '''
    OpenAIAPI class that uses the OpenAI API to generate explanations.
    '''

    def __init__(self, api_key):
        '''
        Constructor for OpenAIAPI class.
        :param api_key: OpenAI API key
        '''
        openai.api_key = api_key
        self.messages = [
            {"role": "system", "content": "Please summarize the slides and provide additional information."}
        ]

    @backoff.on_exception(backoff.expo, openai.error.RateLimitError)
    async def generate_explanations(self, slides) -> list[str]:
        """
        Generates explanations for the given slides. Uses the OpenAI API to generate explanations.
        :param slides: list of slides
        :return: list of explanations
        """
        explanations = []
        tasks = []
        for slide in slides:
            tasks.append(asyncio.create_task(self.get_response(slide, explanations)))
        await asyncio.gather(*tasks)
        return explanations

    @backoff.on_exception(backoff.expo, openai.error.RateLimitError)
    async def get_response(self, slide, explanations) -> None:
        """
        Send a request to the OpenAI Chat API to get a response for the given slide.
        :param slide: Slide object from the PowerPoint presentation.
        :param explanations: list of explanations
        :return: none
        """
        self.messages.append({"role": "user", "content": slide})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            timeout=60,
        )
        explanations.append(response.choices[0].message.content)
