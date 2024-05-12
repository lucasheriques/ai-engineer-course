import os

import requests
from cairosvg import svg2png
from openai import OpenAI

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def svg_to_png_bytes(svg_string):
    # Convert SVG string to PNG bytes
    png_bytes = svg2png(bytestring=svg_string.encode("utf-8"))
    return png_bytes


def python_math_execution(math_string):
    try:
        answer = eval(math_string)
        if answer:
            return str(answer)
    except:
        return "invalid code generated"


def generate_image(prompt: str):
    response = openai.images.generate(
        prompt=prompt, model="dall-e-3", n=1, size="1024x1024"
    )
    image_url = response.data[0].url
    image_response = requests.get(image_url)
    # print debug image_response
    return image_response.content


def run_function(name: str, args: dict):
    if name == "svg_to_png_bytes":
        return svg_to_png_bytes(args["svg_string"])
    elif name == "python_math_execution":
        return python_math_execution(args["math_string"])
    elif name == "generate_image":
        return generate_image(args["prompt"])
    else:
        return None


functions = [
    {
        "type": "function",
        "function": {
            "name": "svg_to_png_bytes",
            "description": "Generate a PNG from an SVG",
            "parameters": {
                "type": "object",
                "properties": {
                    "svg_string": {
                        "type": "string",
                        "description": "A fully formed SVG element in the form of a string",
                    },
                },
                "required": ["svg_string"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "python_math_execution",
            "description": "Solve a math problem using python code",
            "parameters": {
                "type": "object",
                "properties": {
                    "math_string": {
                        "type": "string",
                        "description": "A string that solves a math problem that conforms with python syntax that could be passed directly to an eval() function",
                    },
                },
                "required": ["math_string"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_image",
            "description": "Generate an image from a prompt",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "A prompt to generate an image from",
                    },
                },
                "required": ["prompt"],
            },
        },
    },
]
