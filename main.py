from functools import wraps
from time import process_time


def timeit(func):
    """Execution time decorator"""
    @wraps(func)
    def _time_it(*args, **kwargs):
        start = int(round(process_time() * 1000))
        try:
            return func(*args, **kwargs)
        finally:
            end_ = int(round(process_time() * 1000)) - start
            print(
                f"Total execution time {func.__name__}: {end_ if end_ > 0 else 0} ms"
            )

    return _time_it


class Cypher:
    block = 10
    block_coef = 0.05

    def __init__(self):
        while True:
            self.file_path = input("Enter full file path: ")
            self.len_, self.block = self.get_settings()
            self.height = self.get_height()
            choice = input("Type\n e to encrypt\n d to decrypt\n:")
            if choice == 'e':
                self.encrypt()
            elif choice == 'd':
                self.decrypt()

    @timeit
    def encrypt(self):
        levels = ['' for lvl in range(self.height)]
        heights = self.__heights()
        for b in self.__blocks():
            for char in b:
                levels[next(heights)] += char
        with open('encrypted.txt', 'w') as out:
            for b in levels[::-1]:
                out.write(b)

    @timeit
    def decrypt(self):
        levels = self.generate_levels()
        file = open(self.file_path, 'r')
        for lvl, count in enumerate(levels):
            levels[lvl] = file.read(count)
        levels = levels[::-1]
        heights = self.__heights()
        out_str = ''
        for i in range(self.len_):
            cur_h = next(heights)
            out_str += levels[cur_h][0]
            levels[cur_h] = levels[cur_h][1:]
        with open('decrypted.txt', 'w') as out:
            out.write(out_str)

    def generate_levels(self):
        """Returns chars count for each height level"""
        levels = [0 for lvl in range(self.height)]
        heights = self.__heights()
        for b in range(self.len_):
            levels[next(heights)] += 1
        return levels[::-1]

    def __blocks(self):
        """File data generator"""
        file = open(self.file_path, 'r')
        while True:
            data = file.read(self.block)
            if not data:
                break
            yield data

    def __heights(self):
        """Current height generator"""
        heights = list(range(self.height))
        heights += heights[1:-1][::-1]
        while True:
            for h in heights:
                yield h

    def get_height(self):
        """Get height(key) from user"""
        while True:
            h = int(input(f"Enter height (1 < height < {self.block}): "))
            if 1 < h < self.block:
                return h

    def get_settings(self):
        """Get file len and calculate block size"""
        len_ = sum(len(bl) for bl in self.__blocks())
        block = int(len_ * self.block_coef)
        return len_, block


if __name__ == '__main__':
    c = Cypher()
