# PySickle
The ~~PyRope~~ Octane Secondary Pickler *now my name doesn't work* :(

~~PyRope~~ Octane dug up lots of usable data from the replay. PySickle gets things rolling by turning its output network stream into usable data.
Used to parse a ~~PyRope network stream~~ Octane output JSON into usable data.

Pickle is used to output the file, and has to be used to input the file to be used.

## Usage:
Create a folder named pysickle with this stuff inside. Move _pys.py to the same directory as the pysickle folder. Use _pys.py to create a drag and drop application.

The parsed information can be accessed as an attribute - .pysickleData.

## Structure:
  * Game
    * frames [ ]
    * teams [ ]
      * teamID
      * typeName
      * colour 'orange'/'blue'
      * players [ ]
    * players [ ]
      * team 
      * carIDs {frameNo:ID}
      * positions [ ]
      * velocities {frameNo:velocity}
      * properties
      * hits [ ]    * REMOVED. (All removed moved to PyroPlane)
    * ball
      * positions [ ]
      * velocities [ ]
      * game
    * goals
      * player (goalscorer)
      * frameNo
      * firstHit (frame number of first hit.)    * REMOVED.
    * hits   * REMOVED.
      * frameNo
      * player
      * velocity (ball)
      * position (ball)
      * carPosition
      * distance 
