from typing import List
import random

from transformations.replace_financial_amounts import token
from interfaces.SentenceOperation import SentenceOperation
from tasks.TaskTypes import TaskType


class ReplaceFinancialAmount(SentenceOperation):
    tasks = [
        TaskType.TEXT_CLASSIFICATION,
        TaskType.TEXT_TO_TEXT_GENERATION,
        TaskType.TEXT_TAGGING,
    ]
    languages = ["en"]

    def __init__(self, seed: int = 0, max_outputs: int = 1) -> None:
        super().__init__(seed=seed, max_outputs=max_outputs)
        self.financial_amount_transformation = (
            token.FinancialAmountTransformation(seed, max_outputs)
        )

    def generate(self, sentence: str) -> List[str]:
        # we seed the random generator to keep coherent and consistent transformation throughout a text.
        random.seed(self.seed)

        percentage_financial_amount_variation = random.choice(
            [-1, 1]
        ) * random.randint(1, 20)
        financial_amounts_encountered = {}

        token_list = token.create_tokens(sentence)

        for _token in token_list:
            if _token.is_financial_amount:
                (
                    replacement,
                    financial_amounts_encountered,
                ) = token.generate_financial_amount_replacement(
                    _token,
                    financial_amounts_encountered,
                    percentage_financial_amount_variation,
                )
                _token.replace(replacement)

        result = "".join(_token.string for _token in token_list)

        if self.verbose:
            print(f"Perturbed Input from {sentence} : {result}")

        return [result]
