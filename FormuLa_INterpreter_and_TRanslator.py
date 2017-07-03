from __future__ import division

class FLINTR(object):
	"""
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

	"""

	global operator_set, operator_indexes, protocol_stack, sigil_dict, sigil_length,\
	new_sigil,gen_sigil,Interpreter,value_store,Translator, random, collections, standardize, init_index,\
	sigil_test,reIndex,split_expression,last_result,sigils,store,Builder,sigilation,formula,\
	operator_counts,force_user_order, nestor, old_formula, nestingTest, number_dict, special_dict

	import random
	import collections

	operator_set = ('^','/','%','*','-','+','(',')')
	number_dict = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9}
	special_dict = {'>':1/2,']':1/3}

	sigil_dict = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h',8:'i',9:'j',10:'k',11:'l',\
	12:'m',13:'n',14:'o',15:'p',16:'q',17:'r',18:'s',19:'t',20:'u',21:'v',22:'w',23:'x',24:'y',25:'z',\
	26:'A',27:'B',28:'C',29:'D',30:'E',31:'F',32:'G',33:'H',34:'I',35:'J',36:'K',37:'L',\
	38:'M',39:'N',40:'O',41:'P',42:'Q',43:'R',44:'S',45:'T',46:'U',47:'V',48:'W',49:'X',50:'Y',51:'Z',\
	52:'!',53:'@',54:'#',55:'$',56:'&',57:'=',58:'|',59:'?',60:';',61:',',62:'.',63:':',64:'"',65:'0',\
	66:'1',67:'2',68:'3',69:'4',70:'5',71:'6',72:'7',73:'8',74:'9',75:'<',76:'[',77:'{',78:'}'}
	sigil_length = 1
	sigils = [sigil_dict[i] for i in sigil_dict]


	
	def new_sigil():
		sigil=''
		while len(sigil) < sigil_length:
			pointer = int(random.random()*len(sigil_dict.keys()))
			sigil+=sigil_dict[pointer]
		return sigil

	
	def sigil_test(sigil):
		if sigil in formula or sigil in store.keys() or sigil in protocol_stack.keys() or sigil in value_store.keys():
			return True
		else:
			return False

	
	def gen_sigil():
		sigil = new_sigil()
		while sigil_test(sigil):
			sigil = new_sigil()
		return sigil

		
	def init_index():
		operator_indexes = {}
		for operator in operator_set:
			operator_indexes[operator]=[]
		return operator_indexes

	
	def reIndex():
		global operator_indexes
		operator_indexes = init_index()
		j=-1
		for char in formula:
			j+=1
			if char in operator_set:
				operator_indexes[char].append(j)

	
	def standardize(formula_string):
		formula_string = formula_string.lower()
		vagrants = list(set([char for char in formula_string if char not in operator_set and char not in sigils and char not in special_dict]))
		for char in vagrants:
			formula_string = formula_string.replace(char,'')
		return formula_string

	
	def sigilation(index):
		global store, formula,protocol_stack
		left_index = index - 1
		right_index = index + 2
		group = formula[left_index:right_index]
		# update store and protocol stack
		sigil = gen_sigil()
		store[sigil] = '('+group+')'
		# replace group with sigil in formula
		formula = formula.replace(group,sigil)
		protocol_stack[sigil] = group
		reIndex()


	def nestingTest():
		# concordant or discordant nesting?
		discordant=0
		use_left = -1
		use_right = 0
		error=0
		reIndex()
		try:

			max_left = operator_indexes['('][-1]
			first_right = operator_indexes[')'][0]

			if first_right<max_left:
				discordant = 1
				use_left = -1
				use_right = -1
		except:
			error=1

		return use_left,use_right,error

	def force_user_order():
		global formula, operator_indexes, store, protocol_stack, old_formula
		reIndex()
		nest_count = len(operator_indexes['('])
		old_formula = [formula]
		for i in range(nest_count):
			use_left,use_right,error = nestingTest()
			if error == 0:
				left = operator_indexes['('][use_left]
				right = operator_indexes[')'][use_right]+1
				group = formula[left:right]
				entry = group[1:-1]
				formula = entry
				nestor()
				last_protocol_key = list(protocol_stack.keys())[-1]
				formula = old_formula[i]
				formula = formula.replace(group,last_protocol_key)
				old_formula.append(formula)





	def nestor():
		global formula, operator_indexes, store, protocol_stack, operator_counts, old_formula

		operator_counts = []
		reIndex()
		operator_counts.append(len(operator_indexes['^'])) 
		operator_counts.append(len(operator_indexes['/'])) 
		operator_counts.append(len(operator_indexes['%'])) 
		operator_counts.append(len(operator_indexes['*'])) 
		operator_counts.append(len(operator_indexes['-'])) 
		operator_counts.append(len(operator_indexes['+']))

		# implement order-of-precedence based nesting (^, /, %, *, -, +)
		k=-1
		for operator in operator_set[:6]:
			k+=1
			for i in range(operator_counts[k]):
				sigilation(operator_indexes[operator][-1])

	
	def Interpreter(formula_string):
		global protocol_stack,operator_indexes,operator_counts, formula, store, value_store, old_formula

		protocol_stack = collections.OrderedDict({})
		store = collections.OrderedDict({})
		value_store = {}

		formula = standardize(formula_string)
		force_user_order()
		nestor()

		# defining the value store

		for char in old_formula[0]:

			if char not in operator_set:

				if char in number_dict:

					value_store[char] = number_dict[char]

				elif char in special_dict:

					value_store[char] = special_dict[char]

				else:
					value_store[char] = 0.00

		return protocol_stack, value_store

	
	def split_expression(expression):
		alpha = expression[0]
		operator = expression[1]
		beta = expression[2]
		return alpha,operator,beta

		
	def Translator(protocol_stack):
		global last_result
		last_result = 0.00
		sequence_keys = list(protocol_stack.keys())
		for sequence_key in sequence_keys:
			expression = protocol_stack[sequence_key]
			try:
				alpha,operator,beta = split_expression(expression)
				alpha_val = value_store[alpha]
				beta_val = value_store[beta]
				if operator == '+':
					last_result = alpha_val+beta_val
				if operator == '-':
					last_result = alpha_val-beta_val 
				if operator == '/':
					try:
						last_result = alpha_val/beta_val
					except:
						last_result = 0
				if operator == '*':
					last_result = alpha_val*beta_val
				if operator == '^':
					last_result = alpha_val**beta_val
				if operator == '%':
					try:
						last_result = alpha_val%beta_val
					except:
						last_result = 0
				value_store[sequence_key] = last_result
			except:
				pass
		return last_result

	
			
	def __init__(self,formula_string):
		self.formula_string = formula_string
		self.protocol_stack = collections.OrderedDict()
		self.value_store={}
		self.last_result=0.00
		self.formula_name = ''
		self.var_names = {}

	
	def interpret(self):
		if self.formula_string != '':
			self.protocol_stack, self.value_store = Interpreter(self.formula_string)

	
	def solve(self):
		if self.protocol_stack != collections.OrderedDict():
			self.last_result = Translator(self.protocol_stack)
			return self.last_result

	
	def get_params(self):
		if self.formula_string != '':
			return list(self.value_store.keys())
	
	
	def set_values(self,value_dict):
		try:
			for key in value_dict.keys():
				if key in self.value_store.keys():
					if key != '1':
						self.value_store[key] = value_dict[key]
					else:
						self.value_store[key] = 1.00
		except:
			pass

	def set_var_names(self,name_dict):
		try:
			for key in name_dict.keys():
				if key in self.value_store.keys():
					self.var_names[key] = name_dict[key]
		except:
			pass

	def set_formula_name(self,fname):
		self.formula_name = fname


	
	def get_values(self):
		return self.value_store


		
		


