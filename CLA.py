
import sys
import operator
import math
import time
#from numpy import *
import numpy
import CLA_support


def main():
	k=7 # size of INPUT VECTOR
	d=2  # NUMBER OF ON BITS IN INPUT VECTOR
	percentage_of_col_active=3
	#input_vector=numpy.matrix([[1,1,0],[0,1,1],[1,0,1],[1,1,0],[0,1,1],[1,0,1]])
	#input_vector=numpy.matrix([[1,1,0,0,0],[0,1,1,0,0],[0,0,1,1,0],[0,0,0,1,1]])
	#input_vector=numpy.matrix([[1,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]])
	input_vector=numpy.matrix([[1,1,0,0,0,0,0],[0,1,1,0,0,0,0],[0,0,1,1,0,0,0],[0,0,0,1,1,0,0]])
	
	#though i have delcared this as a matrix we should use one by one input.
	#single input takes long enough to go through the cla. then we can take another. and loop continues !
	
	number_of_repetition=30
	#NUMBER OF TIMES THE WHOLE INPUT SEQUENCE MATRIX IS PASSED IN CLA
	
	
	m=3 #ROWS OF MEMORY MATRIX
	n=100 # COLUMNS OF MEMORY MATRIX
	
	memory_matrix=numpy.matrix(numpy.zeros((m,n)))
	history_matrix=memory_matrix
	prediction_matrix=memory_matrix
	synapse_matrix=(numpy.zeros((m*n,m,n)))
	# 3 - DIMENSIONAL MATRIX [3rd dim, rows, col ]
	connection_matrix=numpy.random.rand(n,k)
	
	
	# !!!!! INDEXING OF A NUMPY MATRIX STARTS FROM [0,0]
	
	#THIS LOOP SETS THE CONNECTION MATRIX WITH 50% CONNECTIONS AS "NAN" 
	for i in xrange(0,n):
		for count in xrange(0,numpy.int(math.floor(0.5*k))):
			#print numpy.int(math.floor(0.5*k))
			#raw_input('that is the count range')
			#setting 50% of connections from i/p to coloumns to NAN
			while True:
				rand_num=numpy.random.random_integers(0,k-1)
				#print (rand_num)
				#raw_input('random number')
				if (numpy.isnan(connection_matrix[i,rand_num]))== False:
					#if that connection is not already a NAN then set it as NAN and also increase the count, else just continue iterations
					# without increasing the count
					connection_matrix[i,rand_num]=numpy.nan
					#print connection_matrix[i,:]
					#raw_input('about to break the while loop and increase count')
					break
				#else:
					#print ('its already NaN')
	
	#ALGORITHM PROBABLY STARTS HERE !!!!!
	
	for repi in range(0,number_of_repetition):
		print(repi)
		#raw_input('\n number of repetition\n')
	
		for number_of_input in range(0,input_vector.shape[0]):				
	# every input from input_vector is taken in interations ONE AT A TIME
	#WHOLE PROGRAM WIL COME UNDER THIS FOR LOOP 	BECAUSE IT PROVIDES NEXT INPUT IN NEXT ITERATION
	
	
		#print (connection_matrix)
		#raw_input('\nthat was connection matrix')
		#print (input_vector[number_of_input,:].T)
		#raw_input('\nthat was input vector')
			print input_vector[number_of_input,:]
			#raw_input('\n\n\n input \n\n')
			connection_matrix_zero=CLA_support.replacing_nan_with_zero(connection_matrix)
		#THIS REPLACES NAN IN CONNECTION MATRIX WITH "0" . THIS HELPS IN MULTIPLICATIONS
		#print (connection_matrix_zero)
		#raw_input('connection matrix with zeros instead of NAN')
		
			output_of_columns=connection_matrix_zero*(input_vector[number_of_input,:].T)
		#THIS IS A VECTOR, EVERY BIT REPRESENTING OUTPUT OF EVERY COLUMN
		
		#this will keep only "percentage_of_col_active" bit ON IN THE COLUMN VECTOR
			output_of_columns=CLA_support.top_bit(output_of_columns,numpy.int(math.floor((percentage_of_col_active/float(100))*n)))
		
		#CHECKING FOR NEW PREDICTION FROM HISTORY MATRIX WHICH HAS THE PREVIOUS MEMORY MATRIX IN IT
		#if sum(sum(history_matrix)) !=0:
			prediction_matrix=CLA_support.next_prediction(history_matrix,m,n,synapse_matrix)
		#THIS PREDICTION MATRIX HAS MANY ON CELLS PER COLUMN AND MANY COLUMNS ACTIVE
		
		
		#getting vector with max value every column as its bits
			prediction_vector=CLA_support.matrix_to_vector(prediction_matrix)
		
			prediction_vector=CLA_support.top_bit(prediction_vector,numpy.int(math.floor((percentage_of_col_active/float(100))*n)))
		#NOW THIS PREDICTION_VECTOR WILL HAVE ONLY CERTAIN PERCENTAGE OF BITS ACTIVE.
			#print(prediction_vector)
			#raw_input('\n\n\n its the prediction vector \n\n')
		
		
		#SUBSTITUTE ON BITS FROM VECTOR TO THEIR CORRESPONDING LOCATIONS IN 
		#PREDICTION MATRIX !!
			prediction_matrix=CLA_support.vector_to_matrix(prediction_vector,prediction_matrix,n)
			print(prediction_matrix)
			#raw_input('\n\n\n its the prediction matrix \n\n')
		
		
		#IT GIVES MEMORY MATRIX BY ACTIVING THOSE % OF COLUMNS THAT HAVE WON 
		#AND ACTIVATING THOSE CELLS THAT ARE IN PREDICTIVE STATE IN THAT ON COLUMN
		#OR RANDOM CELL 
			print(output_of_columns.T)
			#raw_input('\n\n output of columns \n\n')
			memory_matrix=CLA_support.memory_matrix_using_coloutput_predictionmat(output_of_columns,prediction_vector,prediction_matrix,m,n)
			print(memory_matrix)
			#raw_input('\n\n memory matrix\n\n')
		
		#IT FORMS CONNECTIONS BETWEEN CURRENT ACTIVE CELLS FROM MEMORY MATRIX AND PREVIOUS ACTIVE CELLS FROM HISTORY MATRIX
		#THESE CONNECTIONS ARE IN SYNAPSE MATRIX
			synapse_matrix=CLA_support.strengthening_synapse(synapse_matrix,history_matrix,memory_matrix,m,n,prediction_matrix)
			print synapse_matrix
			#print(sum(sum(synapse_matrix)))
			#raw_input('\n synapse_matrix\n')
		
		#IT STRENGTHENS CONNECTIONS BETWEEN ACTIVE COLUMNS AND ACTIVE BITS .THESE CONNECTIONS ARE STORED IN CONNECTION MATRIX
		#input_vector IS ACTUALLY A MATRIX. HERE ONLY THE CURRENT INPUT BEING PROCESSED IS PASSED !! aWESOME
			connection_matrix=CLA_support.strengthening_connection_matrix(output_of_columns,connection_matrix,n,input_vector,number_of_input,prediction_vector)
		
			#print connection_matrix
			#raw_input('\connection_matrix\n')
		
		#STORING MEMORY MATRIX IN HISTORY MATRIX AND READY FOR NEXT ITERATION !!
			history_matrix=memory_matrix
	
			connection_matrix_zero=CLA_support.replacing_nan_with_zero(connection_matrix)
			output=CLA_support.reconstruction(memory_matrix,connection_matrix_zero,n)
			output=CLA_support.top_bit(output,d)
			raw_input(' \n Doing immediate reconstruction from learned patterns.\n input was\n' )
			print input_vector[number_of_input,:]
			raw_input(' \n output is\n' )
			print (output)
			raw_input(' \n \n' )
	
	
	'''connection_matrix_zero=CLA_support.replacing_nan_with_zero(connection_matrix)
	output=CLA_support.reconstruction(memory_matrix,connection_matrix_zero,n)
	output=CLA_support.top_bit(output,d)
	raw_input(' \n first output is\n' )
	print (output)
	raw_input(' \n output is\n' )
	'''
	while True:
	
		prediction_matrix=CLA_support.next_prediction(memory_matrix,m,n,synapse_matrix)
		#THIS PREDICTION MATRIX HAS MANY ON CELLS PER COLUMN AND MANY COLUMNS ACTIVE
		
		print(memory_matrix)
		raw_input('\n\n memory matrix \n\n')
		
		#getting vector with max value every column as its bits
		prediction_vector=CLA_support.matrix_to_vector(prediction_matrix)
		
		prediction_vector=CLA_support.top_bit(prediction_vector,numpy.int(math.floor((percentage_of_col_active/float(100))*n)))
		#NOW THIS PREDICTION_VECTOR WILL HAVE ONLY CERTAIN PERCENTAGE OF BITS ACTIVE.
		#print(prediction_vector)
			#raw_input('\n\nits the prediction vector \n\n')
		
		
		#SUBSTITUTE ON BITS FROM VECTOR TO THEIR CORRESPONDING LOCATIONS IN 
		#PREDICTION MATRIX !!
		prediction_matrix=CLA_support.vector_to_matrix(prediction_vector,prediction_matrix,n)
		
		print(prediction_matrix)
		raw_input('\n\n prediction matrix \n\n')
	
		output=CLA_support.reconstruction(prediction_matrix,connection_matrix_zero,n)
		output=CLA_support.top_bit(output,d)
		memory_matrix=prediction_matrix
		raw_input(' \n output is\n' )
		print (output)
		raw_input(' \n get on the train baby\n' )


if __name__ == '__main__':
  main()
