# pychat

A message client project.

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

Open two terminal windows.
In the first one do

``
$ python -m pychat.Bob
``

and enter the things you are asked.
Then, in the second one, do

``
$ python -m pychat.Alice
``

and again enter the needed things.

Now you should be able to send messages from the Alice window to the Bob window.

After you are done chatting, you should be able to Ctrl-C out of both.
