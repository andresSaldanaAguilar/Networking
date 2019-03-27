import rrdtool

def createRDD(filename,samplingType): 
	ret = rrdtool.create(filename+".rrd",
						"--start",'N',
						"--step",'10',
						"DS:in:"+samplingType+":600:U:U",
						#archivos recolectados
						"RRA:AVERAGE:0.5:1:600",
						#RRA:HWPREDICT:rows:alpha:beta:seasonal period[:rra - num]
						#archivos esperados, predecidos
						"RRA:HWPREDICT:11:0.1:0.0035:5:3",
						#RRA:SEASONAL:seasonal period:gamma:rra-num
						#coeficiente estacional, el primer numero debe ser igual al penultimo anterior
						#entre menor, actuales, entre mayor, mas viejos
						#estamos relacionando a hw con seasonal con el indice 2
						"RRA:SEASONAL:5:0.1:2",

						#los valores deben empatar con los anteriores
						#RRA:DEVSEASONAL:seasonal period:gamma:rra-num
						"RRA:DEVSEASONAL:5:0.1:2",
						#debe empatar con hwpredict
						#RRA:DEVPREDICT:rows:rra-num
						"RRA:DEVPREDICT:11:4",
						#si esta dentro, vale cero, si es falla, uno
						#RRA:FAILURES:rows:threshold:window length:rra-num
						"RRA:FAILURES:11:7:9:4")

				#HWPREDICT rra-num is the index of the SEASONAL RRA.
				#SEASONAL rra-num is the index of the HWPREDICT RRA.
				#DEVPREDICT rra-num is the index of the DEVSEASONAL RRA.
				#DEVSEASONAL rra-num is the index of the HWPREDICT RRA.
				#FAILURES rra-num is the index of the DEVSEASONAL RRA.

	
	if ret:
		print (rrdtool.error())


