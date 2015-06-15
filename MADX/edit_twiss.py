###########################################################################
#
# Script to edit the aperture file (note: assumes a thick sequence!)
# * add markers before/after each element in the matching sections with aperture = 0.04
# * add BPMs in the arcs, before each quadrupole
# * convert circle into rectellipse to be read by GetAperture
#
#
#########################################################################

import re

inIR = False
inCOLL = False
addLine = False
drift_aperture = 0.040000
BPM_aperture = 0.018000
BPM_lenght = 0.30
lastElement = ""

with open('twiss_aperture_thick_b1.tfs', 'r') as infile:
    with open('allapert_final.b1', 'w') as outfile:
        line = infile.readlines()
        for item in line:
            if item[0] == '@' or item[0] == '$' or item[0] == '*':
                outfile.write(item)
    outfile.close()
infile.close()

with open('twiss_aperture_thick_b1.tfs', 'r') as infile:
    with open('allapert_final.b1', 'a') as outfile:
        counter = 0
        for character in infile:
            columns = character.strip().split()
            if character[0] != '@' and character[0] != '$' and character[0] != '*':
                if columns[1].find("IR_FCC_HH$START") >=0:
                    print "IR starting at s %f" %float(columns[3])
                    inIR = True
                if columns[1].find("IR_FCC_HH$END") >=0:
                    print "IR ending at s %f" %float(columns[3])
                    inIR = False
                if columns[1].find("S.COLL") >=0:
                    print "Collimation insertion starting at s %f" %float(columns[3])
                    inCOLL = True
                if columns[1].find("E.COLL") >=0:
                    print "Collimation insertion ending at s %f" %float(columns[3])
                    inCOLL = False

                #insert markers before and after each element in matching section
                if inIR:
                    #only consider elements that are no drifts and have L>0 and that are in the matching section:
                    if columns[0].find("DRIFT")<0 and float(columns[4])>0. and (columns[1].find("MQYY")>0 or columns[1].find("MQYL")>0 or columns[1].find("DM")>0 or columns[1].find("MQML")>0 or columns[1].find("MQM")>0 ):
                        s_before = float(columns[3]) - ( float(columns[4]) + 0.2)
                        s_after = float(columns[3]) + 0.2
                        addLine = True

                #add BPMs in DS and ARCs before each quadrupole
                if not inIR and not inCOLL:
                    if ( columns[1].find("MQ.")>0 or columns[1].find("MQT.")>0 or columns[1].find("MQTL.")>0 or columns[1].find("MQDA.")>0 or columns[1].find("MQDB.")>0):
                        #Note: If there are two quadrupoles one after each other (eg. MQT, MQ), only place one BMP before the first one
                        if lastElement.find("MQ")<0:
                            s_start_bpm =  float(columns[3]) - ( float(columns[4]) + 1.0) #BMP 1m before the quadrupole
                            s_stop_bpm = s_start_bpm + BPM_lenght
                            outfile.write('%20s %-17s %19s %23f %18f %15f %18f %18f %18f \n' % ('"MARKER"', '"BPM"',  '"MARKER"', s_start_bpm , 0.0, BPM_aperture , BPM_aperture ,BPM_aperture ,BPM_aperture ))
                            outfile.write('%20s %-17s %19s %23f %18f %15f %18f %18f %18f \n' % ('"MARKER"', '"BPM"',  '"MARKER"', s_stop_bpm , 0.0, BPM_aperture , BPM_aperture ,BPM_aperture ,BPM_aperture ))
                if columns[0].find("DRIFT")<0:
                    lastElement = columns[1]

                # Skip open apertures
                #if float(columns[5]) == 9.999999 and float(columns[6]) == 9.999999 and float(columns[7]) == 9.999999 and float(columns[8]) == 9.999999:
                #    continue
                # Skip closed apertures
                #elif float(columns[5]) == 0 and float(columns[6]) == 0 and float(columns[7]) == 0 and float(columns[8]) == 0:
                #    continue
               
                #edit last line: give it an aperture=arc
                if columns[1].find("FCC_RING$END")>0:
                    outfile.write('%20s %-17s %19s %23f %18f %15f %18f %18f %18f \n' % (columns[0], columns[1], columns[2], float(columns[3]), float(columns[4]), 0.016000, 0.013000, 0.016000, 0.016000))

                #insert markers before each element in matching section
                if addLine:
                    outfile.write('%20s %-17s %19s %23f %18f %15f %18f %18f %18f \n' % ('"MARKER"', '"MK"',  '"MARKER"', s_before, 0.0, drift_aperture, drift_aperture, drift_aperture, drift_aperture))

                 # Transform CIRCLE
                if float(columns[5]) != 0 and float(columns[6]) == 0 and float(columns[7]) == 0 and float(columns[8]) == 0:
                    outfile.write('%20s %-17s %19s %23f %18f %15f %18f %18f %18f \n' % (columns[0], columns[1], columns[2], float(columns[3]), float(columns[4]), float(columns[5]), float(columns[5]), float(columns[5]), float(columns[5])))
                # Transform RACETRACK
                elif float(columns[5]) == 0 and float(columns[6]) != 0 and float(columns[7]) != 0 and float(columns[8]) == 0:
                    outfile.write('%20s %-17s %19s %23f %18f %15f %18f %18f %18f \n' % (columns[0], columns[1], columns[2], float(columns[3]), float(columns[4]), float(columns[6]), float(columns[6]), float(columns[7]), float(columns[7])))
                else:
                    outfile.write('%20s %-17s %19s %23f %18f %15f %18f %18f %18f \n' % (columns[0], columns[1], columns[2], float(columns[3]), float(columns[4]), float(columns[5]), float(columns[6]), float(columns[7]), float(columns[8])))
                #insert markers after each element in matching section
                if addLine:
                    outfile.write('%20s %-17s %19s %23f %18f %15f %18f %18f %18f \n' % ('"MARKER"', '"MK"','"MARKER"', s_after, 0.0, drift_aperture, drift_aperture, drift_aperture, drift_aperture))
                    addLine = False
                                 
    outfile.close()
infile.close()

# with open('allapert_final.b1', 'r') as infile:
#     with open('plot_allapert.txt', 'w') as outfile:
#         for character in infile:
#             columns = character.strip().split()
#             if character[0] != '@' and character[0] != '$' and character[0] != '*':
#                 outfile.write('%0s %15f %15f %15f %15f \n' % (columns[3], float(columns[5]), float(columns[6]), float(columns[7]), float(columns[8])))
#     outfile.close()
# infile.close()
