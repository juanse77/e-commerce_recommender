Example
=======

In this section we show how to use the library. You can either call the program directly from the package, 
so that the main function will be called, or importing the modules inside the python interpreter. In any case 
you must have placed the train.csv and test.csv files in the data directory. If you don't have these files or 
you have lost them, you can generated again from the original datasets calling the program with the subcommand 'init'.
You can find the original datasets in https://www.kaggle.com/datasets/dschettler8845/recsys-2020-ecommerce-dataset.

.. code-block:: shell
    # Recreates the CSVs file from the original datasets
    python e_commerce init

    # Launches the program
    python e_commerce

    # If you have test.csv file you can calculate the estimation of the efficiency of the program calling
    python e_commerce score

The result of the program consists in one file in binary pickle that contains a matrix with one list 
of recommended product codes for each client.