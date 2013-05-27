Drinker
=======

This is the main repository for a distributed, open-source drinking game. All necessary assets to create the game for yourself
are provided here.

The repository is built as follows:

<pre>
root	       	  	       The root directory, contains this README file and the gitignore file
|-- Cards		             This directory contains all the data needed to generate the cards
|    |-- Descriptions	   This directory contains the different translations of the text on the cards
|    |   |-- en		       The english version of the text on the cards
|    |   |-- nl
|    |   +-- ...
|    |
|    |-- Images		       This directory contains all the images used in the cards
|    +-- Templates	     This directory contains the card templates and the back of the cards
|
+-- Generator		         This directory contains the python code for generating the finished cards in printable format
</pre>
