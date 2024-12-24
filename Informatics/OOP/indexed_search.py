import sys


class IndexedSearch:
    def __init__(self):
        self.paths = []

    def add(self, path):
        self.paths.append(path)

    def get(self, pattern):
        def match(path_parts, part):
            path_idx, index = 0, 0

            while index < len(part):
                if part[index] == "*":
                    if index == len(part) - 1:
                        return True
                    while path_idx < len(path_parts) and not match(path_parts[path_idx:], part[index + 1:]):
                        path_idx += 1
                    return path_idx < len(path_parts)
                elif part[index] == "?":
                    if path_idx >= len(path_parts):
                        return False
                elif index >= len(path_parts) or part[index] != path_parts[path_idx]:
                    return False

                path_idx += 1
                index += 1

            return path_idx == len(path_parts)

        pattern_parts = pattern.split('/')
        result = []

        for path in self.paths:
            path_parts = path.split('/')
            if match(path_parts, pattern_parts):
                result.append(path)

        return result


input_lines = sys.stdin.read().strip().split('\n')
indexed_search = IndexedSearch()

for line in input_lines:
    if line.startswith("find:"):
        pattern = line[len("find:"):].strip()
        results = indexed_search.get(pattern)
        for result in results:
            print(result)
    else:
        indexed_search.add(line.strip())
