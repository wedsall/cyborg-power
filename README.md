# cyborg-power
Author
  W. Edsall (wedsall@gmail.com)

DESCRIPTION
  The rules for this model are based on a game in which there is a 'Cyborg' class. The Cyborg class has a power system based on a series of implants which are installed into the Cyborg's body to provide more power to other systems such as weapons, etc.

RULES
  There are a few rules which this model is built on.

  1. The % of SI control (the player's Cyborg level) available to power 
     systems is 25% per level. I.e. level 10 grants 2.5 control for power
     systems. The sum of all power implants control requirement cannot
     exceed this threshold.
  2. Each point of power regeneration requires 50 points of total power.

ASSUMPTIONS
  
  1. We always use the efficiency coprocessor at level 25 and up.
     It doesn't play into this power calculator but it provides
     benefits for other systems, so we always include it.

OBJECTIVE

  Our main objective is to determine the maximum power regeneration at any of the 1-100 Cyborg levels.

FUTURE GOALS

  I would like to..

  1. Figure out why this runs so slowly. I can't solve this on say 50 levels at a time - it runs forever. Is it possible to optimize further?
  2. When using the IPOPT solver I'm getting continuous results but it's not possible to have a non-integer number of implants. Not sure why this is happening but my hope was IPOPT would run better than the other solvers.
  3. Also optimize on the rate of change between levels. For example we wouldn't want to drop all implants and completely redo our implants between levels. It would be better to make smaller changes to the total implants.

For feedback please email me: wedsall@gmail.com
