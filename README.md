# draw-from-pyramid

Draw ages for existing population from a population pyramid.

Context: I have an agent based model of disease transmission which is initialized with a number of living agents. I need to initialize these agents with age according to an existing population pyramid (potentially ignoring sex, potentially considering sex). We will use Vose's algorithm for aliasing to setup for efficient sampling from the population age distribution.

See `pyramid_alias.py` for the code.

See `explore.ipynb` for an example and the result of sampling from the distribution.

-----

**_Note:_** this pseudo-code uses probabilities. The implementation in `pyramid_alias.py` depends on the integer counts in each bin (which, helpfully, avoids floating point accuracy issues).

**Initialization:**

- Create arrays `Alias` and `Prob`, each of size `n`
- Create two worklists, `Small` and `Large`
- Multiply each probability by `n`
- For each scaled probability p<sub>i</sub>
  - If p<sub>i</sub> < 1, add `i` to `Small`
  - Otherwise (p<sub>i</sub> ≥ 1), add `i` to `Large`
- While `Small` is not empty:
  - Remove the first element from `Small`; call it `l`
  - Remove the first element from `Large`; call it `g`
  - Set `Prob[l]` = p<sub>l</sub>
  - Set `Alias[l]` = g
  - Set p<sub>g</sub> = p<sub>g</sub> − (1 − p<sub>l</sub>)
  - If p<sub>g</sub> < 1, add `g` to `Small`
  - Otherwise (p<sub>g</sub> ≥ 1), add `g` to `Large`
- While `Large` is not empty:
  - Remove the first element from `Large`; call it `g`
  - Set `Prob[g]` = 1

**Generation:**

- Generate a fair die roll from an n-sided die; call the side `i`
- Flip a biased coin that comes up heads with probability `Prob[i]`
- If the coin comes up "heads," return `i`
- Otherwise, return `Alias[i]`

----

## Resources

- [Darts, Dice, and Coins](https://www.keithschwarz.com/darts-dice-coins/)
- [A Linear Algorithm for Generating Random Numbers from a Given Distribution](https://www.computer.org/csdl/journal/ts/1991/09/e0972/13rRUxBa5oH)
- [Population Pyramid Data](https://www.populationpyramid.net/)
