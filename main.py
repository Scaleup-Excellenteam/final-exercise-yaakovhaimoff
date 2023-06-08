import argparse
import asyncio
import json
import time

from OpenAIAPI import OpenAIAPI
from PresentationParser import PresentationParser


def print_to_file(explanations, presentation_path) -> None:
    """
    Print the explanations to a file.
    :param explanations: list of explanations from the openai api responses
    :param presentation_path: for the name of the output file
    :return: nothing
    """
    presentation_name = presentation_path.split("/")[-1].split(".")[0]
    output_file = f"{presentation_name}.json"
    output_data = {"explanations": explanations}

    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=4)


async def main():
    parser = argparse.ArgumentParser(description="Process PowerPoint presentation and generate explanations.")
    parser.add_argument("presentation_path", metavar="presentation_path", type=str,
                        help="path to the PowerPoint presentation")
    args = parser.parse_args()

    presentation_path = args.presentation_path

    print(f"Processing {presentation_path}")

    # Parse presentation
    presentation_parser = PresentationParser(presentation_path)
    slides = presentation_parser.process_presentation()

    # Generate explanations
    openai_api = OpenAIAPI(api_key="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")
    explanations = await openai_api.generate_explanations(slides)

    # Print explanations to file
    print_to_file(explanations, presentation_path)


if __name__ == "__main__":
    start_time = time.time()

    asyncio.run(main())

    end_time = time.time()
    execution_time = end_time - start_time
    minutes, seconds = divmod(execution_time, 60)
    print(f"Execution time: {minutes:.0f} minutes {seconds:.2f} seconds")
