CLA
===


  
Description of Functions:

  CLA.py is the main file. It calls other functions from CLA_support. I have written lot of comments which should make 
  it easier to understand. uncommenting the print and raw_input commands you will get to see step wise execution of the
  code.
  Even the function names are self explanatory so i will just explain the algorithm here.
  
  1-  Input is defined in the beginning. Its called input_vector but its a matrix though. every row is one input pattern.
      few patterns form a sequence which is then repeated for number_of_repetition times in for loop.
      If u decide on changin the input, do change input size [k] and  number of on bits[d]
      
  2-  Then we define memory matrix which has all cells. connection matrix which has connections from column to the input
      pattern.every row of connection matrix is the connection from one column to every input bit. synapse matrix 
      stores connections between all cells. its a 3 dimensional array. every dimension represents one cells connection to
      all other cells in memory matrix. history matrix stores the previous memory matrix. its used for doing predictions
      from previous patterns.prediction matrix stores predictions.if u give history matrix as input then it will give u 
      current prediction.if u give memory matrix it will give u future prediction.
      
  3-  50% of connections of every column to inputs are set NAN.. so no connection exists.
  
  4-  Now algorithm begins. !! input bits are mulitplied by connection matrix and that is the out put of every column.
      now that its the first output, top few percentage of columns are selected and their random cells are activated in 
      memory matrix. this represents our first input. now next input also gets multiplied by connection matrix.
      now for newly active col, we check prediction from old memory matrix which is stored in history matrix. if any 
      columnar prediction match, the predictive cell is activated in that particular col else a random cell is turned ON.
      Now connections between current active memory cells and past memory cells is strengthen in synapse matrix. Also
      connection between active columns and active input bits is strengthened in connection matrix. 
      
      
      
  
      
      
