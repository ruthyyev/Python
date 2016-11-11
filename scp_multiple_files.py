#------------------------------------------------------------------------------
#IMPORT REQUIRED MODULES
#------------------------------------------------------------------------------
import paramiko
from paramiko import SSHClient
from scp import SCPClient
import numpy as np 
import progressbar

#------------------------------------------------------------------------------
#LOAD TABLE DATA
#------------------------------------------------------------------------------
source_names = np.loadtxt('/Users/c1541417/Documents/DustPedia/Paper/final_sample_names.csv', dtype=np.str, delimiter=',')

#------------------------------------------------------------------------------
#OPEN THE SSH 
#------------------------------------------------------------------------------
ssh = SSHClient()
ssh.set_missing_host_key_policy(
    paramiko.AutoAddPolicy())
ssh.connect('saruman.astro.cf.ac.uk', username='c1541417', 
    password='Tmfwwyyw3')
    
    
"""
ssh = SSHClient()
ssh.load_system_host_keys()
ssh.connect('c1541417@saruman.astro.cf.ac.uk')
"""
# SCPCLient takes a paramiko transport as its only argument
scp = SCPClient(ssh.get_transport())


bar = progressbar.ProgressBar()

#------------------------------------------------------------------------------
#SCP THE SPIRE DATA
#------------------------------------------------------------------------------
"""
for name in bar(source_names):
    for wavelength in [250, 350, 500]:
        try:
            scp.get('/home/saruman/spx7cjc/DustPedia/SPIRE/Cutouts/'+name+'_SPIRE_'+str(wavelength)+'.fits', '/Users/c1541417/Documents/DustPedia/Paper/Data/SPIRE')
        except:
            print 'fail ' + name + ' ' + str(wavelength)
            
"""
#------------------------------------------------------------------------------
#SCP THE PACS DATA
#------------------------------------------------------------------------------      

for name in bar(source_names):
    for wavelength in [100, 160]:
        try:
            scp.get('/home/saruman/spx7cjc/DustPedia/PACS/Cutouts/'+name+'_PACS_'+str(wavelength)+'.fits', '/Users/c1541417/Documents/DustPedia/Paper/Data/PACS')
        except:
            #print 'fail ' + name + ' ' + str(wavelength)
            print '/home/saruman/spx7cjc/DustPedia/PACS/Cutouts/'+name+'_PACS_'+str(wavelength)+'.fits'

scp.close()