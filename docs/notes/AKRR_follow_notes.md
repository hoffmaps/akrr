## Notes on trying to follow what akrr is doing with pycharm...?
pycharms started with 
```bash
sudo /usr/local/bin/charm &
```

```bash
#nikolay suggested doing something like
akrr daemon startdeb
# as well as somehow using pycharm debugger
# so i'm trying to figure out what it all means now
```

```bash
# stopped the daemon with
akrr daemon stop

# then did that above
akrr daemon startdeb
# Result:
[2019-05-31 15:07:25,306 - INFO] Starting Application Remote Runner
[2019-05-31 15:07:25,317 - INFO] AKRR Scheduler PID is 9448.
[2019-05-31 15:07:25,327 - INFO] Starting REST-API Service
[2019-05-31 15:07:25,329 - INFO] ####################################################################################################
[2019-05-31 15:07:25,329 - INFO] Got into the running loop on 2019-05-31 15:07:25
[2019-05-31 15:07:25,329 - INFO] ####################################################################################################

Starting REST-API Service
Bottle v0.12.13 server starting up (using SSLWSGIRefServer())...
Listening on http://localhost:8091/
Hit Ctrl-C to quit.

#So its running in foreground now? unsure

```


Pycharm Debugging:
- need to set a break point (click next to line number) - debugger goes runs to that point and then stops. Then can step forward and proceed through the program step by step (i believe)
- cli init calls the util and log init too
- cli provides access to command line and uses log from akrr.util
- Anytime import happens, first goes through init
- So import akrr.cli -> akrr/__init__.py then once that is done it goes to cli/__init__
- __init__ files only look at the function definitions, don't run anything in functions
- In cli/init it eventually gets to the class defined as CLI - looks at those functions in there
- Once all the initing is done, goes to do akrr.cli.CLI().run()
	- This statement goest to the cli init file, where the class CLI is in. Now CLI calls its __init__ before its run can be called
- with arg parser in cli/__init__, it goes to commands to import those things - sets up argument parser
- in the cli run it looks at the args - and with debug there are no args so its an error

- To run the debugger with arguments, you have to go to Run -> Edit Configurations -> "+" and add a new config there
	- This sets the short_log_prefix to false

- It does cli_arg.func(cli_args) -> i think this tells the arg parser to just find the proper function based on the arguments given. It does end up going to the handler for daemon_startdeb in commands, which goes to daemon.py
- The daemon init starts gets a bunch of defaults started - also imports cfg (AKRR config?)
	- The config sets up some defaults as to what everything is called, what port things are connected to, where the data goes, job submit time wait/max time for job submit attempts, etc.
- Then cfg gets the directories where things are located
- Then goes to get akrr dirs - where it tries to get directories where everything is it seems
	- Unsure what all the directories are supposed to be, it seems the akrr_cli_fillpath isn't completely correct, unsure though - seems to just be pointing to the very initial akrr.py script
- All the variables from the config now come in and are present in cfg
- Then from cfg goes to cfg_util - this imports akrrError and some variables from akrr.cfg and util
- Towards end of cfg, reads in akrr.conf file
- Then verifies akrr conf - checks if files/variables needed exist
	- Seems to raise warnings if certain variables aren't in config file (akrr.conf)? but they do seem to be in the python script that did the config things...?
- loading resources - goes to resource directory and calls load_resource from cfg_util
- it reads in the config files and stores in all the variables they give - has stuff like the usernames and such to use for that resource, I'm assuming
- removes the built ins - so dictionary only has the variables given in the config file
- So then it has all the variables for that resource in a dictionary - that is then passed to a validation system
- 



