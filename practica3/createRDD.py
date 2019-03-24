import rrdtool

def createRDD(filename,samplingType): 
	ret = rrdtool.create(filename+".rrd",
							"--start",'N',
		                    "--step",'3',
		                    "DS:in:"+samplingType+":30:U:U",
				              #archivos recolectados
				                     "RRA:AVERAGE:0.5:1:100",
				              #RRA:HWPREDICT:rows:alpha:beta:seasonal period[:rra - num]
				              #archivos esperados, predecidos
				                     "RRA:HWPREDICT:60:0.5:0.0035:10:3",
				              #RRA:SEASONAL:seasonal period:gamma:rra-num
				              #coeficiente estacional, el primer numero debe ser igual al penultimo anterior
				              #entre menor, actuales, entre mayor, mas viejos
				              #estamos relacionando a hw con seasonal con el indice 2
				                     "RRA:SEASONAL:10:0.5:2",

				              #los valores deben empatar con los anteriores
				              #RRA:DEVSEASONAL:seasonal period:gamma:rra-num
				                     "RRA:DEVSEASONAL:10:0.5:2",
				              #debe empatar con hwpredict
				              #RRA:DEVPREDICT:rows:rra-num
				                     "RRA:DEVPREDICT:60:4",
				              #si esta dentro, vale cero, si es falla, uno
				              #RRA:FAILURES:rows:threshold:window length:rra-num
				                     "RRA:FAILURES:60:7:9:4")

				#HWPREDICT rra-num is the index of the SEASONAL RRA.
				#SEASONAL rra-num is the index of the HWPREDICT RRA.
				#DEVPREDICT rra-num is the index of the DEVSEASONAL RRA.
				#DEVSEASONAL rra-num is the index of the HWPREDICT RRA.
				#FAILURES rra-num is the index of the DEVSEASONAL RRA.

	
	if ret:
		print (rrdtool.error())


