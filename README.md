# Genetic Programming Learning in Multi-agent Economic Competition

## Authors

Chen, S. H., & Yeh, C. H. (1996). Genetic programming learning and the cobweb model. Advances in genetic programming, 2, 443-466.

Koza, J. R., & Koza, J. R. (1992). Genetic programming: on the programming of computers by means of natural selection (Vol. 1). MIT press.

Steve Vu

## 1. Introduction

Extending my previous work in multi-agent economic competitions, the project generalizes the learning of economic agents in the Cobweb model, Jasmina Arifovic (1994), by applying the genetic programming (GP), developed by Koza (1992). By the end of the day, GP-based learning agents can also learn the equilibrium price, even under more unstable case with the cobweb ratio of 3. Furthermore, GP requires less prior knowledge then Genetic Algorithm (GAs) as solutions are expressed by parse trees, and the search space is very large.

In practice, GP is being used increasingly in economic modelling and function approximation in multi-agent systems.

## 2. The Cobweb model

Information about the Cobweb model is available [here](https://github.com/SteveVu2212/Evolutionary-Learning-in-Multi-agent-Economic-Competition). In the project, there are two highlights related to the Cobweb model.

Firstly, in a competitive market, a strategy of a firm/agent represents its expectation of price, instead of quantity. The price expectation will determine how much the firm will produce and supply in a period. Once the aggregate supply of the goods are determined, firms/agents are able to see the market clearing price and calculate their own profits based on their submitted strategies.

Secondly, the project considers a very unstable case with Cobweb ratio of 3. The Cobweb ratio is a division of B parameter by y parameter. According to *Ezekiel's cobweb theorem*, the market price will converge to its equilibrium value if the ratio is less than 1. Intuitively, B parameter is the slope of the demand curve which measures the sensitivity of the price with respect to quantity supplied. When the ratio is greater than 1, it works as an amplifier which amplifies any mistakes made by firms and makes the coordination of price expectations more difficult. However, even in the unstable case, the convergence result is observed in the market composed of GP-based learning agents. That supports to the famous **Hayek Hypothesis** that market has a mechanism to coordinate firms' beliefs to correctly forecast the price.

## 3. The multi-agent genetic programming (MAGP)

The main difference between GAs and GP is that the latter represents its chromosomes/strategies by parse trees written over the *function set* and *terminal set*. Terminals are variables and constants while functions are operations.

|Parameters|Values|
|---------|:----:|
|Number of firms|50|
|Population size|150|
|Number of trees created by **full** method|80|
|Number of trees created by **growth** method|80|
|Function set|{+ ,- ,x ,% ,Log ,Sin ,Cos}|
|Terminal set|{R, Prices lagged upto 10 periods}|
|Probability of crossover|0.9|
|Probability of mutation|0.033|
|Number of generations|100|
|A parameter|4.48|
|B parameter|0.048|
|x parameter|0|
|y parameter|0.016|

*Note:* 
* R is an ephemeral random floating-point constant ranging over the interval [-9.99, 9.99].
* % is the protected division function.

The project uses a widely used method of *Ramped half-and-half* to initialize the population. The method is a combination of the **full** and **growth** methods which ensure that parse trees do not exceed a specified maximum depth. The depth of a node is the number of edges that need to be traversed to reach the node starting from the tree's root node. While the **full** method generates trees where all the leaves are at the same depth, the **growth** method allows for the creation of trees of more varied sizes and shapes.

Below is an example of a strategy. That represents the function mapping previous prices into an expectation of price in a period.

![](https://github.com/SteveVu2212/Genetic-Programming-Learning-in-Multi-agent-Economic-Competition/blob/main/images/strategy_representation.png)

The forecasting function is explicitly written as:

![](https://github.com/SteveVu2212/Genetic-Programming-Learning-in-Multi-agent-Economic-Competition/blob/main/images/forecast%20functions.png)

## 4. Results

The price patterns of GP-based markets have a tendency towards the rational expectations equilibrium (REE) of 1.12. There is also a self-stabilizing feature bringing back every deviation from the equilibrium in the market. Lastly, under perfect competition, all kinds of sophisticated strategic behavior will eventually be useless because the price in the rational expectations equilibrium will not fluctuate very much.

![](https://github.com/SteveVu2212/Genetic-Programming-Learning-in-Multi-agent-Economic-Competition/blob/main/images/equilibrium_price.png)


