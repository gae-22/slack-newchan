## README.md

# Slack Channel Notifier

This project is a Python script designed to interact with the Slack API to monitor and notify about new Slack channels. It fetches the list of current channels, compares it with a previously stored list, and sends a notification to a specified Slack channel if new channels are detected.

## Features

-   **Fetch Channels**: Retrieves all channels from Slack.
-   **Detect New Channels**: Compares the current list of channels with a stored list to identify new channels.
-   **Notify via Slack**: Sends a message to a designated Slack channel listing any new channels.

## Requirements

-   Python 3.x
-   `requests` library
-   `python-dotenv` library
-   `slack_sdk` library

## Setup

1. **Clone the repository**:

    ```bash
    git clone https://github.com/gae-22/slack-newchan.git
    cd slack-newchan
    ```

2. **Install dependencies**:

    ```bash
    rye sync
    ```

3. **Environment Variables**: Create a `.env` file in the root directory and add your Slack Bot Token and Channel ID:

    ```
    SLACK_BOT_TOKEN=your-slack-bot-token
    SLACK_CHANNEL_ID=your-slack-channel-id
    ```

## Usage

Run the script to check for new channels and send notifications:

```bash
rye run python main.py
```

## Code Overview

-   **load_json_file(filename: str)**: Loads or initializes a JSON file.
-   **get_channels()**: Fetches all channel IDs from Slack.
-   **get_new_channels()**: Identifies new channels by comparing current and previous lists.
-   **create_block(new_channels: list[str])**: Creates a message block for new channels.
-   **send_new_channels_to_slack(new_channels: list[str])**: Sends a notification to Slack with the new channel information.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

This README provides an overview of how to set up and use the Slack Channel Notifier script, including its features, requirements, setup instructions, usage, code overview, contribution guidelines, and license information.
