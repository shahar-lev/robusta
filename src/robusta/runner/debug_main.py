import logging
import os
import os.path
import sys
from inspect import getmembers

from ..core.reporting.blocks import Finding
from ..core.sinks.msteams.msteams_sink import MsTeamsSink,MsTeamsSinkConfig


print('*** running ***')



def main():

    finding = Finding('some title')
    finding.title = 'test'
    finding.description = 'this is a short desc\nanother line'

    
    conf = MsTeamsSinkConfig()
    hook_url = "https://robusta650.webhook.office.com/webhookb2/b8b2b92a-02e9-4f5b-9c6f-3b77010d9cc6@34408606-07e6-4a82-98ac-c3668f4e57f5/IncomingWebhook/5479ec3149a34b99a0c7bca141787950/82e528f7-78de-4ded-9b84-0c6eb2c4883a"
    conf.msteams_hookurl = hook_url
    msteams_sink = MsTeamsSink(hook_url)
    msteams_sink.write_finding()
    print('*** done ***')
    pass

main()