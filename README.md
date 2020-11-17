# Pyramid Solitaire
> A program based on a variation of the card game, solitaire.

<!-- TABLE OF CONTENTS -->
## Table of Contents
* [Screenshots](#screenshots)
* [How To Play](#how-to-play)
* [Installation](#installation)
* [Built with](#built-with)


<!-- Screenshots -->
## Screenshots

### Gameplay demo:
![Pyramid Solitaire Gameplay Demo](https://user-images.githubusercontent.com/44094740/98440811-d6a14600-20f2-11eb-9559-9411dc4283c9.gif)

### Start animation:
![Pyramid Solitaire Animation Demo](https://user-images.githubusercontent.com/44094740/98865468-54eb4880-2463-11eb-8094-09e59862ab28.gif)


<!-- Usage -->
## How To Play
This game is played with a standard deck of 52 playing cards. The aim is to remove as many cards from play until no further moves can be made. Each discarded card scores 1 point. Cards must be paired with other cards so that their combined face value is equal to 13. As kings have a face value of 13, they do not need to be paired with another card. Cards in the pyramid can be paired together but only uncovered cards can be selected. Any card covering another card in the pyramid must be removed before the card underneath is made selectable. Cards can be selected by clicking on them. If no pairs can be made within the pyramid, a stack of cards can be cycled through to uncover other cards for pairing. Clicking on the stack will reveal the card on top, thus making it available for selection. The stack can be cycled through as many times as needed.
N.B.: Pressing the space bar will start a new game.

Possible card pairings are listed below:
* Ace and Queen
* 2 and Jack
* 3 and 10
* 4 and 9
* 5 and 8
* 6 and 7


<!-- How to install the program -->
## Installation
To install the app, double click the zip file, save it and then extract the files before running. 
Note that the 'data' file must be kept in the same folder as the executable for the executable to run.

[Pyramid Solitaire.zip](https://github.com/Jamnic98/scrabble-scorekeeper/files/5553422/Pyramid.Solitaire.zip)


<!-- Technologies used in development -->
## Built with
* Python 3.8
* Pygame 1.9.6
