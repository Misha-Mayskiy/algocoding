old_keys = set(eval(input()).new_nodes())
new_keys = set(eval(input()).new_nodes())

kept = old_keys.intersection(new_keys)
added = new_keys.difference(old_keys)
removed = old_keys.difference(new_keys)

result = {
    'kept': kept,
    'added': added,
    'removed': removed
}
print(result)
