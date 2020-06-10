import random
import numpy as np
from viz import draw_graph

def gen_hash():
    return random.getrandbits(16)

def generate_rule():

    def iterate_base(inputs):
        x, y = inputs[0]
        z = gen_hash()
        return [[x,y], [y,z]]

    def should_rule_apply_base(inputs):
        pathA = inputs[0]
        x, y = pathA
        if x != y:
            return True
        else:
            return False

    def iterate_loop(inputs):
        x, y = inputs
        z = gen_hash()
        return [[y,z], [z,x]]

    def iterate_tree(inputs):
        x, y  = inputs
        z = gen_hash()
        return [[x,z], [z,z], [z,z]]

    def iterate_mesh(inputs):
        pathA, pathB = inputs
        x, y, _ = pathA
        z, x, u = pathB
        v = gen_hash()
        return [[y,v], [v,y], [y,z], [z,v], [u,v], [v,v]]
        #return [[y, v, y], [y, z, v], [u, v, v]]

    def should_rule_apply_mesh(inputs):
        pathA, pathB = inputs
        if (pathA[0] != pathA[1] and pathA[1] == pathA[2]) and \
                (pathB[0] != pathB[1] and pathB[1] != pathB[2]):
                    return True
        else:
            return False

    return iterate_base, should_rule_apply_base
    return iterate_mesh, should_rule_apply_mesh

def generate_hashes(n):
    hashes = []
    for iteration in range(n):
        hashes.append(gen_hash())
    return hashes

def generate_relations(hashes, n_relations):
    relations = []
    for iteration in range(n_relations):
        selected_hashes = []
        for card in range(2):
            selected_hashes.append(hashes[np.random.randint(0, len(hashes))])
        relations.append( selected_hashes )
    return relations

def follow(n_steps, starting_hash, relations):
    path_def = [starting_hash]
    hash_ptr = starting_hash
    for step in range(n_steps-1):
        relation_subset = [x for x in relations if x[0] == hash_ptr]
        try:
            chosen_relation = relation_subset[np.random.randint(0, len(relation_subset))]
            hash_ptr = chosen_relation[1]
        except:
            hash_ptr = 'TERMINAL'
        path_def.append(hash_ptr)
    return path_def

### CONFIG: CHANGE THESE
N_HASHES = 5
N_RELATIONS = 5
N_EVOLUTIONS = 10
N_REPLACEMENT_CHECKS = 200

### CONFIG: KEEP THESE, MOSTLY
PATH_CARDINALITY = 2
NUM_PATHS_IN_INPUTS = 1
NUM_STEPS_PER_PATH = 2

### START PROGRAM

# INITIAL CONDITIONS
print('GENERATING...')
initial_hashes = generate_hashes(N_HASHES)
relations = generate_relations(initial_hashes, 
                                N_RELATIONS)

# EVOLVE USING RULE
apply_rule, should_rule_apply = generate_rule()

rule_applications = 0
for n_evolution in range(N_EVOLUTIONS):
    attempted_indexes = []
    for n_replacement in range(N_REPLACEMENT_CHECKS):
        while True and len(attempted_indexes) < len(relations)/2:
            idx1 = np.random.randint(0, len(relations))
            if idx1 not in attempted_indexes:
                attempted_indexes.append(idx1)
                break
        while True and len(attempted_indexes) < len(relations)/2:
            idx2 = np.random.randint(0, len(relations))
            if idx2 not in attempted_indexes:
                attempted_indexes.append(idx2)
                break
        if len(attempted_indexes) >= len(relations)/2:
            break

        input_paths = []
        for path_idx in range(NUM_PATHS_IN_INPUTS):
            input_paths.append(
                follow(n_steps=NUM_STEPS_PER_PATH, 
                    starting_hash=relations[idx1][0],
                    relations=relations)
                )

        inputs = input_paths
        if should_rule_apply(inputs):
            new_relation = apply_rule(inputs)
            # delete the old relation(s)
            '''
            if idx1 > idx2:
                del relations[idx1]
                del relations[idx2]
            elif idx1 < idx2:
                del relations[idx2]
                del relations[idx1]
            else:
                del relations[idx1]
            '''
            # add the new relation(s)
            relations = relations + new_relation
            rule_applications += 1
            print('RULE APPLIED %i' % rule_applications)
        else:
            # rule should not be applied
            pass

# DRAW THE GRAPH
print('DRAWING...')
draw_graph(relations)
print ('LEN of relations: %i' % len(relations))

print ('Rule applications: %i' % rule_applications)

print('EOL...')
