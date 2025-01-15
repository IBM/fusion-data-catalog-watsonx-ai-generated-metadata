import base64
from ibm_watsonx_ai.foundation_models import ModelInference
import wget
from dotenv import load_dotenv
import getpass
from ibm_watsonx_ai import Credentials
import os
from ibm_watsonx_ai.foundation_models.schema import TextChatParameters
from PIL import Image


def describe_image(filepath: str):
    """Take an image filepath and get some tags which describe it from watsonx.ai"""
    load_dotenv()
    credentials = Credentials(
        url=os.environ["WX_BASE_URL"],
        api_key=os.environ["IBM_API_KEY"],
    )
    # Load the watsonx project ID from the environment
    project_id = os.environ["PROJECT_ID"]

    # Convert PNG images to JPG
    if (filepath.find(".png") > -1):
        im = Image.open(filepath)
        rgb_im = im.convert('RGB')

        new_filepath = filepath.replace(".png", ".jpg")
        rgb_im.save(new_filepath)
        filepath = new_filepath

    # Use the pixtral-12b multi-modal image on watsonx.ai
    model_id = "mistralai/pixtral-12b"

    params = TextChatParameters(
        temperature=1,
        max_tokens=100,
    )

    model = ModelInference(
        model_id=model_id,
        credentials=credentials,
        project_id=project_id,
        params=params
    )

    # Convert the imagefile to base64
    with open(filepath, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    # Prompt for watsonx.ai to generate keywords
    question = "Generate a list of maximum 10 keywords which describe the image separated by commas"

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": question
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/jpeg;base64," + encoded_string,
                    }
                }
            ]
        }
    ]

    # Load the response and return the tags
    response = model.chat(messages=messages)
    return response["choices"][0]["message"]["content"].replace("\n", "")


if __name__ == "__main__":
    print(describe_image("test_images/train.png"))
