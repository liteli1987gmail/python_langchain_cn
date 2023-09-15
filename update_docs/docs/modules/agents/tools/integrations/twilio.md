# Twilio

This notebook goes over how to use the [Twilio](https://www.twilio.com) API wrapper to send a text message.

## Setup

To use this tool you need to install the Python Twilio package `twilio`


```python
# !pip install twilio
```

You'll also need to set up a Twilio account and get your credentials. You'll need your Account String Identifier (SID) and your Auth Token. You'll also need a number to send messages from.

You can either pass these in to the TwilioAPIWrapper as named parameters `account_sid`, `auth_token`, `from_number`, or you can set the environment variables `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM_NUMBER`.

## Sending a message


```python
from langchain.utilities.twilio import TwilioAPIWrapper
```


```python
twilio = TwilioAPIWrapper(
    #     account_sid="foo",
    #     auth_token="bar",
    #     from_number="baz,"
)
```


```python
twilio.run("hello world", "+16162904619")
```
