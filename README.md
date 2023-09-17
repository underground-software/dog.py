# dog.py

A set of dog-themed externally-hosted site reliability tools
to monitor and alert admins to KDLP ORBIT service degradation

## Extant tools:

### dogdaemon.py

Purpose: Check service status at a configurable interval and report
any changes to a local alert delivery server.

The alert delivery service is implemented by the sms.py submodule
originally written to send a text message alert upon a succesful
login to the server when it was in earlier development. It's
a small general-purpose uwsgi relay app for calling the twilio API.

List of implemented status checks:
  * watch for 200 status code from GET kdlp.underground.software
