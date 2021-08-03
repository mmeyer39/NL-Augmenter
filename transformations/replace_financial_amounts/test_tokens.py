from transformations.replace_financial_amounts import token


def test_toto():
    input = True
    assert input


def test_create_tokens():
    tt = token.create_tokens("Could you buy me giftcard at 39.99€")
    assert tt[6].category == "numeric"


def test_indexes_of_financial_amount():
    tt = token.create_tokens("Could you buy me giftcard at 39.99€")
    # for t in tt:
    #     print(f"{t}")
    # i, j = token.indexes_of_financial_amount(6, tt)
    print(i, j)
    assert i == 0
    assert j == 0


# def test_find_financial_amounts():
#     tt = token.create_tokens("Could you buy me giftcard at € 39.99")
#     for i, t in enumerate(tt):
#         print(f"{i}: {t}")
#     results = token.find_financial_amounts(tt)
#     for i, t in enumerate(results):
#         print(f"{i} ({t.category}): {t}")
#     assert results[0] == "Could"
