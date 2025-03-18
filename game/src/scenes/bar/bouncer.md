# pseudo code for bouncer AI logic:

1. Basic Movement (No Pathfinding)
 Make the bouncer move in a straight line toward the player.
 Limit movement speed to prevent instant travel.
 Prevent the bouncer from moving off-screen.

directions = [(1,0), (0,1), (-1,0), (0,-1), (1,1), (-1,-1), (1,-1), ]
direction keys = up, down, left, right, diagonal up left, diagonal 

bouncer class
    bouncer.constructor
    bouncer.sprite
    bouncer.placement
    bouncer.can_move (true/false)
    bouncer.speed

    def can_move
        can_move = False
    
    def 



player class

grid class
