from transformations.replace_financial_amounts import entity_financial_amount
from typing import List, Dict, Tuple
import spacy
import ftfy


class Token:
    """
    | A token is the smallest irreducible part of a sentence
    | It can be a word, a punctuation mark, a suite of numeric characters.
    """

    def __init__(self, token: str or Dict, is_str: bool = False):
        """
        if is_str is False, the token is a dictionary creates from parsing a string using Spacy NLP library.
        """
        self.is_financial_amount = False
        if is_str:
            self.string = token
        else:
            self.string = token.text_with_ws
        if self.value().replace(".", "").replace(",", "").isdigit():
            self.category = "numeric"
        else:
            self.category = "other"

    def value(self):
        return self.string.strip()

    def replace(self, replacement: str):
        """
        Replaces the token by another string
        """
        if self.string.endswith(" "):
            self.string = replacement.strip(" ") + " "
        else:
            self.string = replacement.strip(" ")

    def __str__(self):
        return f"({self.category}) {self.string}"


class FinancialAmountTransformation:
    def __init__(self, seed=0, max_outputs=1):
        self.max_outputs = max_outputs
        self.seed = seed


def create_tokens(text: str) -> List[Token]:
    """
    Analyse the text and return the list of tokens corresponding to the text.
    """
    text = ftfy.fix_text(text)
    nlp = spacy.load("en_core_web_sm")
    text = nlp(text)
    token_list = [Token(element) for _, element in enumerate(text)]
    return find_financial_amounts(token_list)


def find_financial_amounts(token_list: List[Token]) -> List[Token]:
    """
    Determine the type of each tokens in a list of tokens.
    """
    counter = 0

    while counter < len(token_list):
        _token_value = token_list[counter].string.strip()

        # Verify that the token value corresponds to a currency abbreviation
        if (
            _token_value in entity_financial_amount.CURRENCY_ABBREVIATIONS
        ) or (_token_value in entity_financial_amount.CURRENCY_ALL):
            token_list, counter = identify_financial_amounts(counter, token_list)

        counter += 1

    return token_list


def indexes_of_financial_amount(token_index: int, token_list: List[Token]) -> Tuple[int, int]:
    """
    REWORK
    Identify a financial amount in a list of tokens and return the indexes of starting and ending tokens.
    """
    initial_index, final_index = token_index, token_index
    # we test if we should go backward or forward to search for the amount
    # case 15 $
    if token_index != 0 and token_list[token_index - 1].category == "numeric":
        initial_index, final_index = look_backward_for_amount(token_index, token_list)
    # case USD 15
    elif (token_index != len(token_list) - 1 and token_list[token_index + 1].category == "numeric"):

        initial_index, final_index = look_ahead_for_amount(token_index, token_list)

    return initial_index, final_index


def toto(initial_index: int, final_index: int, token_list: List[Token]) -> List[Token]:
    # The token is just a currency symbol not followed by any numbers
    if initial_index == final_index:
        return token_list

    # Update the token list and value with the financial amount token identified
    value = "".join(
        [
            _token.string
            for _token in token_list[initial_index: final_index + 1]
        ]
    )
    new_token = Token(value, True)
    new_token.is_financial_amount = True
    new_token_list = (token_list[:initial_index] + [new_token] + token_list[final_index + 1:])
    return new_token_list


def identify_financial_amounts(
    token_index: int, token_list: List[Token]
) -> (List[Token], int):
    """
    Identify a financial amount in a list of tokens and crunch corresponding tokens into one.
    """
    initial_index, final_index = token_index, token_index

    # we test if we should go backward or forward to search for the amount
    # case 15 $
    if token_index != 0 and token_list[token_index - 1].category == "numeric":
        initial_index, final_index = look_backward_for_amount(
            token_index, token_list
        )
    # case USD 15
    elif (
        token_index != len(token_list) - 1 and
        token_list[token_index + 1].category == "numeric"
    ):
        initial_index, final_index = look_ahead_for_amount(
            token_index, token_list
        )

    # merge/ create new token list 

    # The token is just a currency symbol not followed by any numbers
    if initial_index == final_index:
        return token_list, token_index

    # Update the token list and value with the financial amount token identified
    value = "".join(
        [
            _token.string
            for _token in token_list[initial_index: final_index + 1]
        ]
    )
    new_token = Token(value, True)
    new_token.is_financial_amount = True
    new_token_list = (
        token_list[:initial_index]
        + [new_token]
        + token_list[final_index + 1 :]
    )
    return new_token_list, initial_index


