# err-tag

Makes the bot spit out text for tags you define.  
If you feel like you have to explain the same stuff every 2 days, this could be useful.

Example    
Day1  
BotOwner: !tag add baby 'detailedInstructionsOfProcess'  

Day2  
User1: How is baby made again?  
BotOwner: !tag baby  
Bot: 'detailedInstructionsOfProcess'

```
Simple plugin for tagging messages or general information

- .tag - Fetches a tag, usage: .tag <tag>
- .tag add - Adds a new tag, usage: .tag add <tag> <message>
- .tag del - Removes tag from database, usage: .tag del <id>
- .tag details - Returns further details about a tag, usage .tag details <tag>
- .tag find - Searches the tags and their messages for given keyword, usage: .tag <args>
- .tag new - Returns the latest 3 tags, usage .tag new
```
inspired by https://github.com/Rapptz/RoboDanny
