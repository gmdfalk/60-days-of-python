demibot
==================
An IRCBot written in Python.  
--
  
What it currently does:  
  * Logs chat messages.
  * Splits urls into a separate logfile (why not?).
  * Basic commands:
    * join: Join one or more channels, comma separated.
    * leave: Leave one or more channels.
    * rehash: Reload modules.
    * me: Shows how you are registered with the bot (superadmin, admin, none).  
          Might be expanded to include various stats, e.g. your ping or score.  
  * Provides modules:
    * bmi: calculate the body mass index with height/weight.
    * whatshesaid: quotes from emancipated women ([**collected by jessamynsmith**](https://github.com/jessamynsmith/talkbackbot)).
    * swanson: quotes from the one and only Ron Swanson.  
    * timer: pings you with a message after n seconds.
    * quiz: asks questions, gives hints and takes answers.
    
Quite a bit of the code is adopted from [**Pyfibot**](https://github.com/lepinkainen/pyfibot), including the BMI-module.  
  
Features and modules I'd like to introduce:  
  * Quiz (with a database. smart autohinting, highscores, etc)
  * Conduct a poll.
  * Search channel log.
  * HTTP link capture/collection/storage. Displaying the title tag in the chat.
  * Implement some popular online service modules:
    * Weather and date/time information (day + week number, too)
    * Google search
    * Google translate
    * Dictionary/Wiki queries
    * Wolfram Alpha?
  * Collecting and displaying notes and quotes from the chat (sorted by nick)
  * Database of nicks. Allow adding quotes and with quotes and authorizations, allowing querying (like last seen).
  * Evaluate python/bash/regex.
  * Store notes with keyword and repeat them on demand (!give nick note)
  * Operator/Auth features (Kick, Ban, Silence, give OP to admins etc)
  * Disable/enable commands, public ignore
  * Fortune cookie quotes
  * Markov-Chain for "smart" conversation
  * Tomorrow is Monday
  