import os
import base64
from dotenv import load_dotenv
from openai import AzureOpenAI


def main():

    os.system('cls' if os.name == 'nt' else 'clear')

    try:

        load_dotenv()

        endpoint = os.getenv("ENDPOINT")
        api_key = os.getenv("API_KEY")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")
        api_version = os.getenv("API_VERSION")

        print("Endpoint:", endpoint)
        print("Model Deployment:", model_deployment)
        print("API Version:", api_version)
        print("API Key Loaded:", api_key is not None)

        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint
        )

        img_no = 0

        while True:

            prompt = input("Enter the prompt (or type 'quit' to exit): ")

            if prompt.lower() == "quit":
                break

            if prompt.strip() == "":
                print("Please enter a prompt.")
                continue

            result = client.images.generate(
                model=model_deployment,
                prompt=prompt,
                size="1024x1024"
            )

            # FLUX returns base64 image
            image_base64 = result.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)

            img_no += 1
            filename = f"image_{img_no}.png"

            save_image(image_bytes, filename)

    except Exception as ex:
        print("Error:", ex)


def save_image(image_bytes, filename):

    image_dir = os.path.join(os.getcwd(), "images")

    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    image_path = os.path.join(image_dir, filename)

    with open(image_path, "wb") as f:
        f.write(image_bytes)

    print(f"Image saved as {image_path}")


if __name__ == "__main__":
    main()