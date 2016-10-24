#Import twython interface as ti
#to be used as
#python -i tiStarter.py
#This is to load python in interactive mode with the twython interface already
#loaded
import twythonInterface as ti

print "\n\n\nLoaded twythonInterface as ti\n\n\n"
print "To search for terms use:\nti.searchForTerms(<term>, <count>, <output file name>)"
print "To stream ids to file use:\nti.streamIDsTo(<output file name>, <location box>)"
print "To grab timelines:\nti.grabTimelines(<id file name>, <output file name>)"