def look_ahead_for_amount(
    token_index: int, token_list: List[Token]
) -> (int, int):
    # we are going forward
    # The amount could look like ["euros","300"] or ["$","12",".","540"] or ["$", "25",",","000", ".", "00"]
    # Test on the value of type $xxx,xxx.xxx
    initial_index, final_index = token_index, token_index
    n_tokens = len(token_list)
    # format $xxx,xxx.xxx
    if (
        (
            token_index != n_tokens - 2 and
            token_list[token_index + 2].value() == ","
        ) and (
            token_index != n_tokens - 3 and
            verify_numeric_token(token_list[token_index + 3], 3)
        ) and (
            token_index != n_tokens - 4 and
            token_list[token_index + 4].value() == "."
        ) and (
            token_index != n_tokens - 5 and
            token_list[token_index + 5].category == "numeric"
        )
    ):
        final_index = token_index + 5
    # format $xxx,xxx or $xxx.xxx 
    elif token_index != n_tokens - 2 and (
        token_list[token_index + 2].value() == "." or
        token_list[token_index + 2].value() == ","
    ):
        # The amount should look like ["$","12",".","540"] or ["$","12",",","540"]
        if (
            token_index != n_tokens - 3 and
            token_list[token_index + 3].category == "numeric"
        ):
            final_index = token_index + 3
        else:
            final_index = token_index + 1
    # format $ 12 540
    # The amount should look like ["$","12","540"]
    elif (token_index != n_tokens - 2) and (
        token_list[token_index + 2].category == "numeric"
    ):
        final_index = token_index + 2
    # $ xxxxx{1,n}
    else:
        final_index = token_index + 1

    # Special case where there is 2 symbols, e.g. ["$", "12", "USD"]
    if (final_index != n_tokens - 1) and (
       (token_list[final_index + 1].value() in entity_financial_amount.CURRENCY_ABBREVIATIONS) or
       (token_list[final_index + 1].value() in entity_financial_amount.CURRENCY_ALL)):
        final_index = final_index + 1
    return initial_index, final_index


def look_backward_for_amount(
    token_index: int, token_list: List[Token]
) -> (int, int):
    # We are going backward
    # The amount could look like ["300","euros"] or ["12",".","540","$"] or ["25",",","000", ".", "00", "$"]
    # Test on the value of type xxx,xxx.xxx$
    initial_index, final_index = token_index, token_index
    # format xxx,xxx.xxx $
    if ((token_index != 1 and token_list[token_index - 2].value() == ".") and
       (token_index != 2 and verify_numeric_token(token_list[token_index - 3], 3)) and
       (token_index != 3 and token_list[token_index - 4].value() == ",") and
       (token_index != 4 and token_list[token_index - 5].category == "numeric")):
        initial_index = token_index - 5
    # format xxx,xxx$ or xxx.xxx$
    elif token_index != 1 and (
        token_list[token_index - 2].value() == "." or
        token_list[token_index - 2].value() == ","
    ):
        # The amount should look like ["12",".","540","$"] or ["12",",","540","$"]
        if (token_index != 2 and token_list[token_index - 3].category == "numeric"):
            initial_index = token_index - 3
        else:
            initial_index = token_index - 1
    # The amount should look like ["12","540","$"]
    # format 12 540$
    elif (token_index != 1 and token_list[token_index - 2].category == "numeric"):
        initial_index = token_index - 2
    # xxxxx{1,n} $
    else:
        initial_index = token_index - 1
    # Special case where there is 2 symbols, e.g. ["12","$","USD"]
    if token_index != len(token_list) - 1 and (
        (
            token_list[token_index + 1].value()
            in entity_financial_amount.CURRENCY_ABBREVIATIONS +
            entity_financial_amount.CURRENCY_ALL
        )
    ):
        final_index = token_index + 1
    return initial_index, final_index


def verify_numeric_token(token: Token, expected_shape: int or None) -> bool:
    if expected_shape is None:
        return token.category == "numeric"
    else:
        return (
            token.category == "numeric" and
            len(token.value()) == expected_shape
        )


def generate_financial_amount_replacement(
    token: Token,
    financial_amounts_encountered: Dict,
    percentage_financial_amount_variation: int,
) -> (str, Dict):
    """
    Generate replacements for an amount and currency based on previous amounts generated to
    conserve coherence within document.
    """
    amount, currency = entity_financial_amount.get_amount_and_currency(
        token.value()
    )
    # case monnaie courante
    if "name" in currency.keys():  # only supported currencies have a name
        # We have already encountered the currency previously
        if currency["name"] in financial_amounts_encountered.keys():
            for replaced_amount, new_amount in financial_amounts_encountered[
                currency["name"]
            ]["amounts"]:
                # We have already encountered the amount previously
                if amount == replaced_amount:
                    return (
                        new_amount,
                        financial_amounts_encountered,
                    )

            currency_to_generate = financial_amounts_encountered[currency["name"]]["name"]
            currency_to_generate = entity_financial_amount.CURRENCIES[currency_to_generate]
            new_financial_amount = (
                entity_financial_amount.generate_specific_financial_amount(
                    amount,
                    currency,
                    currency_to_generate,
                    financial_amounts_encountered[currency["name"]][
                        "symbol_chosen"
                    ],
                    percentage_financial_amount_variation,
                )
            )

            if len(token.string.split(" ")) > 1:
                new_financial_amount += " "

            financial_amounts_encountered[currency["name"]]["amounts"].append(
                (amount, new_financial_amount)
            )
        else:
            # We have never encountered the currency previously
            currencies_generated = [
                _c["name"] for _c in financial_amounts_encountered
            ]
            (
                new_financial_amount,
                new_currency,
                new_symbol,
            ) = entity_financial_amount.generate_financial_amount(
                amount,
                currency,
                currencies_generated,
                percentage_financial_amount_variation,
            )

            if len(token.string.split(" ")) > 1:
                new_financial_amount += " "

            financial_amounts_encountered[currency["name"]] = {
                "name": new_currency["name"],
                "symbol_chosen": new_symbol,
                "amounts": [(amount, new_financial_amount)],
            }

        return new_financial_amount, financial_amounts_encountered
    # case others: just replace the financial amount
    # detected but unsupported currency -> we just vary the amount
    return (
        entity_financial_amount.generate_new_format(
            entity_financial_amount.generate_new_amount(
                amount, percentage_financial_amount_variation
            ),
            currency["symbol"][0],
        ),
        financial_amounts_encountered,
    )
