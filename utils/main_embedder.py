import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np

class ManualEmbedder:
    def __init__(self, model_name: str, device: str = "cpu"):
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(device)
        self.model.eval()

    def encode(self, texts: list[str]) -> np.ndarray:
        with torch.no_grad():
            inputs = self.tokenizer(texts, return_tensors="pt", padding=True, truncation=True).to(self.device)
            outputs = self.model(**inputs)
            last_hidden_state = outputs.last_hidden_state  # shape: (batch, seq_len, hidden_size)

            # Mean pooling, ignoring padding tokens
            attention_mask = inputs['attention_mask'].unsqueeze(-1).expand(last_hidden_state.size())
            masked_embeddings = last_hidden_state * attention_mask
            summed = masked_embeddings.sum(dim=1)
            counts = attention_mask.sum(dim=1)
            mean_pooled = summed / counts  # shape: (batch, hidden_size)

            return mean_pooled.cpu().numpy()
