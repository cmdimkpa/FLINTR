# FLINTR
An Arithmetic Solver for Python

FLINTR (FormuLa INTerpreter and TRanslator):

	An arithmetic solver.

	(1) Encode your formula into a string e.g. 'a+(b-1)*c^2'
			** supports letters, integer numerals '0 - 9' and parenthesis '( )'.
			** the numbers 1/2 and 1/3 are represented by the symbols > and ] respectively (e.g. sqrt(2) is '2^>' and cuberoot(3) is '3^]')
			** supports standard arithmetic operations
	(2) Create a FLINTR instance and bind your formula to the object e.g. formula = FLINTR('a+(b-1)*c^2')
	(3) Interpret the formula with interpret() e.g. formula.interpret()
	(4) Set values for formula parameters by passing a value_dict to the formula object e.g. 
			value_dict = {'a':1,'b':2,'c':3}
			formula.set_values(value_dict)
	(5) Solve the formula by calling solve() e.g. formula.solve()
	(6) This will output the result of the calculation .e.g. 10 (for this example)
