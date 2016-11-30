from pychat.crypto import RSA
import gnupg 


gpg=gnupg.GPG()
with open("RUkey.asc") as keyfile:
    key_data=keyfile.read()
    try:
        import_result = gpg.import_keys(key_data)
    except ValueError:
        pass
    print(import_result.results)
    result = gpg.encrypt("Hi there, Jonathan"
                        , import_result.results[0]["fingerprint"]
                        , always_trust=True
                        )
    print("RESULT: ", repr(result))
    print(str(result))
    with open("hellojonathan.pgp", "w") as resultfile:
        resultfile.write(str(result))
