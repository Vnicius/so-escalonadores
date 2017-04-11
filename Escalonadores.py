#!/usr/bin/python
#-*- coding: utf-8-*-

import copy

#[Entrada, Tempo de execução, Tempo de Retorno, Tempo de Resposta, Tempo de Espera]

def fcfs(fila):
	procs = copy.deepcopy(fila) #Copia a fila de entrada
	#Variáveis auxíliares
	entrada = texec = tCPU = 0
	ret = res = esp = 0

	for proc in procs:
		entrada = proc[0]	#Tempo de entrada do processo atual
		texec = proc[1]		#Tempo de execução do processo atual

		if entrada >= tCPU:		#Se o tempo da entrada for maior ou igual ao tempo atual da CPU, então o processo é logo executado, sem espera
			tCPU += (entrada - tCPU) + texec	#O novo tempo da CPU será a diferença entre a entrada o processo atual mais o seu tempo de execução
			proc[2] = texec		#O tempo de retorno do processo será o seu tempo de execução
		else:
			espera = tCPU - entrada		#Calcular tempo de espera do processo
			proc[2] = espera + texec	#O tempo de resposta será a soma dos tempos de espera e execução
			proc[3] = espera	#O tempo de resposta será o próprio tempo de espera
			proc[4] = espera	#Atribuição do tempo de espera
			tCPU += texec		#O tempo da CPU é somado com o tempo de execução do processo

	#A soma dos tempos poderia ser feita no for anterior, mas vou deixar aqui para facilitar a visualização
	for proc in procs:
		ret += proc[2]
		res += proc[3]
		esp += proc[4]

	tam = float(len(procs))

	print("FCFS "+str(ret/tam)+" "+str(res/tam)+" "+str(esp/tam))

###############################

def sjf(fila):
	procs = copy.deepcopy(fila)

	entrada = texec = tCPU = 0
	ret = res = esp = 0
	swap = True
	j = 0
	tam = len(procs)

	for i in range(tam):
		swap = True
		j = i
		#Ordena pelo tempo de execução todos os processos que estão naquele momento (entrada <= tCPU) na fila
		while swap or j < tam-1:
			swap = False
			if j < tam-1:
				if (procs[j][0] <= tCPU) and (procs[j+1][0] <= tCPU) and (procs[j][1] > procs[j+1][1]):
					aux = procs[j]
					procs[j] = procs[j+1]
					procs[j+1] = aux
					swap = True
					j = i
				else:
					j += 1

		entrada = procs[i][0]
		texec = procs[i][1]

		#Processo igual o FCFS
		if procs[i][0] >= tCPU:
			tCPU += (entrada - tCPU) + texec
			procs[i][2] = texec
		else:
			espera = tCPU - entrada
			procs[i][2] = espera + texec
			procs[i][3] = espera
			procs[i][4] = espera
			tCPU += texec

	for proc in procs:
		ret += proc[2]
		res += proc[3]
		esp += proc[4]

	tam = float(tam)

	print("SJF "+str(ret/tam)+" "+str(res/tam)+" "+str(esp/tam))

##################################

def rr(fila, quantum = 2):
	ret = res = esp = tCPU = 0
	entrada = texec = i = 0
	procs = copy.deepcopy(fila)
	tam = len(procs)

	while i < tam:
		entrada = procs[i][0]
		texec = procs[i][1]

		if entrada >= tCPU: #Vê se o processo entrou durante ou depois do tempo atual da CPU
			if (texec - quantum) <= 0:		#Caso o processo execute totalmente
				procs[i][2] += texec
				procs[i][3] = -1 if tCPU == 0 else procs[i][3]	#Usado para eliminar o primero processo da soma dos tempo de resposta
				tCPU += (entrada - tCPU) + texec
				i += 1
			else:		#Caso o processo executer parcialmente
				procs[i][3] = -1 if tCPU == 0 else procs[i][3]
				tCPU += (entrada - tCPU) + quantum		#Usado para eliminar o primero processo da soma dos tempo de resposta
				procs[i][0] = tCPU		#Atualiza o tempo de entrada do processo
				procs[i][1] -= quantum	#Subtrai o tempo que o processo executou
				procs[i][2] += quantum	#Incrementa o tempo de retorno

				#Coloca no fim da fila dos processos atuais o processo que executou pacialmente
				for j in range(i, tam-1):
					if (procs[j][0] <= tCPU) and (procs[j+1][0] <= tCPU):
						aux = procs[j]
						procs[j] = procs[j+1]
						procs[j+1] = aux
					else:
						break
		else:		#Caso o processo entre antes do tempo atual da CPU
			if (texec - quantum) <= 0:	#Caso executou totalmente
				espera = tCPU - entrada
				procs[i][2] += espera + texec	#Incrementa o tempo de retorno
				procs[i][3] = espera if (procs[i][3] == 0) and (procs[i][3] != -1)  else procs[i][3] #Usado para não alterar o tempo de resposta
				procs[i][4] += espera		#Incrementa o tempo de espera
				tCPU += texec
				i += 1
			else:
				espera = tCPU - entrada
				procs[i][2] += espera + quantum		#Incrementa o tempo de retorno
				procs[i][3] = espera if (procs[i][3] == 0) and (procs[i][3] != -1) else procs[i][3]	#Usado para não alterar o tempo de resposta
				procs[i][4] += espera		#Incrementa o tempo de espera
				tCPU += quantum
				procs[i][0] = tCPU
				procs[i][1] -= quantum

				#Coloca no fim da fila dos processos atuais o processo que executou pacialmente
				for j in range(i, tam-1):
					if (procs[j][0] <= tCPU) and (procs[j+1][0] <= tCPU):
						aux = procs[j]
						procs[j] = procs[j+1]
						procs[j+1] = aux
					else:
						break
		#print (str(i)+" "+str(tCPU))
		#print (procs)
	for proc in procs:
		ret += proc[2]
		if proc[3] != -1:
			res += proc[3]
		esp += proc[4]

	tam = float(tam)

	print("RR "+str(ret/tam)+" "+str(res/tam)+" "+str(esp/tam))
