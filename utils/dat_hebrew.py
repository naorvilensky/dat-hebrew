import os
from typing import Callable
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from huggingface_hub.constants import HF_HUB_CACHE
import os

from utils.constants import DAT_MODELS, DAT_MODELS_LITERAL
from utils.main_embedder import ManualEmbedder


class DatHebrew():

    input_path: str
    output_path: str
    used_models: list[DAT_MODELS_LITERAL]
    log_method: Callable[[str], None]

    def __init__(self, log_method: Callable[[str], None], used_model: DAT_MODELS_LITERAL = DAT_MODELS[0]):
        self.input_path = None
        self.output_path = None
        self.log_method = log_method
        self.used_model = used_model

    def set_used_model(self, used_model: DAT_MODELS_LITERAL):
        self.used_model = used_model

    def set_input_path(self, input_path: str):
        self.input_path = input_path

    def set_output_path(self, output_path: str):
        self.output_path = output_path

    def compute_dat_score(self, words, model):
        embeddings = model.encode(words)
        cosine_scores = util.pytorch_cos_sim(embeddings, embeddings)

        total = 0
        count = 0
        for i in range(len(words)):
            for j in range(i + 1, len(words)):
                total += 1 - cosine_scores[i][j]
                count += 1

        return (total / count).item()

    def load_model_with_logging(self, model_name: str) -> SentenceTransformer:
        self.log_method(f"Checking local cache for model: {model_name}")
        self.log_method(f"Hugging Face cache location: {HF_HUB_CACHE}")

        # Construct expected cache path
        safe_repo = model_name.replace("/", "--")
        model_dir = os.path.join(HF_HUB_CACHE, f"models--{safe_repo}")

        if os.path.exists(model_dir):
            self.log_method("Model found in local cache.")
        else:
            self.log_method("Model not found in cache. Downloading...")

        # Load the model (will download if not cached)
        try:
            model = ManualEmbedder(model_name)
            self.log_method(f"Model '{model_name}' loaded successfully.")
            return model
        except Exception as e:
            self.log_method(f"Error loading model '{model_name}': {e}")
            raise e

    def computed_and_write_to_file(self, is_write: bool = True) -> pd.DataFrame:
        if self.input_path is None or (self.output_path is None and is_write is True):
            raise Exception(
                f"No input or output path selected: ({self.input_path}, {self.output_path})")

        model = self.load_model_with_logging(self.used_model)

        try:
            df = pd.read_excel(self.input_path)
        except FileNotFoundError:
            self.log_method("Error: The file does not exist.")
            return
        except pd.errors.EmptyDataError:
            self.log_method("Error: The file is empty.")
            return
        except pd.errors.ParserError:
            self.log_method("Error: The file could not be parsed.")
            return
        except Exception as e:
            self.log_method(f"An unexpected error occurred: {e}")
            return

        # Compute DAT score for each row
        scores = []
        for _, row in df.iterrows():
            words = row.tolist()
            score = self.compute_dat_score(words, model)
            self.log_method(f"computed score: ({score}, [{', '.join(words)}])")
            scores.append(score)

        # Add scores to DataFrame and save
        df['DAT_score'] = scores
        if is_write is True:
            df.to_excel(self.output_path, index=False)
            self.log_method(f"Updated file saved to {self.output_path}")
        else:
            self.log_method(f"Score were not saved")

        return df
