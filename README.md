# Genetic Programming Learning in Multi-agent Economic Competition

## Authors

Chen, S. H., & Yeh, C. H. (1996). Genetic programming learning and the cobweb model. Advances in genetic programming, 2, 443-466.

Koza, J. R., & Koza, J. R. (1992). Genetic programming: on the programming of computers by means of natural selection (Vol. 1). MIT press.

Steve Vu

## 1. Introduction

Extending my previous work in multi-agent economic competitions, the project generalizes the learning of economic agenst in the Cobweb model, Jasmina Arifovic (1994), by applying the genetic programming (GP), developed by Koza (1992). By the end of the day, GP-based learning agents can also learn the equilibrium price, even under more unstable case with the cobweb ratio of 3. Furthermore, GP requires less prior knowledge then Genetic Algorithm (GAs) as solutions are expressed by parse trees, and the search space is very large.

In practice, GP is being used increasingly in economic modelling and function approximation in multi-agent systems.

## 2. The Cobweb model

Information about the Cobweb model is available [here](https://github.com/SteveVu2212/Evolutionary-Learning-in-Multi-agent-Economic-Competition). In the project, there are two highlights related to the Cobweb model.

Firstly, in a competitive market, a strategy of a firm/agent represents its expectation of price, instead of quantity. The price expectation will determine how much the firm will produce and supply in a period. Once the aggregate supply of the goods are determined, firms/agents are able to see the market clearning price and calculate their own profits based on their submitted strategies.

Secondly, the project considers a very unstable case with Cobweb ratio of 3. The Cobweb ratio is a division of B parameter by y parameter. According to *Ezekiel's cobweb theorem*, the market price will converge to its equilibrium value if the ratio is less than 1. Intuitively, B parameter is the slope of the demand curve which measures the sensitivity of the price with respect to quantity supplied. When the ratio is greater than 1, it works as an amplifier which amplifies any mistakes made by firms and makes the coordination of price expectations more difficult. However, even in the unstable case, the convergence result is observed in the market composed of GP-based learning agents. That supports to the famous **Hayek Hypothesis** that market has a mechanism to coordinate firms' beliefs to correctly forecast the price.

## 3. The multi-agent genetic programming (MAGP)

The main difference between GAs and GP is that the latter represents its chromosomes/strategies by parse trees written over the *function set* and *terminal set*. Terminals are variables and constants while functions are operations.

The project uses a widely used method of *Ramped half-and-half* to initialize the population. The method is a combination of the **ful** and **growth** methods which ensure that parse trees do not exceed a specified maximum depth. The depth of a node is the number of edges that need to be traversed to reach the node starting from the tree's root node. While the **full** method generates trees where all the leaves are at the same depth, the **growth** method allows for the creation of trees of more varied sizes and shapes.

![](https://github.com/SteveVu2212/Genetic-Programming-Learning-in-Multi-agent-Economic-Competition/blob/main/images/strategy_representation.png)

## 4. Results

![](https://github.com/SteveVu2212/Genetic-Programming-Learning-in-Multi-agent-Economic-Competition/blob/main/images/equilibrium_price.png)


