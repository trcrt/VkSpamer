# VkSpamer
Spams messages to a certain VK user or group (not up-to-date).
Selects random message from messages file and sends it to certain user on selected schedule.

Requires "config.json" file with a certain format:
```json
{
    "messages_file": "./messages.txt",
    "target_id": 1234345,
    "message_delay_range": [10, 15],
    "skip_first_message": false,
    "access_token": ""
}
```
```
target_id: id of target user/group;
messages_file: path to file with messages;
message_delay_range: delay between messages (in seconds);
skip_first_message: send message on start or wait for message_delay_range;
access_token: VK access token.
```
