# E-commerce recommender

This solution is designed to propose recommendations for an e-commerce business
and is based on collaborative filtering between users. What differentiates 
this solution from others of the same type is that it establishes comparisons 
between users based on the categories of items most consumed by them, instead 
of on the items themselves.

In this way, a matrix of vectors is generated that represents the tastes of 
each client. With this matrix, the angular distance that exists between the vectors 
of each client is calculated.

Next, for each customer, three other customers that are closest in this vector 
space are selected. Finally, each customer will be recommended for the last eight
purchases made by the three 'neighbors' customers. This result will be registered 
in a data structure to be consumed by an online service.

## Installation

This module is available to be installed via pip.

## Example

In this section we show how to use the library. You can either call the program directly from the package, 
so that the main function will be called, or importing the modules inside the python interpreter. In any case 
you must have placed the train.csv and test.csv files in the data directory. If you don't have these files or 
you have lost them, you can generated again from the original datasets calling the program with the subcommand 'init'.
You can find the original datasets in https://www.kaggle.com/datasets/dschettler8845/recsys-2020-ecommerce-dataset.

```python
    # Recreates the CSVs file from the original datasets
    python e_commerce init

    # Launches the program
    python e_commerce

    # If you have test.csv file you can calculate the estimation of the
    #  efficiency of the program calling
    python e_commerce score
```

The result of the program consists in one file in binary pickle that contains a matrix with one list 
of recommended product codes for each client.