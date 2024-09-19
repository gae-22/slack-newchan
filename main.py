import os
import json
from typing import Union

import requests
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

load_dotenv()

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
CHANNEL_ID = os.environ["SLACK_CHANNEL_ID"]

client = WebClient(token=SLACK_BOT_TOKEN)


def load_json_file(filename: str) -> list[str]:
    """Loads a JSON file and returns its content as a list. Creates an empty file if it doesn't exist."""
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump([], f)
        return []

    with open(filename, "r") as f:
        return json.load(f)


def get_channels() -> list[str]:
    """Fetches all channels from Slack and returns their IDs."""
    channels_info = []
    cursor = None

    try:
        while True:
            response = client.conversations_list(cursor=cursor)
            channels_info.extend(response["channels"])
            cursor = response["response_metadata"].get("next_cursor")
            if not cursor:
                break
    except SlackApiError as e:
        print(f"Error fetching conversations: {e.response['error']}")

    return [channel["id"] for channel in channels_info]


def get_new_channels() -> list[str]:
    """Compares old and current channel lists and returns a list of new channel IDs."""
    old_channels = load_json_file("channels.json")
    current_channels = get_channels()

    new_channel_ids_list = [
        channel_id for channel_id in current_channels if channel_id not in old_channels
    ]

    with open("channels.json", "w") as f:
        json.dump(current_channels, f, indent=4, ensure_ascii=False)

    return new_channel_ids_list


def create_block(new_channels: list[str]) -> Union[str, dict]:
    """Creates a Slack message block for new channels."""
    if not new_channels:
        return "No new channels to send."

    message = "New channel just landed! :tada:\n" + "".join(
        f"- <#{channel_id}> \n" for channel_id in new_channels
    )

    return {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message,
                },
            }
        ]
    }


def send_new_channels_to_slack(new_channels: list[str]) -> None:
    """Sends a message to Slack with the list of new channels."""
    if not new_channels:
        print("No new channels to send.")
        return

    blocks = create_block(new_channels)
    if isinstance(blocks, str):
        print(blocks)
        return

    try:
        response = requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={
                "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
                "Content-Type": "application/json",
            },
            json={
                "channel": CHANNEL_ID,
                "username": "newchan",
                "blocks": blocks["blocks"],
            },
        )
        response.raise_for_status()
        print("Message sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")


if __name__ == "__main__":
    new_channels = get_new_channels()
    send_new_channels_to_slack(new_channels)
