from sentence_transformers import SentenceTransformer, util
import pandas as pd

def main():

    model = SentenceTransformer('distiluse-base-multilingual-cased-v2')

    try:
        df = pd.read_csv("random_word_sets.csv", encoding="utf-8")
    except FileNotFoundError:
        print("Error: The file does not exist.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except pd.errors.ParserError:
        print("Error: The file could not be parsed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    word_sets = df.values.tolist()

    for words in word_sets:
        embeddings = model.encode(words, convert_to_tensor=True)
        cosine_scores = util.pytorch_cos_sim(embeddings, embeddings)

        total = 0
        count = 0
        for i in range(len(words)):
            for j in range(i+1, len(words)):
                total += 1 - cosine_scores[i][j] 
                count += 1

        divergent_score = total / count
        print(f"Divergent Association Score: {divergent_score:.3f}")

    return 0


if __name__ == '__main__':
    main()