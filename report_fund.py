# a tree has type (number, tree list list) where the tree list list is
# a partition of the subtrees for the children of number by account type

################################################################

def account_tree(number, chart):
    account = chart.account(number)

    name = lambda num: chart.account(num).name()
    asset = sorted(account.asset(), key=name)
    liability = sorted(account.liability(), key=name)
    fund = sorted(account.fund(), key=name)
    income = sorted(account.income(), key=name)
    expense = sorted(account.expense(), key=name)

    trees = [account_trees(kind, chart)
             for kind in [asset, liability, fund, income, expense]]
    trees = [tree for tree in trees if tree]

    return (number, trees)

def account_trees(numbers, chart):
    return [account_tree(num, chart) for num in numbers]

################################################################

def account_tree_prune(tree, prune_number):
    (number, trees_list) = tree

    if prune_number(number):
        return None

    trees_list = [account_trees_prune(trees, prune_number)
                  for trees in trees_list ]
    trees_list = [trees for trees in trees_list if trees]

    return (number, trees_list)
    
def account_trees_prune(trees, prune_number):
    trees = [account_tree_prune(tree, prune_number) for tree in trees]
    trees = [tree for tree in trees if tree]
    return trees

################################################################

def account_tree_strip_income_expense(tree, chart):
    return account_tree_prune_income_expense(tree, chart)

################################################################

def list_unzip(pairs):
    return ([pair[0] for pair in pairs],
            [pair[1] for pair in pairs])

def list_simplify(elts):
    return [elt for elt in elts if elt]

def list_list_filter(list_list, keep_elt):
    keep_elts = lambda elts: [elt for elt in elts if keep_elt(elt)]
    return list_simplify([keep_elts(elts) for elts in list_list])

################################################################

# tree = (number, tree list list)

# tree -> number list list
def account_tree_flatten(tree):
    return account_tree_list_flatten([tree])

# tree list -> number list list
def account_tree_list_flatten(tree_list):
    if not tree_list:
        return []

    (numbers, tree_list_lists) = list_unzip(tree_list)

    number_list_list = [numbers]
    for tree_list_list in tree_list_lists:
        number_list_list += account_tree_list_list_flatten(tree_list_list)
    return list_simplify(number_list_list)

# tree list list -> number list list
def account_tree_list_list_flatten(tree_list_list):
    if not tree_list_list:
        return []
    
    number_list_list = []
    for tree_list in tree_list_list:
        number_list_list += account_tree_list_flatten(tree_list)
    return list_simplify(number_list_list)        

################################################################

def account_tree_prune_income_expense(tree, chart):
    return account_tree_prune(tree,
                              lambda num:
                              chart.account(num).is_income() or
                              chart.account(num).is_expense())

def account_tree_list_income_expense(tree, chart):
    def number_keep(num):
        return chart.account(num).is_income() or chart.account(num).is_expense()
    number_list_list = account_tree_flatten(tree)
    return list_list_filter(number_list_list, number_keep)

################################################################
