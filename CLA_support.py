import sys
import operator
import math
import time
#from numpy import *
import numpy

def replacing_nan_with_zero(connection_matrix):
	matrx=connection_matrix+(connection_matrix*0)
	#PYTHON DOESNT HAVE PASS BY VALUE, AND I DONT WANT IT TO MODULATTE CONNECTION MATRIX BY REPLACING NAN. 
	#THIS NEW MATRX IS RETURNED AND IS STORED IN CONNECTION_MATRIX_ZERO
	for i in range(0,matrx.shape[0]):
		for j in range(0,matrx.shape[1]):
			if numpy.isnan(matrx[i,j]):
				matrx[i,j]=0
				
	return matrx
	
def top_bit(vect_in,num):
# this function returns a vector with top "num" number 
#of bits in a vector "vect" KEPT ON and others are turned 0
	vect=vect_in+(vect_in*0)
	#CREATED A NEW OBJECT SO THAT THE PASSED ORIGINAL VECTOR IS UNCHANGED
	temp= vect*0
	"""print(vect)
	raw_input('\n this is the vector to select top bits\n')
	print (num)
	raw_input('\n number of counts \n')
	print (temp)
	raw_input('\n temporary zero vector to store\n')
	"""
	for count in range(0,num):
	# [num-1] IS THE TOTAL NUMBER OF TIMES THIS LOOP WILL EXECUTE
		index_to_change=numpy.argmax(vect)
		temp[index_to_change]=vect[index_to_change]
		vect[index_to_change]=0
		
		#print (temp)
		#print( vect)
		#raw_input('\nmodified after 1st count\n')
		
	return temp
			
def next_prediction(history_matrix,m,n,synapse_matrix):
	# RETURNS A "MATRIX" (it may have more than required columns active)
	#OF NEXT PREDICTION.
	trial2=history_matrix*0
	#print (trial2)
	#raw_input(' \n\ntrial2 defined \n\n')
	#print (history_matrix)
	#raw_input(' \n\nHistory matrix \n\n')
	for i in range(0,m*n):
		if history_matrix.flat[i]>0:
			#print (trial2)
			#raw_input(' \n\ntrial2 being assigned\n\n')
			trial2=trial2+synapse_matrix[i,:,:]
	
	for col in range(0,n):
		#print (trial2)
		#raw_input(' \n\ntrial2 being assigned\n\n')
		trial2[:,col]=top_bit(trial2[:,col],1)
		
		
	return trial2
	
def matrix_to_vector(mat):
	#RETURNS A VECTOR WHOSE BITS ARE MAX VALUE EVERY COLUMN IN THAT MATRIX
	number_col=mat.shape[1]
	k=numpy.zeros(number_col)
	for i in range(0,number_col):
		k[i]=numpy.amax(mat[:,i])
	return k
	
	
	
def vector_to_matrix(vect,mat,n):
	# IT SUBSTITUTE ON BITS FROM VECTOR TO THEIR CORRESPONDING LOCATIONS IN 
	# THE MATRIX [BY PARSING THE MATRIX] !!
	output_matrix=mat*0
	for i in range(0,n):
		if vect[i]!=0:
			index=numpy.argmax(mat[:,i])
			max_val=numpy.amax(mat[:,i])
			#mat[:,i]=0
			output_matrix[index,i]=max_val
		
	return output_matrix
	
	
	
def memory_matrix_using_coloutput_predictionmat(output_of_columns,prediction_vector,prediction_matrix,m,n):
	#IT TAKES COLUMN OUTPUT AND IF THERE IS A PREDICTIVE CELL IN THAT COLUMN
	#SEEN THROUGH PREDICTION MATRIX, IT GETS ACTIVATED ELSE A RANDOM CELL IN THAT
	#COLUMN IS ACTIVATED
	memory_matrix2=prediction_matrix*0
	for i in range(0,n):
		if output_of_columns[i]>0:
			if prediction_vector[i]>0:
				memory_matrix2[numpy.argmax(prediction_matrix[:,i]),i]=1
			else:
				memory_matrix2[numpy.random.randint(0,m),i]=1
				
	return memory_matrix2			
				
				
				
