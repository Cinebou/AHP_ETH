# Research procedure
1. Make the FMU file of the dynamic simulator from DYMOLA with Modelica.
2. Run the multiple dynamic simulations with some temperature range and cycle time.
3. Extract two results of simulation with specific temperature triple setting. These data will be used for performance map fitting later.
4. Decide some fitting parameters in the short-cut model by fitting. 
5. Apply the fitting perameters and run the short-cut model simulation. 
6. Validate the results from short-cut model and dynamic simulations.

# 1. Make Dynamic simulation
Install the dynamic simulation package, Sorplib from Chair of Technical Thermodynamics.  
https://git.rwth-aachen.de/ltt/SorpLib/-/tree/SorpLib_v2  

Drop the .mo file of this package into DYMOLA.  
Open 'Applications' -> 'Adsorption Chiller' -> 'ModelicaMediaLibrary'.  
Copy the two bed system adsorption chiller model and paste on your new file.  

You need to edit the parameters from python file.  
'Propagate' some parameters to enable the parameters to edit.  
Here, you should edit the inlet temperature of the condenser and the evaporator, temperature swing amplitude and period of the two adsorption beds.  
After you confirm the simulation can be done without error, you generate the fmu file from 'Translate'.  

Note: Branch 'Sorplib_v2' should be used.   
      You need Modelica license for the simulation.  


# 2. Run Dynamic simulation 
You bring the fmu file that you made into './FMU/FMU'.  
The temperature range and cycle time can be edited in the main() of 'dynamic_ac.py'.  
Here, you have to adjust the cycle time so that the operating simulation is Pareto frontier.  

If the simulation stop in the middle (it sometimes happen due to the license problem, make sure that you connect to the server while you're running DYMOLA python simulation), you can restart from there.  
You edit the parameter 'restart' in main(), which is the number of the cases that you finished so far.  

'run_fmu.py' change the input parameters of the each operation points and summarise the data into .csv file.  
All the simulation results is stored in "Results/saving"+self.file_name.replace(".fmu","").replace("./FMU/","")+".csv".  
```
cd FMU
python dynamic_ac.py
```

# 3. Extract dynamic simulation of two temperature triples
You edit the temperature setting in the main() in 'dynamic_ac.py' and run the simulation again.
You can get the simulation results with './Results/~~~~.pickle'

The point of choosing temperature triple is to make the performance results of two simulation separate.  
One of the temperature setting should have high COP and Qflow, and the other should have lower performance.  

# 4. Fitting of short-cut model
