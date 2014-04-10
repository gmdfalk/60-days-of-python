# demibot  

## An IRCBot written in Python.  
  
##### What it currently provides:  
  * Logs both system messages and chat. URLs are logged to a separate file.
  * Modularity/Plugins (taken from [**Pyfibot**](https://github.com/lepinkainen/pyfibot))  
    so their modules are mostly compatible with demibot, some of which i even included.
  * Many commands and modules (type .help or look through the modules directory)
    
##### Features and modules I'd like to introduce:  
  * Log rotation and maybe use syslog or twisteds logger instead of logging.
  * Database logging (would allow many interesting functionalities).
  * Collecting and displaying notes and quotes (!give, !grab, !q nick, !rq etc)
  * Channel password support.
  * Search channel log.
  * Possible modules:
    * Weather
    * Dictionary/Wiki queries
    * Seen+Tell
    * RSS+Github
    * IMDB/TVcal
    * Twitter
    * Polling
    * Evaluate python/bash/regex
    * Fortune cookie quotes
    * Markov-Chain for "smart" conversation
    * Wolfram Alpha?
 
 ### Installation:  
 ```
 git clone https://github.com/mikar/demibot
 cd demibot
 pip install .
 ```  
 
 There you go, that's it.  
 
 ### Usage:  
 
 You probably want to modify config.py in the installation directory of demibot,
 which provides you with multi-server support and fine-grained configuration.  
 You can create a file called "auth" in either the installation directory or
 $HOME/.config/demibot or $HOME/.demibot from which nickserv and server passwords
 can be read.  
 By default, public commands and url title display are disabled. You can enable
 them with `.setmin 0` and `.urls on` or permanently in the Factory class by setting
 `self.titles_enabled = True` and `self.minperms = 0`.
 
 
 For a simple test run, on-the-fly changes/setups or bot stacking, there is a command-line interface.  
   
 Examples:  
 ```
 demibot irc.freenode.net:6667 python,bash,linux -a adminnick -n botnick -p nickservpw
 demibot irc.quakenet #cs,#offtopic -a adminnick --ssl -l /mnt/share/weird/place/for/logs
 ```