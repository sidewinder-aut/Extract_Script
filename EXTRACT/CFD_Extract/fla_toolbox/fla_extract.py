#!/usr/bin/python
                                                                                                                                                             
import sys, string, os, time, re
from sys import argv
                                                                                                                                                             
nr_arg = len(argv)
if nr_arg != 3:
        print "Syntax:"
        print "./extract_fla.py  <filename.fla>  <extract_log.input>"
        sys.exit()
fla_name = argv[1]
input_name = argv[2]

sheet = "general.txt"

i = 0
rest = 0

fla_line = []
row_nr = []

print "--------------------------------------------------------"

cpu_time = " "
run_mode = " "
host_name = " "
bit_mode = " "
cpu_model = " "

tim_start_writing = 0
start_mpi_time = 0
time_strings = ["ACCIF_EXCHANGE    ", "File IO    ", "Linear Solver    ", "MPI Barrier    ", "MPI Communication    ", "Mesh Movement    ", "Mesh time update    ", "Other    ", "Rezone    ", "Spray    ", "Thermochemistry    ", "Wallfilm    ", "Thin_Walls    ", "Total Execution    ", "Combustion    "]


sheet = "general.txt"
nr_cpu = 1

#tim = open("timings.txt", 'w')
csvtim = []
fla = open(fla_name, 'r')
for line in fla.readlines():
	fla_line.append(line)
	fla_line[i] = line
	i = i + 1
	len_fla = i
	scpu_model = string.rfind(line, '=  CPU  Model     :')
        if scpu_model != -1:
                cpu_model_01 = string.split(line, '=  CPU  Model     :')
                cpu_model_02 = cpu_model_01[1].replace(" ","")
                cpu_model_03 = cpu_model_02.replace("=","")
                cpu_model = str(cpu_model_03)
                #print " CPU Model = ", cpu_model
        sbit_mode = string.rfind(line, '=  Bit Mode       :')
        if sbit_mode != -1:
                bit_mode_01 = string.split(line, '=  Bit Mode       :')
                bit_mode_02 = bit_mode_01[1].replace(" ","")
                bit_mode_03 = bit_mode_02.replace("=","")
                bit_mode = str(bit_mode_03)
                #print " Bit Mode = ", bit_mode
        snr_cpu = string.rfind(line, 'MPI Parallelization                On:')
        if snr_cpu != -1:
                snr_cpu_01 = string.split(line, 'MPI Parallelization                On:')
                snr_cpu_02 = string.split(snr_cpu_01[1])
                nr_cpu = snr_cpu_02[0]
        shost_name  = string.rfind(line, ' =  Host Name      :')
        if shost_name != -1:
                host_name_01 = string.split(line, ' =  Host Name      :')
                host_name_02 = host_name_01[1].replace(" ","")
                host_name_03 = host_name_02.replace("=","")
                host_name = str(host_name_03)
                #print " Host Name = ", host_name
        srun_mode = string.rfind(line, '*   Run Mode ')
        if srun_mode != -1:
                run_mode_01 = string.split(line, '*   Run Mode ')
                run_mode_02 = run_mode_01[1].replace(" ","")
                run_mode_03 = run_mode_02.replace("*","")
                run_mode_04 = run_mode_03.replace("\n","")
                run_mode = str(run_mode_04)
                print " Run Mode = ", run_mode
        scpu_time = string.rfind(line, '*   Total Execution')
        if scpu_time != -1:
                cpu2 = line.replace(" ","")
                cpu3 = string.rfind(cpu2, '%]')
                if cpu3 != -1:
                        cpu4 = string.split(cpu2, '%]')
                        cpu5 = string.split(cpu4[1], '[')
                        cpu6 = string.split(cpu5[0], '.')
                        cpu_time =str(cpu6[0])
                        #print " CPU Time = ", cpu_time
        srestart = string.rfind(line, 'Restart Files are used')
        if srestart != -1:
                rest = 1


        find_calc_time_mpi = string.rfind(line, '*   Total MPI Timings                       Count        Total CPU Time        Average WCT              *')
        find_calc_time_serial = string.rfind(line, '*   RUNTIME ANALYSIS AT END OF CALCULATION                                                              *')
        find_calc_time_end = string.rfind(line, '*   Total Execution     ')
        if find_calc_time_serial != -1 and nr_cpu == 1:
                start_mpi_time = 0
        if find_calc_time_mpi != -1 and nr_cpu != 1:
                start_mpi_time = 1
        if start_mpi_time == 1:
                for ti in range(len(time_strings)):
                        rfi_tim = string.rfind(line, time_strings[ti])
                        if rfi_tim != -1:
                                if nr_cpu == 1:
                                        sp001 = string.split(line, '[')
                                        sp002 = string.split(line, ']')
                                        line = sp001[0] + sp002[1]
                                        #print line
                                if nr_cpu > 1:
                                        find_brack = string.rfind(line, '[')
                                        if find_brack != -1:
                                                continue
                                header_mv = time_strings[ti].replace(' ', '_')
                                spl_tim = string.split(line, time_strings[ti])
                                spl_spl_tim = string.split(spl_tim[1])
                                if tim_start_writing == 0:
                                        tsout = header_mv + "\t" + spl_spl_tim[2]
                                        csvout = time_strings[ti] + "," + spl_spl_tim[2]
                                        tim_start_writing = 1
                                else:
                                        tsout = "\n" + header_mv + "\t" + spl_spl_tim[2]
                                        csvout = "\n" + time_strings[ti] + "," + spl_spl_tim[2]
                                #print tsout
                                #tim.write(tsout)
                                csvtim.append(csvout)
        #if start_mpi_time == 1 and find_calc_time_end != -1:
        #        start_mpi_time = 0
        if line.startswith("Process: "):
                start_mpi_time = 0

        acc_iter_find = string.rfind(line,'Accumulated Sum of Iterations =')
        if acc_iter_find != -1:
                spl_acc_iter_find = string.split(line, 'Accumulated Sum of Iterations =')
                spl_spl_acc_iter_find = string.split(spl_acc_iter_find[1])
                acc_iter = spl_spl_acc_iter_find[0]

