from typing import List
import numpy as np
from collections import Counter
import re


class SimpleEncoder:
    def __init__(self, max_features: int = 100):
        self.max_features = max_features
        self.vocabulary: dict[str, int] = {}
        self._fitted = False

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r'\b\w+\b', text)
        return tokens

    def _build_vocabulary(self, texts: List[str]) -> None:
        all_tokens = []
        for text in texts:
            all_tokens.extend(self._tokenize(text))

        counter = Counter(all_tokens)
        most_common = counter.most_common(self.max_features)
        self.vocabulary = {word: idx for idx, (word, _) in enumerate(most_common)}
        self._fitted = True

    def encode(self, texts: List[str]) -> np.ndarray:
        if not self._fitted:
            self._build_vocabulary(texts)

        embeddings = np.zeros((len(texts), len(self.vocabulary)))

        for i, text in enumerate(texts):
            tokens = self._tokenize(text)
            for token in tokens:
                if token in self.vocabulary:
                    embeddings[i, self.vocabulary[token]] += 1

        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1, norms)
        embeddings = embeddings / norms

        return embeddings

    def get_dimension(self) -> int:
        return len(self.vocabulary)
