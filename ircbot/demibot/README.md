# demibot  

## A modular IRCBot 
  
##### What it currently provides:  
  * Logs both system messages and chat. URLs are logged to a separate file.
  * Modularity/Plugins (taken from [**Pyfibot**](https://github.com/lepinkainen/pyfibot)) so their modules are mostly compatible with demibot, some of which i even included.
  * Lots of commands:
    * admin actions:
      * update: pull the bot sources from the official github
      * rehash: reload all modules
      * urls: enable/disable printing of URL titles to the chat.
      * logs: enable/disable chatlogging.
      * setnick: change the nick of the bot
      * setlead: change the command identifier of the bot (default is ".")
      * setmin: set minimum required permission level to perform commands. anything above 0 disabled public access.
      * settopic: set the channel topic.
      * admins: add/delete/list admins.
      * join/leave/channels: join, leave or list channels.
      * quit: quit this bot instance or optionally the whole program.
      * mode: set a mode on a user. this is used for mose channel operations.
      * kick, tempban
    * debugging/info:
      * setvar, printvars: set or display internal variables. 
      * me: shows some information about the user.
      * version: prints version and source of demibot.
      * date: time and date information.
    * mildly useful ones:
      * bmi: calculate your body-mass-index.
      * btc: show bitcoin exchange rate (from mtgox, no idea if this is accurate).
      * g: perform a google search.
      * quiz: a very rudimentary quizbot. gives no hints, takes no answers. just guess. to be improved.
      * translate and transliterate: uses google to translate text to english.
    * fun stuff:
      * 8ball: ask the magic 8ball.
      * cointoss: flip a coin.
      * randomname: prints random names from lots of countries/ethnicities.
      * randomnumber: next-generation PRNG.
      * range: random number in a specified range.
      * swanson: quotes from ron swanson.
      * whatshesaid: quotes from famous females.    
    
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