from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext, Tool
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the variables from the environment
model_name = os.getenv('MODEL_NAME')
base_url = os.getenv('BASE_URL')
api_key = os.getenv('API_KEY')

# Create an instance of OpenAIModel using the loaded variables
model = OpenAIModel(
    model_name,
    provider=OpenAIProvider(base_url=base_url, api_key=api_key),
)

agent = Agent(
    model=model,
    result_retries = 3,
    system_prompt = "You are smart agent with analysis skills, you will analysis any file and extract as much info as possible",
)

@agent.tool_plain
def list_all_files(input_dir: str) -> list[str]:
    """
    List all files in the input directory

    Args:
        input_dir (str): The directory to list files from

    Returns:
        (list[str]): A list of all file paths in the input directory
    """
    print(f"Call list files with dir:{input_dir}")
    return [str(path) for path in Path(input_dir).glob("**/*")]


@agent.tool_plain
def list_files_matching_pattern(input_dir: str, pattern: str) -> list[str]:
    """
    List all files matching a specific pattern in the given directory.

    Args:
        directory (str): The directory to search for files.
        pattern (str): The pattern to match file names against.

    Returns:
        list[str]: A list of paths to files that match the specified pattern within the directory.
    """
    print(f"Call list files with pattern, dir:{input_dir}, pattern:{pattern}")
    return [str(path) for path in Path(input_dir).glob(pattern)]


@agent.tool_plain
def get_file_contents_as_str(file_path: str) -> str:
    """
    Read the contents of a file as a string

    Args:
        file_path (str): The path to the file to read
    Returns:
        (str): The contents of the file as a string
    """
    print(f"get files content called for file {file_path}")
    return Path(file_path).read_bytes().decode("utf-8")





response = agent.run_sync("Analysis all files ends with 'bin' extention in directory './10_sample_data' and tell me what is those files")
print(response.output)


response = agent.run_sync("Do you find andy common data between all files in './10_sample_data'")
print(response.output)

