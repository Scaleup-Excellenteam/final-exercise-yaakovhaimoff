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



# import asyncio
# import json
# import os
#
# from OpenAIAPI import OpenAIAPI
# from PresentationParser import PresentationParser
#
#
# async def process_file(presentation_path):
#     print(f"Processing file {presentation_path}")
#
#     # Parse presentation
#     presentation_parser = PresentationParser(presentation_path)
#     slides = presentation_parser.process_presentation()
#
#     # Generate explanations
#     openai_api = OpenAIAPI(api_key="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")
#     explanations = await openai_api.generate_explanations(slides)
#     print("here3")
#
#     # Save explanations to file
#     save_to_file(explanations, presentation_path)
#     print("here4")
#
#
# def save_to_file(explanations, presentation_path) -> None:
#     presentation_name = os.path.splitext(os.path.basename(presentation_path))[0]
#     output_file = f"outputs/{presentation_name}.json"
#     output_data = {"explanations": explanations}
#
#     with open(output_file, "w") as f:
#         json.dump(output_data, f, indent=4)
#
#
# async def main():
#     # Get the parent directory of the current script file
#     parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     output_folder = os.path.join(parent_dir, 'outputs')
#     input_folder = "uploads"
#
#     os.makedirs(output_folder, exist_ok=True)
#
#     print(f"Explainer system started. Monitoring folder: {input_folder}")
#
#     while True:
#         files = os.listdir(input_folder)
#         for file in files:
#             file_path = os.path.join(input_folder, file)
#             if os.path.isfile(file_path):
#                 try:
#                     await process_file(file_path)
#                 except Exception as e:
#                     print(f"Error processing file {file_path}: {e}")
#
#         print("Sleeping for 10 seconds...")
#         await asyncio.sleep(10)
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
