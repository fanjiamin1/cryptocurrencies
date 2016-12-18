from shamir import Shamir


def test_extract_keys():
    k = 7
    secret = 113
    amount_of_keys = 30
    shamir = Shamir(k, secret)
    keys = [shamir.get_key() for _ in range(amount_of_keys)]
    for n in range(1, amount_of_keys+1):
        key_subset = keys[:n]
        extracted_secret = Shamir.extract_secret(key_subset)
        if n < k:
            # Can get secret... but let's assert anyway
            assert extracted_secret != secret
        else:
            assert extracted_secret == secret
        
