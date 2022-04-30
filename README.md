# SMS Bot

## Setup
1. Open Terminal
2. Install the required libraries
    ```bash
    # install the dependencies from
    python3 -m pip install -r requirements.txt
    ```

## Run the Bot
1. Open Terminal
2. Enter the `bot` folder: `cd /path/to/bot`
3. Run the code (number after `-n` is how many conversations to generate): 
   ```bash
   python3 bot.py sms-2022-04-15_07-50-13.json -n 10 --from James --to Sue
   ```

To give a starting phrase:

```bash
python3 bot.py sms-2022-04-15_07-50-13.json -n 10 --from James --to Sue --start "I can't believe you are"
```

To start the conversation with the sender or recipient use `%to%` or `%from%`.
For example, to start the conversation with James saying "what are you up to":
```bash
python3 bot.py sms-2022-04-15_07-50-13.json -n 10 --from James --to Sue --start "%from% what are you up to"
```


## Help
```
usage: bot.py [-h] [-n NUM] -f FROM -t TO [-s START] input_file

positional arguments:
  input_file            path to the json file containing the conversation

optional arguments:
  -h, --help            show this help message and exit
  -n NUM, --num NUM     number of conversations to create
  -f FROM, --from FROM  the person the messages were sent from
  -t TO, --to TO        the person the messages were sent to
  -s START, --start START
                        the starting phrase
```