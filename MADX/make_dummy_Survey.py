import re

with open('outputTwiss/FCCAperture.b1.dat', 'r') as infile:
    with open('SurveyWithCrossing_XP_lowb.dat', 'w') as outfile:
        outfile.write("\%s [m]   Xx [m]   Yx [m]   Xs [m] PXx [rad] PYx [rad] \n")
        line = infile.readlines()
        for item in line:
            if item.find("s")>=0:
                continue
            s_pos = float(item.split()[0])
            outfile.write("%2.1f \t %2.7f \t %2.7f \t %2.7f \t %2.7f \t %2.7f \n" %(s_pos,0.0,0.0,0.0,0.0,0.0))
    outfile.close()
infile.close()