def strengthening_synapse(synapse_matrix,history_matrix,memory_matrix,m,n,prediction_matrix):
	#IT FORMS CONNECTIONS BETWEEN ON CELLS FROM HISTORY AND MEMORY MATRIX IN SYNAPSE MATRIX
	#IF PREDICTION GOES RIGHT i:e: IF PREDICTED CELL AND OUTPUT OF COL PREDICTS SAME COLUMN 
	#THAN THAT CELL NEEDS TO BE REINFORCED A LOT. COZ ITS DOING RIGHT. BUT CONECTIONS FROM
	#PREVIOUS CELLS TO THIS PREDICTED CELL SHOULD BE STRENGTHENED, SO NEXT TIME THEY PREDICT THE 
	#SAME. THIS PREDICTED CELL SHOULD NOT PREDICT THOSE HISTORY CELLS .SO THRESHOLD INCREASS IS 
	#APPLIED ONLY TO HISTROY MATRIX CELL !!
	for i in xrange(0,(m*n)):
		if history_matrix.flat[i]>0:
			temp=synapse_matrix[i,:,:]
			threshold=1
			for j in xrange(0,(m*n)):
				if memory_matrix.flat[j]>0:
					if i!=j:
						
						temp2=synapse_matrix[j,:,:]
						
						if prediction_matrix.flat[j]>0: #this means that prediction was correct. 
							#that cell is activated in memory matrix.reinforce it strongly
							threshold=10
						else:
							threshold=1
							#awesome !!
								
						
						
						if temp.flat[j] <=threshold:
							temp.flat[j]=temp.flat[j]+0.2
						#if temp2.flat[i]<=1:
							#temp2.flat[i]=temp2.flat[i]+0.2
						synapse_matrix[i,:,:]=temp
						synapse_matrix[j,:,:]=temp2
						#print synapse_matrix[i,:,:]
						#raw_input('\n\n synapse mat \n\n')
	return synapse_matrix
	
	
def strengthening_connection_matrix(output_of_columns,connection_matrix,n,input_vector,number_of_input,prediction_vector):
#IT STRENGTHENS CONNECTIONS BETWEEN ACTIVE COLUMNS AND ACTIVE BITS
#THESE CONNECTIONS ARE STORED IN CONNECTION MATRIX
	for i in xrange(0,n):
		threshold_1=1
		if output_of_columns[i]>0:
			#print (connection_matrix[i,:])
			#raw_input('\connection_matrix one row before changing!!\n')
			
			
			if prediction_vector[i]>0:# THIS SHOWS PREDICTED COLUMN BECAME ACTIVE THROUGH FEEDFORWARD INPUT
				#PREDICTION MATCHES OUTPUT !! YAY. strengthen it  a lot !!
				threshold_1=10
			else:
				threshold_1=1
			for col in range(0,input_vector.shape[1]):
				#print input_vector.shape[1]
				if connection_matrix[i,col]<=threshold_1:
					#print i
					#print col
					#print connection_matrix[i,col]
					#print (input_vector[number_of_input,col])
					#raw_input('\n\n problem \n\n')
					connection_matrix[i,col]=(input_vector[number_of_input,col]/float(1))+connection_matrix[i,col]
			
	#print (connection_matrix)
	#raw_input('\n\nconnection_matrix \n')
			
	return connection_matrix
	
	
def reconstruction(memory_matrix,connection_matrix,n):
	#IT BUILDS THE INPUT IN SAME SEQUENCE AGAIN
	trial= (connection_matrix[0,:]*0)+(connection_matrix[0,:]*0)
	#print(connection_matrix.size)
	#raw_input('\n size')
	for i in xrange(0,n):
		if numpy.amax(memory_matrix[:,i])>0:
			trial=trial+connection_matrix[i,:]
			#print(trial)
			#raw_input('\n trial')
			
	return trial
			
	
	
	
