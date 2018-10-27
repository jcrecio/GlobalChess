# GlobalChess
Global Chess is a REST API to play chess.

The API consist of some REST methods in order to provide functionality for several games.
## 1. Requirements
Install python-chess library. This is the chess library core the api uses underneath.  
Install Flask for supporting REST implementation.  

## 2. Run the server
You just need to execute the python file indicating the path of the engine to be used in the api.
```python
  restapi.py rybka.exe
````

## 1. Start playing
In order to start a new game you have 2 options, ask for the CPU move or do your own move.
All the moves follow the UCI chess format.  
[UCI Wikipedia](https://en.wikipedia.org/wiki/Universal_Chess_Interface)  
[UCI Protocol Specification](http://wbec-ridderkerk.nl/html/UCIProtocol.html)  

### 1.1 CPU move
POST /game/<__game id__>/board/moves/best
It will apply and return the best CPU move for the game specified. If the game does not exist yet, it will create a new one with the first move done by the CPU.  
There is no required information to be sent via POST, the CPU will change the state of the game directly with the best move it finds.  
  
The output of the method is as follows:
```json
{
  "Move": "CPU UCI form move, eg: c2c3"
}
```
 
### 1.2 Player move
POST /game/<__game id__>/board/move
It will apply the move done by the user. If the game does not exist yet, it will create a new one with the first move done by the user.  
The body request looks like:
```json
{ 
  "move": "a2a3" 
}
```
The output of the method is identical if the operation went well:
```json
{
  "Move": "a2a3"
}
```
