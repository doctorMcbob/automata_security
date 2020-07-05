# automata_security
Using cellular atomation for security!

Just a proof of concept, could be re-wired for real implementation, but very slow when faster one way functions exist

## The cellular automata 
you can play with a javascript implementation on my website at http://www.wesleyscoolsite.com/automata

it works like this, 

the "Rule" is a random number between 0 and 2**256, converted to binary

each 'cell' in the automata has 8 neighbors, each generation those cells are converted to binary

so a cell with neighboring cells like so:
```
0 1 0
1 @ 0
0 0 1
```
would evaluate into binary `01010001` which has an integer value of 81

Taking this value, the 81st bit in our binary "Rule" is refrenced to determen if the cell should be alive in the next generation.

Therefore, rules are unique and running a rule is a one way function

## Security

The "Rule" is used as the key, when a user is initialized, the key is sent.

When a connection starts, a grid is generated, converted to an int and sent, and then the key rule is applied a number of times (default, 50)

If the user responds with the same grid as our rule process concludes with, then the user had the key, and the connection is secure.
