import os
import znc
import hashlib
from slackclient import SlackClient

SLACK_TOKEN = os.environ.get('SLACK_TOKEN', None)
slack_client = SlackClient(SLACK_TOKEN)

notice_channel = "waffle-pings"
chat_channel = "waffles"
test_channel = "test"

# Begin Slack


def slack_message(channel_id, slackname, message):
        slack_client.api_call(
            "chat.postMessage",
            channel=channel_id,
            text=message,
            username=slackname,
            icon_emoji=':robot_face:'
        )

slack_message(test_channel, 'wafflebot', "initialized")

# Begin Spam Protection
array = ['']


def make_hash(hash):
    h = hashlib.new('sha256')
    h.update(hash)
    return h.hexdigest()


def check_spam(message):
    check = str(make_hash(message))
    slack_message(test_channel, 'bot', check)
    if check in array[0]:
        slack_message(test_channel, 'bot', 'returned true')
        return True
    else:
        slack_message(test_channel, 'bot', 'returned false')
        array[0] = check
        slack_message(test_channel, 'bla', check)
        return False

# Begin ZNC


class zncnoticeslack(znc.Module):
    description = "Forwards IRC Channel Notices to Slack"
    module_types = [znc.CModInfo.UserModule]

    def OnChanNotice(self, nick, channel, message):
        network = self.GetNetwork().GetName()
        nick = nick.GetNick()
        channel = channel.GetName()
        message = str(message)
        encoded_message = message.encode('utf-8')

        full_message = '[{0}] {1}'.format(nick, message)

        if check_spam(encoded_message):
            pass
        else:
            slack_message(notice_channel, 'wafflebot', full_message)

        return znc.CONTINUE

    def OnChanMsg(self, nick, channel, message):
        network = self.GetNetwork().GetName()
        nick = nick.GetNick()
        channel = channel.GetName()
        message = str(message)

        full_message = '{0}'.format(message)
        name = '{0}'.format(nick)
        slack_message(chat_channel, name, full_message)

        return znc.CONTINUE
