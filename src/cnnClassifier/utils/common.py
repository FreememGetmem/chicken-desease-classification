import os 
from box.exceptions import BoxValueError
import yaml
from cnnClassifier import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Read a YAML file and return a ConfigBox object.

        Args: 
            path_to_yaml (str): Path like input
        Raises:
            ValueError: If the file does not exist or is not a YAML file.
            e: If the file is not a valid YAML file.

        Returns:
            ConfigBox: The ConfigBox object.
    """
    try: 
        with open(path_to_yaml, "r") as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} load successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories

    Args:
        path_to_directories (list): list of path of directories
        ignore_log (bool, optional): ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """Save a JSON data

    Args:
        path (Path): Path to json file.
        data (dict): JSON data.
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file saved at : {path} successfully")

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """Load a JSON data

    Args:
        path (Path): Path to json file.

    Returns:
        ConfigBox: data as class attributes instead of dict.
    """
    with open(path, "r") as f:
        content = json.load(f)
    
    logger.info(f"json file loaded from : {path} successfully")
    return ConfigBox(content)

@ensure_annotations
def save_bin(data: Any, path: Path):
    """Save a binary file

    Args:
        data (Any): Data to save.
        path (Path): Path to binary file.
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at : {path} successfully")

@ensure_annotations
def load_bin(path: Path) -> Any:
    """Load a binary file

    Args:
        path (Path): Path to binary file.
        
    Returns:
        Any: data as class attributes instead of dict.
    """
    data = joblib.load(path)
    logger.info(f"binary file loaded from : {path} successfully")
    return data

@ensure_annotations
def get_size(path: Path)-> str:
    """Get the size of a file

    Args:
        path (Path): Path to file.
        
    Returns:
        str: Size of the file.
    """
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"{size_in_kb:.2f} KB"

def decodeImage(imgstring, filename):
    """Decode an image from a base64 string"""
    imgdata = base64.b64decode(imgstring)
    with open(filename, 'wb') as f:
        f.write(imgdata)
        f.close()

def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, 'rb') as f:
        return base64.b64encode(f.read())
    
