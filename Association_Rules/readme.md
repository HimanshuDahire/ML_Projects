# Association_Rules_using_Python

## Definition and Objective

Definition:
```
  Also called as Market Basket Analysis or Affinity Analysis or Relationship mining.
```

Objective:
```
  Learn the pattern to take best business decision.
```
         
How can Association Rules be used ?
```
  1. Promotion on one item, raise price of related item
  2. Placement in Store
  3. Stocking
  4. Product bundling
```
Rule Form
```
Antecedent ---> Consequent [support,confidence, lift...]
```

## Apriori Algorithm for Association Rules
```
  For K products,
  1. Set min support criteria
  2. Generalize list of 1-item sets that meet support criteria
  3. Use list of 1-item sets to generate list of 2-item sets that meet support criteria
  4. Use list of 2-item sets to generate list of 3-item sets that meet support criteria
  5.continue up to K-item sets
```

## How to clean these rules ?
```
  - We also get duplicate or repeated rules, such rules can be cleaned
  - We check for lift ratio, if having more lift ratio we keep that and discard other one
```

### Data Used:
```Groceries, Book```
    
### Programming:
```Python```

The Codes regarding this Association Rules with its datasets Groceries, Book are present in this Repository in detail

The folder also has deployment part separately in another python file.
