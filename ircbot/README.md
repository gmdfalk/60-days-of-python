# demibot  

## A modular IRCBot 
  
##### What it currently provides:  
  * Logs both system messages and chat. URLs are logged to a separate file.
  * Modularity, borrowed from [**Pyfibot**](https://github.com/lepinkainen/pyfibot) (which also means their modules are mostly compatible with demibot, some of which are already included here).
  * Configuration file.
  * Lots of commands:
    * Admin actions:
      * update: Pull the bot sources from the official github.
      * rehash: Reload all modules.
      * urls: Enable/disable printing of URL titles to the chat.
      * logs: Enable/disable chatlogging.
      * setnick: Change the nick of the bot.
      * setlead: Change the command identifier of the bot (default is ".").
      * setmin: Set minimum required permission level to perform commands. anything above 0 disabled public access.
      * settopic: Set the channel topic.
      * admins: Add/delete/list admins.
      * join/leave/channels: Join, leave or list channels.
      * quit: Quit this bot instance or optionally the whole program.
      * mode: Set a mode on a user e.g. +o, -v, +b (OP, voice, ban).
      * kick, tempban
    * Mildly useful:
      * bmi: calculate your body-mass-index.
      * btc: show bitcoin exchange rate (from mtgox, no idea if this is accurate).
      * g: perform a google search.
      * yt: perform a youtube search.
      * wiki: perform a wikipedia search.
      * quiz: a very rudimentary quizbot. gives no hints, takes no answers. just guess. to be improved.
      * translate and transliterate: uses google to translate text to english.
    * Fun stuff:
      * 8ball: Ask the magic 8ball.
      * cointoss: Flip a coin.
      * randomname: Prints random names from lots of countries/ethnicities.
      * randomnumber: Next-generation PRNG.
      * range: Random number in a specified range.
      * swanson: Quotes from ron swanson.
      * whatshesaid: Quotes from famous females.    
    * Debugging/info:
      * setvar, printvars: Set or display internal variables. 
      * me: Shows some information about the user.
      * version: Prints version and source of demibot.
      * date: Time and date information.
      
      
##### Features and modules I'd like to introduce:  
  * Log rotation and maybe use syslog or twisteds logger instead of logging.
  * Database logging (would allow many interesting functionalities).
  * Collecting and displaying notes and quotes (!give, !grab, !q nick, !rq etc).
  * Channel and server password support.
  * Search channel log.
  * Possible modules:
    * Weather
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
 
 You probably want to create either $HOME/.demibot or $HOME/.config/demibot, customize
 your demibot.ini and store it there.
 
 ### Usage:  
 
 For a simple test run, on-the-fly changes/setups or bot stacking, there is a command-line interface.  
   
 Examples:  
 ```
 demibot irc.freenode.net:6667 python,bash,linux -a adminnick -n botnick -p nickservpw
 demibot irc.quakenet.org #cs,#offtopic -a adminnick --ssl -l /your/log/dir
 ```