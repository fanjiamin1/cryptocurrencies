# pychat

A one-way message client project.

## Setup

Having made sure you're running python 3, execute

```
$ python setup.py install
```

and then

```
$ sudo !!
```

after having remembered you need to escalate your privileges.

## Usage

### Connecting

Open two terminal windows.
In the first one do

``
$ python -m pychat.Bob
``

and enter the things you are asked.
The encryption key entered must be 16, 24, or 32 bytes long.
If no encryption key is entered, then the default of "0123456789defabc" is used.
Then, in the second one, do

``
$ python -m pychat.Alice
``

and again enter the needed things.

Now you should be able to send messages from the Alice window to the Bob window.

After you are done chatting, you should be able to Ctrl-C out of both.

### Chatting

Alice can send notes to Bob, but bob never answers.
Alice can also send Bob tasks with the _task_ keyword, e.g.:

```
task: hugo+ivar+ragnar 22
```

which would send Bob on a quest to find a 16 byte suffix to the 16 prefix bytes of "hugo+ivar+ragnar" such that the two hash together into a hash that ends with at least 22 zero bits.
Note that the prefix must be exactly 16 character bytes.
