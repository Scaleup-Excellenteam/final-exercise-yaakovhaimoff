import asyncio
import json
import os
import time

from OpenAIAPI import OpenAIAPI
from PresentationParser import PresentationParser


# Get the parent directory of the current script file
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_folder = os.path.join(parent_dir, 'outputs')
input_folder = os.path.join(parent_dir, 'uploads')


async def process_file(presentation_path):
    print(f"Started processing file {presentation_path}")

    # Parse presentation
    presentation_parser = PresentationParser(presentation_path)
    slides = presentation_parser.process_presentation()

    # Generate explanations
    openai_api = OpenAIAPI(api_key="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")
    explanations = await openai_api.generate_explanations(slides)

    # Save explanations to file
    save_to_file(explanations, presentation_path)
    print(f"Finished processing file {presentation_path}")


def save_to_file(explanations, presentation_path) -> None:
    presentation_name = os.path.splitext(os.path.basename(presentation_path))[0]
    output_file = os.path.join(output_folder, f"{presentation_name}.json")
    output_data = {"explanations": explanations}
    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=4)


async def main():

    os.makedirs(output_folder, exist_ok=True)

    print(f"Explainer system started. Monitoring folder: {input_folder}")

    last_checked = 0

    while True:
        files = os.listdir(input_folder)
        for file in files:
            file_path = os.path.join(input_folder, file)
            if os.path.isfile(file_path):
                try:
                    timestamp = int(file.split("_")[1])  # Extract timestamp from the file name

                    if last_checked < timestamp:
                        await process_file(file_path)

                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")
        last_checked = int(time.time())
        print("Sleeping for 10 seconds...")
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
