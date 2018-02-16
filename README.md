# Roulette

### Usage:

*python roulette.py -s <int> -l <int> -r <int>*


**Roulette** takes three arguments:

- `-s` - `--stake` - (int) - Representing the Player's initial stake
- `-l` - `--limit` - (int) - The table limit
- `-r` - `--rounds` - (int) - Number of rounds to conduct

# Example Usage and Output:

```
python roulette.py -s 26000 -l 26000

Starting Stake: (26000) - Rounds: (100) - Table Limit: (26000)

-Martingale's-
Maxima Average: [ 159.720000 ]
Maxima Standard Deviation: [ 47.675587 ]
Duration Average: [ 142.620000 ]
Duration Standard Deviation: [ 96.387736 ]

Maxima:  [186, 223, 227, 129, 119, 132, 129, 137, 211, 105, 227, 161, 219, 121, 116, 233, 241, 120, 190, 105, 103, 223, 104, 230, 214, 111, 105, 108, 181, 209, 126, 105, 184, 121, 127, 179, 218, 129, 216, 120, 107, 135, 133, 205, 228, 99, 176, 102, 192, 165]


Duration:  [194, 250, 250, 73, 55, 104, 59, 185, 250, 15, 250, 162, 250, 54, 38, 250, 250, 41, 186, 13, 83, 250, 75, 250, 250, 39, 16, 24, 185, 250, 60, 14, 250, 52, 60, 250, 250, 72, 250, 40, 26, 190, 84, 250, 250, 7, 182, 16, 250, 227]


-SevenReds's-
Maxima Average: [ 100.240000 ]
Maxima Standard Deviation: [ 0.471593 ]
Duration Average: [ 250.000000 ]
Duration Standard Deviation: [ 0.000000 ]

Maxima:  [100, 100, 100, 100, 101, 101, 100, 100, 100, 100, 100, 100, 100, 101, 100, 100, 100, 100, 100, 100, 100, 100, 101, 102, 101, 100, 100, 100, 100, 101, 100, 100, 100, 101, 101, 100, 100, 100, 101, 100, 100, 101, 100, 100, 100, 100, 100, 100, 100, 100]


Duration:  [250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250, 250]
```
