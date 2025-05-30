from typing import Literal

# List of model names
DAT_MODELS = [
    "distiluse-base-multilingual-cased-v2",
    "paraphrase-multilingual-MiniLM-L12-v2",
    "paraphrase-multilingual-mpnet-base-v2",
    "xlm-r-100langs-bert-base-nli-stsb-mean-tokens",
    "sentence-transformers/LaBSE",
    "onlplab/alephbert-base",
    "avichr/heBERT",
    "avichr/bert-base-hebrew-uncased",
    "csebuetnlp/multilingual-sentence-bert",
    "intfloat/multilingual-e5-base",
    "intfloat/multilingual-e5-small",
]

# Literal type for type hints
DAT_MODELS_LITERAL = Literal[
    "distiluse-base-multilingual-cased-v2",
    "paraphrase-multilingual-MiniLM-L12-v2",
    "paraphrase-multilingual-mpnet-base-v2",
    "xlm-r-100langs-bert-base-nli-stsb-mean-tokens",
    "sentence-transformers/LaBSE",
    "onlplab/alephbert-base",
    "avichr/heBERT",
    "avichr/bert-base-hebrew-uncased",
    "csebuetnlp/multilingual-sentence-bert",
    "intfloat/multilingual-e5-base",
    "intfloat/multilingual-e5-small",
]
