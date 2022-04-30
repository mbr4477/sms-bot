import json
import argparse
import re
import markovify


def prettify_output(out: str, to_name: str, from_name: str) -> str:
    """Make the output nicer by putting in names.

    Args:
        out: The raw output from the bot.
        to_name: The name of the recipient
        from_name: The name of the sender

    Returns:
        The prettified output.
    """
    out = out.replace("%to%", f"\n{to_name}: ")
    out = out.replace("%from%", f"\n{from_name}: ")
    return out


def main(args):
    # Open the input JSON file with text messages
    with open(args.input_file, "rb") as json_file:
        content = json.loads(json_file.read())

    # Combine all the text messages into a single corpus string
    corpus = ""
    for message in content:
        # Set the sender based on the message direction
        sender = "%from%" if message["messageDirection"] == "OUTGOING" else "%to%"
        # Add the sender and the message to a new line of the corpus
        corpus += sender + " " + message["body"].replace("\n", " ") + "\n"

    # Make everything lowercase and remove extra whitespace
    corpus = re.sub(r"\s+", " ", corpus).lower()

    # Create the bot (Markov chain)
    chain = markovify.Text(corpus, state_size=2)

    # Get the starting state
    prefix = ""
    if args.start is not None:
        state = tuple(args.start.split(" ")[-2:])
        prefix = " ".join(args.start.split(" ")[:-2])
    else:
        state = None

    # Create all the conversations using the bot
    convos = [
        prettify_output(
            prefix
            + " "
            + chain.make_sentence(max_overlap_total=8, tries=100, init_state=state),
            args.to,
            args._from,
        )
        for _ in range(args.num)
    ]

    # Print out the conversations
    print(f"I fed a bot {len(content)} of our texts and this is what it gave me:")
    print("\n\n----------\n".join(convos))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_file", type=str, help="path to the json file containing the conversation"
    )
    parser.add_argument(
        "-n", "--num", type=int, help="number of conversations to create", default=1
    )
    parser.add_argument(
        "-f",
        "--from",
        metavar="FROM",
        dest="_from",
        type=str,
        help="the person the messages were sent from",
        required=True,
    )
    parser.add_argument(
        "-t",
        "--to",     
        type=str,
        help="the person the messages were sent to",
        required=True,
    )
    parser.add_argument("-s", "--start", type=str, help="the starting phrase")
    main(parser.parse_args())
