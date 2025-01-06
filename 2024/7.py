def backtrack(target, nums, concat=False):
    def iter(total, index):
        if total == target and index == len(nums):
            return True
        elif total > target or index >= len(nums):
            return False
        else:
            num = nums[index]
            return (
                iter(total + num, index + 1) 
                or iter(total * num, index + 1)
                or (concat and iter(int(f"{total}{num}"), index + 1))
            )
    return iter(nums[0], 1)

def main():
    with open("7.txt") as f:
        silver = 0
        gold = 0
        for line in f.readlines():
            target, nums = line.split(": ")
            target = int(target)
            nums = [ int(i) for i in nums.split(" ") ]
            if backtrack(target, nums):
                silver += target
            if backtrack(target, nums, True):
                gold += target
        print(silver)
        print(gold)

if __name__ == '__main__':
    main()