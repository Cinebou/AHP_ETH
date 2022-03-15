# Quasi-continuous short-cut adsorption chiller process simulator
You can calculate the performance of the adsorption chiller(COP, cooling power) with good accuracy and high computational efficiency.  
An instraction is given in 'manual.md'


# Requirement
* Python 3.8.5  
* REFPROP  
* TILMedia for Modelica (to calculate dynamic simulation in DYMOLA)  

# Package 
matplotlib.pyplot  
pandas  
pickle  
scipy   

They can be installed with pip.

# File tree
* FMU/ : dynamic simulation  
* Log/ : log files e.g. error record file  
* PerformanceMap/SCP_COP : the performance of the dynamic simulation. They're used for fitting.
* Results/ : store or use results
* Sequaence/ : sequence diagrams of the simulator
* test_code/ : calculate the adsorption potential, enthalpy, fluid properties. If you want to use them, you need to move these files to the ground directly.

# cited parameters
[1]: Adsorption potentila of Silicagel123_water, 'workingpair_database.py'  
Dirk Schawe. Theoretical and Experimental Investigations of an Adsorption Heat Pump with Heat Transfer between two Adsprbers.2001, PhD thesis, 2001.  
[2]: Adsorption potentila of AQSOA_Z02_water, 'workingpair_database.py'  
Uwe Bau. From dynamic simulation to optimal design and control of adsorption energy systems. PhD thesis, 2018  
[3]: Feasible temperare setting of adsorption chiller, 'FMU_dynamic_sc.py', 'generate_multipoint.py'  
Mahbubul Muttakin, Sourav Mitra et al. International Journal of Heat and Mass Transfer, 122, 7 2018, Fig 8

# Author
Andrej  Gibelhaus  
Hibiki Kimura  
Fabian Mayer  
