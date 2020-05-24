# jkChess
jkChess is a REST API to play easly chess. It´s built on Python.

The API consist of some REST methods in order to provide functionality to play several games simultaneously.
There is also an Angular 9 client which consumes the REST API and provides a graphical interface to play.

The project consist of three main modules, MongoDb as database for all chess data and games, Python REST API to play chess via HTTP and Angular 9 for the graphical client interface.

## 0. Requirements
To deploy your own jkChess you will need to have installed on your computer:
- Docker
- Docker compose
- (Optional) Docker swarm

## 1. Installation and setup
The entire project is based on docker, in order to run it, you only need to run the stack with:
```
$ docker-compose -f docker-compose.yml up
```

If you wish to run it within a swarm you can simply run:
```
$ docker stack deploy --compose-file docker-compose.yml jkchess
```
   
The images might be built diretly using Dockerfiles, but the project is intended to separate both angular ui and rest api in a way that separate images might be used in other places.

### Image of the Python REST API
If you want to modify and try new things on your own, you can recreate images in your own dockerhub by running these commands cloning the rest api repository [jkChess-rest-api](https://github.com/jcrecio/jkChess-rest-api)
```
docker build -t <your rest api python image path>:latest -f ./Dockerfile .
docker push <your rest api python image path>:latest
```
Then replace in the *docker-compose.yml* the image *jcrecio/jkchess-restapi:latest* by your own image.

### Image of the Angular Client
If you want to modify and try new things on your own, you can recreate images in your own dockerhub by running these commands cloning the angular ui client repository [ngJkChess](https://github.com/jcrecio/ngJkChess):
```
docker build -t <your angular image path>:latest -f ./Dockerfile .
docker push <your angular image path>:latest
```
Then replace in the *docker-compose.yml* in this same directory, the image *jcrecio/jkchess-restapi:latest* by your own image.

As of now, the chess API depends on the engine rybka.exe to play.
The core is based on python-chess to translate moves to UCI:
[Python-chess library documentation](https://python-chess.readthedocs.io/en/latest/)

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
