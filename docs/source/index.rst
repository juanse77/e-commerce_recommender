.. E-commerce recommender documentation master file, created by
   sphinx-quickstart on Wed Dec  7 19:32:35 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to E-commerce recommender's documentation!
==================================================

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


.. toctree::
   :maxdepth: 2
   :caption: Contents:
      
   install
   example

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