fla.close()
#tim.close()
#csvtim.close()

#sheets = open(sheet, 'w')
#sheets.write(" CPU Model = " + cpu_model)
#sheets.write(" Bit Mode = " + bit_mode)
#sheets.write(" Host Name = " + host_name)
#sheets.write(" Run Mode = " + run_mode)
#if rest == 1:
#	sheets.write("\n Restart Files are used")
#sheets.write("\n Total Calculation Time = " + cpu_time)
#sheets.close()

print len_fla, " lines read in ", fla_name

search_string = []
res_name = []

i = 0
check_xxx = 0

input = open(input_name, 'r')
for line in input.readlines():
	if line.startswith(" "):
		continue
	if line.startswith("#"):
		continue
	if line.startswith("counter"):
		continue
	#print line
	#line = string.strip(line)
	line = line.replace("\n","")
	check_dp = string.rfind(line, ":")
	if check_dp != -1:
		insplit = string.split(line, ':')
		tres_name = insplit[0].replace(" ","")
		res_name.append(tres_name)
		res_name[i] = tres_name
		#print res_name[i]
		row_in = 0
		row_check = string.rfind(res_name[i], '.row_')
		if row_check > 1:
			row_nr_find = string.split(res_name[i], '.row_')
			row_in = int(row_nr_find[1])
		row_nr.append(row_in)
		row_nr[i] = row_in
		#print row_nr[i]
		insplit_string = insplit[0] + ":"
		insplit_dp = string.split(line, insplit_string)
		tsearch_string = insplit_dp[1]
		search_string.append(tsearch_string)
		search_string[i] = tsearch_string
		#print line
		#print res_name[i], " ", search_string[i]
		#print "-------------------------------------------------------"
		i = i + 1
		len_input = i
		#print len_input, ":  ", line
input.close

print len_input, " entries found in ", input_name
print "--------------------------------------------------------"
if rest == 1:
	print "Restart Files are used"
	print "--------------------------------------------------------"
print "\n"

run_mode = run_mode.strip()
if run_mode == 'Crankangle':
	header_string = "    Angle ="
	staedy = 0
if run_mode == 'Timesteps':
	header_string = "Time Step        Time = "
	header_string = "Time Step   Time ="
	staedy = 0
if run_mode == 'Steady':
	staedy = 1

#print run_mode
#print "staedy =", staedy
 
#x = []
#y = []

count_s = 0
start_header = 100000000
end_header = -100000000
nr_header = 0

