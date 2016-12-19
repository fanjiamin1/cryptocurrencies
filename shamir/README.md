# Shamir Secret Sharing

## Install

Make sure you are using a recent Python 3 (e.g., 3.5 currently) and run the following as a superuser:

```
# python setup.py install
```

## Usage

In a terminal window in any directory on your system, run (e.g.)

```
# python -m shamir.secret_sharing create 5 10 my_shares "This is my secret string"
```

to create a "5-out-of-10" secret share.
This will be a directory named my_shares with ten share files.

You can then extract your secret string as long as you have at least 5 of these secret shares in a directory:

```
# python -m shamir.secret_sharing extract my_shares
```
