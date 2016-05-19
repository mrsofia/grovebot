General idea:

Data input: Scan each message for a link to YouTube, Spotify, or Soundcloud. Stretch goal: also successfully handle raw spotify URIs.

On the backend: convert those links into database rows, with columns for 'URL', 'message_time', etc. Stretch goal: successfully parse song and artist names from each link so that we can gather stats about how often a song or artist is shared

In the chat: interact directly with the bot via @grovebot commands. examples:
`@grovebot 5/5/2015`
--> grovebot would respond with all the tracks from that day

`@groveboy today`
--> grovebot would respond with all the tracks posted today

each evening grovebot will post a summary of all the tracks from that day.


Future stuff:

On the front end: render a web page that gets all of the current day's songs out of the database and presents them in the view. Also enable the user to see and search past days tracks. For the v1 we can get by just showing the current day's tracks

Other stretch goals would be:
- having some form of 'likes/fuegos' that would rank the songs based on how many people thought they were fuego