for i in range(len_input):
	print i+1,"(", len_input, ") Processing ", res_name[i]
	k = 0
	#count_s = 0
	#max_count_s = 0
	x = []
	y = []
	len_res = 0
	xxx = -1
	for j in range(len_fla):
		if staedy == 0:
			find_mode = string.rfind(fla_line[j], header_string)
			if find_mode != -1:
				mode_split = string.split(fla_line[j], header_string)
				strip_mode  = string.strip(mode_split[1])
				strip_mode = string.expandtabs(strip_mode, 1)
				med = string.rfind(strip_mode, "  ")
				while med != -1:
					strip_mode = strip_mode.replace("  ", " ")
					med = string.rfind(strip_mode, "  ")
				strip_mode = string.split(strip_mode, ' ')
				xss = strip_mode[0]
				try:
					xxx = float(xss)
                                        if xxx < start_header:
                                                start_header = xxx
                                        if xxx > end_header:
                                                end_header = xxx
                                        nr_header += 1
				except ValueError:
					print " Error: ", xss, " no value"
		if staedy == 1:
			test1 = string.split(fla_line[j], '.')
			nr_point = len(test1)
			test2 = string.split(fla_line[j], 'E')
			nr_E = len(test2)
			if nr_point == 15 and nr_E == 15:
				strip_mode = string.strip(fla_line[j])
				strip_mode  = string.split(strip_mode, ' ')
				xss = strip_mode[0]
                                try:
                                        xxx = float(xss)
                                except ValueError:
                                        print " Error: ", xss, " no value"
		find_string = string.rfind(fla_line[j], search_string[i])
		if find_string != -1:
			#if xxx == check_xxx:
			#	count_s = count_s + 1
			#	if max_count_s < count_s:
			#		max_count_s = count_s
			#else:
			#	count_s = 0
			#print "count_s =", count_s
			#print "max_count_s =", max_count_s
			check_xxx = xxx
			string_split = string.split(fla_line[j], search_string[i])
			strip_res = string.strip(string_split[1])
			strip_res = string.expandtabs(strip_res, 1)
			red = string.rfind(strip_res, "  ")
			while red != -1:
				strip_res = strip_res.replace("  ", " ")
				red = string.rfind(strip_res, "  ")
			strip_res = string.split(strip_res, ' ')
			#yss = strip_res[0]
			#print row_nr[i]
			yss = strip_res[row_nr[i]]
			try:
				yyy = float(yss)
			except ValueError:
				print "Error: ", yss, " no value"
				yyy = -1
				#print "     ", res_name[i], " : at ", xss, "  value is set to ", yyy
				print "\n"
				continue
			if yss == "nan" or yss == "inf" or yss == "Inf" or yss == "NaN" or yss == "Nan" or yss == "-inf" or yss == "-INF":
				print "Error: ", yss, " no value"
				yyy = -1
				#print "     ", res_name[i], " : at ", xss, "  value is set to ", yyy
				print "\n"
				continue
			x.append(xxx)
			x[k] = xxx
			y.append(yyy)
			y[k] = yyy
			kmin = k - 1
			if x[k] < x[kmin]:
				for g in range(kmin):
					if x[k] == x[g]:
						www = y[k]
						#print "www(new) =", www, "   k =", k, "    x =", x[k]
						k = g
						y[k] = www
	
			k = k + 1
			len_res = k


	if len_res > 0:
		info = open(res_name[i],'w')

		for h in range(len_res):
			if h < (len_res - 1):
				if x[h] < x[h+1]:
					xwrite = str(x[h])
					ywrite = str(y[h])
					info.write(xwrite + "\t " + ywrite + "\n")
			else:
				xwrite = str(x[h])
				ywrite = str(y[h])
				info.write(xwrite + "\t " + ywrite + "\n")

		info.close()

	if len_res == 0:
		print "      no values found "
	
gen = open("general.csv", 'w')
txt = "CPU Model," + cpu_model
gen.write(txt)
txt = "Bit Mode," + bit_mode
gen.write(txt)
txt = "Host Name," + host_name
gen.write(txt)
txt = "Number of CPUs," + str(nr_cpu) + "\n"
gen.write(txt)
txt = "Run Mode," + run_mode
gen.write(txt)
if run_mode != 'Steady':
        txt = "\nStart," + str(start_header)
        gen.write(txt)
        txt = "\nEnd," + str(end_header)
        gen.write(txt)
        txt = "\nNumber of Time Steps," + str(nr_header)
        gen.write(txt)
txt = "\nNumber of Iterations," + str(acc_iter)
gen.write(txt)

if rest == 1:
        gen.write("\nRestart Files are used")
gen.write("\n--------------------------------------\nRUNTIME ANALYSIS AT END OF CALCULATION\n")
for lin in range(len(csvtim)):
        gen.write(csvtim[lin])
gen.close



print "--------------------------------------------------------\n"	
