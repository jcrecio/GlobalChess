# GlobalChess
Global Chess is a REST API to play chess.

The API consist of some REST methods in order to provide functionality for several games.

## 1. Start playing
In order to start a new game you have 2 options, ask for the CPU move or do your own move.

### 1.1 CPU move
POST /game/<__game id__>/board/moves/best
It will apply and return the best CPU move for the game specified. If the game does not exist yet, it will create a new one with the first move done by the CPU.
The output of the method is as follows:
```json
{
  "Move": "CPU UCI form move, eg: c2c3"
}
```
 
### 1.2 Player move
POST /game/<__game id__>/board/move
It will apply the move done by the user. If the game does not exist yet, it will create a new one with the first move done by the user.
The output of the method is as follows:
```json
{
  "Move": "User form move, eg: c2c3"
}
```
