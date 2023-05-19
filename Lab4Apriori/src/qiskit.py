import qiskit
from qiskit.algorithms import AmplificationProblem, Grover
from qiskit.algorithms import Grover
from qiskit.primitives import Sampler

# the state we desire to find is '11'
good_state = ['01']

# specify the oracle that marks the state '11' as a good solution
oracle = qiskit.QuantumCircuit(2)
oracle.x(0)
oracle.cz(0, 1)
oracle.x(0)

# define Grover's algorithm
problem = AmplificationProblem(oracle, is_good_state=good_state)

# now we can have a look at the Grover operator that is used in running the algorithm
# (Algorithm circuits are wrapped in a gate to appear in composition as a block
# so we have to decompose() the op to see it expanded into its component gates.)
problem.grover_operator.decompose().draw(output='mpl')

grover = Grover(sampler=Sampler())
result = grover.amplify(problem)
print('Result type:', type(result))
print()
print('Success!' if result.oracle_evaluation else 'Failure!')
print('Top measurement:', result.top_measurement)