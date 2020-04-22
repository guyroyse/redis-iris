# Iris Classification with RedisAI

## Get Python

You need a Python environment to make this all work. I used Python 3.8—the latest, greatest, and most updatest at the time of this writing. I also used `venv` to manage my environment.

I'll assume you can download and install Python 3.8 on your own. So lets go ahead and setup the environment:

    $ python3.8 -m venv venv

Once `venv` is installed, you need to activate it:

    $ . venv/bin/activate

Now when you run `python` from the command line, it will always point to Python3.8 and any libraries you install will only be for this specific environment.

If you want to deactivate this environment, you can do so from anywhere with the following command:

    $ deactivate

## Install Protobuf

You'll need protobuf to use use ONNX. I did a quick install like this:

    $ brew install protobuf

As of the time of this writing, protobuf 3.11 does not work with ONNX. So I had to laboriously install protobuf 3.10.1.

## Get Some Dependencies

Next, let's install all the dependencies. These are all listed in `requirements.txt` and can be installed with `pip` like this.

    $ pip install -r requirements.txt

Run that command, and you'll have all the dependencies installed and will be ready to run the code.

## Build the ONNX Model

This is as easy as running the following:

    $ python build.py

## Import the Model into Redis

    $ redis-cli -x AI.MODELSET iris ONNX CPU < logreg_iris.onnx

## Make Some Predictions

Launch redis-cli:

    $ redis-cli

Set the input tensor with 2 sets of inputs of 4 values each:

    > AI.TENSORSET iris_in FLOAT 2 4 VALUES 5.0 3.4 1.6 0.4 6.0 2.2 5.0 1.5

Make the predictions:

    > AI.MODELRUN iris INPUTS iris_in OUTPUTS iris_out:1 iris_out:2

Check the predictions:

    > AI.TENSORGET iris_out:1 VALUES

    1) (integer) 0
    2) (integer) 1
