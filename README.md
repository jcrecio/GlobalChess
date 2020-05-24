# jkChess-rest-api
jkChess-rest-api is the REST API module built in Python that corresponds to the core functionality of [jkChess](https://github.com/jcrecio/jkChess/)
This REST API needs a mongo server and chess engine to run. (See details in line 16 and 29 on app.py file)

It normally runs as a part of the docker stack of [jkChess](https://github.com/jcrecio/jkChess/), in case you with to run it without docker you will need:
1. Python installed in the system.
2. Mongo installed in the system.
3. All the dependencies included in requirements.txt

## 2. Run the mongodb server without docker
The mongo server needs to be started off with the provided configuration file.      
```python
  mongod -f <path>/gamesdb.conf
````

You need to execute the python file indicating the path of the engine to be used in the api, if you do not specify any, it will use by default stockfish.
```python
  api.py /usr/bin/shredder
````
```python
  api.py /usr/bin/stockfish
````

## 2. Start playing
In order to start a new game you have 2 options, ask for the CPU move or do your own move.
All the moves follow the UCI chess format.  
[UCI Wikipedia](https://en.wikipedia.org/wiki/Universal_Chess_Interface)  
[UCI Protocol Specification](http://wbec-ridderkerk.nl/html/UCIProtocol.html)  

### Create new game
```javascript
POST /games/new      
HEADERS:      
  user: <user>
```
This operation creates a new game.

```json
HTTP RESPONSE: 201
{
  "GameId":  "GUID"
}
```

### CPU move
```javascript
POST /game/<__game id__>/board/moves/best    
```
It will apply and return the best CPU move for the game specified, no matter the turn.
There is no required information to be sent via POST, the CPU will change the state of the game directly with the best move it finds.  
  
The output of the method is as follows:
```json
HTTP RESPONSE: 201
{
  "Move": "CPU UCI form move, eg: c2c3"
}
```
 
### Player move
```javascript
POST /game/<__game id__>/board/move    
```
It will apply the move done by the user. If the game does not exist yet, it will create a new one with the first move done by the user.  
The body request looks like:
```json
{ 
  "move": "a2a3" 
}
```
The output of the method is identical if the operation went well:
```json
HTTP RESPONSE: 201
{
  "Move": "a2a3"
}
```

### Undo move
```javascript
POST /game/<__game id__>/board/undo    
```
It will undo the last move on the game. The moves' stack only includes the moves played during a session.
If you stopped playing a game and restarted lest´s day, next day, the stack will be empty.

The output of the method contains the current position after having applied the undo.
```json
HTTP RESPONSE: 201
{
  "PreviousPosition": "8/p1pk1ppp/4p3/N2rPb2/2p5/b1P1B3/P4PPP/4r1K1 w - - 0 24"
}
```

### Delete game
In order to remove an existing game.      
```javascript
DELETE /game/<__game id__>/delete    
```            
```
HTTP RESPONSE: 204
No content
```
## Display data
You can get the raw current position (8x8 squares matrix) of a game requesting via GET:  
```javascript
GET /game/<__game id__>/board    
```
```
HTTP RESPONSE: 200
{
  "Board": "r n b q k b n r\np p p p p p p p\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\n. . . . . . . .\nP P P P P P P P\nR N B Q K B N R"
}
```

## Retrieve all the existing games
You can get all the games
```javascript
GET /games   
```
```
HTTP RESPONSE: 200
{
  "Games": ["gameid1", ..., "gameid_N"]
}
```