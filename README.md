# Quasi-continuous short-cut adsorption chiller process simulator
You can calculate the performance of the adsorption chiller(COP, cooling power) with good accuracy and high computational efficiency.

# Usage
## Dynamic simulation
You need the sample data from dynamic simualtions for the parameter fittings.

You select two temperature triples, (T<sub>heat</sub>, T<sub>reject</sub>, T<sub>chill</sub>) and run the simulation for two lines.
Run "dynamic.py"
```bash
python dynamic.py
```
### Note
The cycle time of the performance map should be the Pareto frontier.

You can calculate more than two lines in once.

When the calculation stops in the middle, you can restart from 'restart' in line 37.

The FMU file is made in DYMOLA.

## Fitting
Using the obtained data, the parameters in short-cut model is adjusted with least-square method.

You shoud tune the initial guess for better fitting results.

The fitting parameters are output in the console.

Run "fitModel.py"
```bash
python fitModel.py
```

## Searching the optimal operating setting
You can store the fitted parameters in "param_database.py".

With the optimized parameters, you can calculate the short-cut model.

The temperature range can be changed.

Run "generate_multipoint.py"
```bash
python generate_multipoint.py
```
### Note
Unfeasible temperature setting at low heating temperatures are excluded from calculation.

Additionally, lower rejecting temperature output error, sometimes.

## Validation
You can compare the dynamic simulation results and short-cut model results.

Run "validation.py"
```bash
python validation.py
```

# Requirement
* Python 3.8.5
* REFPROP
* TILMedia for Modelica (to calculate dynamic simulation in DYMOLA)

# Author
Andrej  Gibelhaus  
Hibiki Kimura  
Fabian Mayer  
