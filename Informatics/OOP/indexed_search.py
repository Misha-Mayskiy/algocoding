class IndexedSearch:
    def __init__(self):
        self.paths = []

    def add(self, path):
        self.paths.append(path)

    def get(self, pattern):
        def match(path_parts, pattern_parts):
            path_idx, pattern_idx = 0, 0

            while pattern_idx < len(pattern_parts):
                if pattern_parts[pattern_idx] == "*":
                    if pattern_idx == len(pattern_parts) - 1:
                        return True  # Trailing * matches everything
                    while path_idx < len(path_parts) and not match(path_parts[path_idx:], pattern_parts[pattern_idx + 1:]):
                        path_idx += 1
                    return path_idx < len(path_parts)
                elif pattern_parts[pattern_idx] == "?":
                    if path_idx >= len(path_parts):
                        return False
                elif pattern_idx >= len(path_parts) or pattern_parts[pattern_idx] != path_parts[path_idx]:
                    return False

                path_idx += 1
                pattern_idx += 1

            return path_idx == len(path_parts)

        pattern_parts = pattern.split('/')
        result = []

        for path in self.paths:
            path_parts = path.split('/')
            if match(path_parts, pattern_parts):
                result.append(path)

        return result

# Example usage
searcher = IndexedSearch()
searcher.add("C:/folder1/folder11/file111")
searcher.add("C:/folder1/folder11/file112")
searcher.add("C:/folder1/folder12/file121")
searcher.add("C:/folder2/folder22/file122")
searcher.add("C:/folder2/folder21/file111")

# Perform search
query = "file111"
print("\n".join(searcher.get(query)))
