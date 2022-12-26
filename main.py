from hint import Hint
from generate_map import *


n = 16
array_map = np.chararray([n, n], 3, "utf-8")

array_map = gen_map(array_map, n)
print(array_map)

res = minDistance(array_map, 'p')
if (res != -1):
    print("Number of steps:", res.dist)
    print("Pirate is in:", res.preStep.pop(0))
    print(res.preStep)
else:
    print("Can not find")


hint = Hint(array_map, n)
hint.hint_1()
hint.hint_2()
hint.hint_3()
hint.hint_4()
hint.hint_5()
hint.hint_6()
hint.hint_7()
hint.hint_8()
hint.hint_12()
hint.hint_14()
hint.hint_15()

hint.print_hint_list()

# hint.verify(hint.hint_list[0])
# hint.verify(hint.hint_list[1])
# hint.verify(hint.hint_list[2])
print("\n\n")
#print(hint.hint_list[6])
#hint.verify(hint.hint_list[6])
print(hint.hint_list[4])

#print(hint.mask_map)
