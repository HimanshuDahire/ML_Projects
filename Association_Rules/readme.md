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
## Support, Confidence and Lift

Support:
```
  Apriori Algorithm defines rules based on "Support" as measurement metric.
  It is a criteria based on frequency, this doesn't represent any associatoin.
```
Confidence:
```
  To cover Support drawback, "Confidence" metric is introduces.
  It tells conditional probablity of occurance of consequent given that antecent has occured.
  But it can be biased when support for some rule is high.
```
Lift:
```
  Finally "Lift" is used as more robust mrtric to justify the importnace of rule.
  It is the ratio of Confidence to Benchmark Confidence (Confidence with indepent probablity of occurance).
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
