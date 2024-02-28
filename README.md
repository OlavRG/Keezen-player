# Keezen-player
Takes a Keezen boardstate and hand as input, and outputs the (sub-)optimal play.

Class hierarchy

	Card 	Att: name, suit, move
			Meth: place_pawn, move_pawn,
			
		Cards:
		Hearts_Ace ()
		Hearts_seven (Meth: move_pawn)
		Hearts_Jack (Meth: move_pawn)
	
	
	Hand (list: cards)
	Discard pile (list: cards)
	Deck (list: card)
	
	Board(att: size
	Home (
	Finish (
	Pawn (att: color, position)
	



To do
	- class hierarchy
	- Read solid