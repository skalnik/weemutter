WeeMutter
=========

Send push notifications to [Mutter](https://www.mutterirc.com/) from
[Weechat](https://weechat.org/). (This is because I don't use
ZNC as my Bouncer, so I can't use the
[Mutter ZNC Module](https://bitbucket.org/jmclough/mutter-push/overview).

##To use
Get your apple push token for mutter. I may eventually automate this,
but since Weechat's relay doesn't seem to have an easy way of adding
server CAPs, it can't be automated in the way that it is for the ZNC
module.

Open up a listening netcat/socat on your machine, add a server in mutter
to connect to it, and tell it you support the ```mutterirc.com/push``` CAP.

    echarlie@localhost:~ $ nc -6 -l 6667 
    CAP LS
    NICK echalie
    USER echarlie * * :Mutter User
    :weechat.relay.irc CAP nick LS :mutterirc.com/push

    CAP REQ mutterirc.com/push
    :fake.irc.server CAP echarlie ACK :mutterirc.com/push                                                         
    CAP END
    :fake.irc.server 001 echarlie :Hello
    
    MUTTER BEGIN 67FA492439FCB92C2A55555927208206CF19076447777777FD8BE9F5326C94ED
    MUTTER VERSION 67FA492439FCB92C2A55555E27208206CF19076447777777FD8BE9F5326C94ED 1.0
    MUTTER KEYWORD 67FA492439FCB92C2A55555E27208206CF19076447777777FD8BE9F5326C94ED :echalie
    MUTTER END 67FA492439FCB92C2A55555E27208206CF19076447777777FD8BE9F5326C94ED

That long numeric string is the token. Set it as ```MUTTER_TOKEN = ''``` in
the script.

##Features

- It sends push notifications when you don't have mutter open, on highlighs and private messages

##Bugs

- No in-Weechat configuration
- No easy way to get tokens
- Formatting of push notification is ugly
- sends notifications whether or not you are away

