import json
import weechat
import requests

#MUTTER_PUSH_IRCV3_CAPABILITY = "mutterirc.com/push"
MUTTER_SERVER_URL = "https://api.mutterirc.com:8100"
MUTTER_STATE_FILE = "mutter.json"
MUTTER_USER_AGENT = "weemutter"
MUTTER_VERSION = '1.0'
MUTTER_TOKEN = ''

SCRIPT_NAME = 'weemutter'
SCRIPT_AUTHOR = 'echarlie'
SCRIPT_VERSION = '0.0'
SCRIPT_LICENSE = 'ISC'
SCRIPT_DESC = 'Send push notifs to mutter for iOS'

script_options = {
        'api_key' : '',
        'only_away' : ''
        }


weechat.prnt("", "Starting up weeMutter" )


def send_notif(body):
    #This is just mutter-push's send_notification function
    title = SCRIPT_NAME
    version = MUTTER_VERSION
    token = MUTTER_TOKEN
    session = requests.Session()
    session.headers['User-Agent'] = MUTTER_USER_AGENT
    alert = { 'title' : title, 'body' : body }
    payload = { 'version' : version, 'token' : token, 'alert' : alert }
    response = session.post(MUTTER_SERVER_URL, verify=False, data=json.dumps(payload), headers={"content-type": "text/javascript"})
    data = response.json()
    if 'error' in data and 'code' in data['error']:
        if data['error']['code'] == "200":
             expired_token = data['error']['token']
             self.remove_token_from_networks(expired_token)

def weemutter_cb(data, buf, args):
    #weechat.prnt("",args) #clearly for debug
    send_notif(args)
    return weechat.WEECHAT_RC_OK;


def print_cb(data, buf, date, tags, displayed, highlight, prefix, message):
    if highlight != 1 and weechat.buffer_get_string( buf, "localvar_type") != "private":
        return weechat.WEECHAT_RC_OK
    bufname = weechat.buffer_get_string(buf, "short_name")
    msg = "[%s] <%s> %s" % (bufname, prefix, message)
    send_notif(msg)
    #weechat.prnt("", msg ) #clearly for debug
    return weechat.WEECHAT_RC_OK

#eventual support for in-weechat config.
def init_config():
    weechat.hook_config("plugins.var.python." + SCRIPT_NAME + ".*", "config_cb", "")


#eventually should add support for live reconfiguration.
def config_cb(pointer, name, value):
    return weechat.WEECHAT_RC_OK;



if weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, "", ""):
    #hooks
    weechat.hook_command(SCRIPT_NAME, "send push notif to mutter", "<text>",
            "text: notification to send", "", "weemutter_cb", "")
    weechat.hook_print("", "notify_message,notify_private,notify_highlight", "", 1, "print_cb", "")
