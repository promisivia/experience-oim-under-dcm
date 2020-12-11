from visualizationTools.drawBaseFunction import *

drawType = "Average"  # "Cumulative" "Average" "Default"

alg_list = [
    ('UCB', 'UCB', 'orange', 'UCB'),
    ('CMAB-average', 'CMAB_average', '#0072BD', 'CMAB-UCB-average'),
    ('CMAB-random', 'CMAB_random', '#7E2F8E', 'CMAB-UCB-random'),
    ('DILinUCB-DC', 'DILinUCB-DC', 'green', 'DILinUCB'),
    ('DC-UCB-radius0.1', 'DC-UCB', '#A2142F', 'DC-UCB'),
]

dataset_list = ['Small2']
scale_list = ['0.5-0.9_10000']
for dataset in dataset_list:
    for scale in scale_list:
        file_path_ex1 = '../SimulationResults/Ex1/' + dataset + '_' + scale + '/'
        if dataset == 'Small2':
            draw_Reward(fileFolderPath=file_path_ex1, alg_list=alg_list, count=2000, drawType=drawType,
                        issave=True, file_name="Ex1_" + dataset + scale, y_start=17.5, y_end=18.5, subTitile='(d) 20 nodes, 51 edges')
        # else:
        #     draw_Reward(fileFolderPath=file_path_ex1, alg_list=alg_list, count=10000, drawType=drawType,
        #                 issave=True, file_name="Ex1_" + dataset + scale, subTitile='(c) 10 nodes, 13 edges')

alg_list = [
    ('CUCB', 'CUCB', '#EDB120', 'CUCB(IC)'),
    ('CMAB-average', 'CMAB_average', '#0072BD', 'CMAB-UCB-average'),
    ('CMAB-random', 'CMAB_random', '#7E2F8E', 'CMAB-UCB-random'),
    ('DILinUCB-DC', 'DILinUCB-DC', 'green', 'DILinUCB'),
    ('DC-UCB-radius0.1', 'DC-UCB', '#A2142F', 'DC-UCB'),
]
# prob = 0.2
# file_path_ex2 = '../SimulationResults/Ex2/p=' + str(prob) + '/'
# draw_Reward(fileFolderPath=file_path_ex2, alg_list=alg_list, count=10000, y_start= 0,
#             drawType=drawType, issave=True, file_name="Ex2_p=" + str(prob), subTitile="(a) p=" + str(prob),
#             )
# prob = 0.5
# file_path_ex2 = '../SimulationResults/Ex2/p=' + str(prob) + '/'
# draw_Reward(fileFolderPath=file_path_ex2, alg_list=alg_list, count=10000, y_start= -2,
#             drawType=drawType, issave=True, file_name="Ex2_p=" + str(prob), subTitile="(b) p=" + str(prob))
#
prob = 0.8
file_path_ex2 = '../SimulationResults/Ex2/p=' + str(prob) + '/'
# draw_Reward(fileFolderPath=file_path_ex2, alg_list=alg_list, count=10000, y_start= 0,
#             drawType=drawType, issave=True, file_name="Ex2_p=" + str(prob), subTitile="(c) p=" + str(prob))

file_path_ex4 = '../SimulationResults/Flixster/'
alg_list = [
    ('CUCB', 'CUCB', '#EDB120', 'CUCB(IC)'),
    ('CMAB-average', 'CMAB_average', '#0072BD', 'CMAB-UCB-average'),
    ('CMAB-random', 'CMAB_random', '#7E2F8E', 'CMAB-UCB-random'),
    ('DILinUCB-IC', 'DILinUCB-IC', 'green', 'DILinUCB'),
    ('DC-UCB-radius0.1', 'DC-UCB', '#A2142F', 'DC-UCB'),
]
# draw_Reward(fileFolderPath=file_path_ex4, alg_list=alg_list, count=10000, drawType=drawType, issave=True,
#             file_name="Ex4", y_start=2, y_end=16)

alg_list = [
    ('CMAB-average', 'CMAB_average', '#0072BD', 'CMAB-UCB-average'),
    ('CMAB-random', 'CMAB_random', '#7E2F8E', 'CMAB-UCB-random'),
    ('DILinUCB-DC', 'DILinUCB-DC', 'green', 'DILinUCB'),
    ('DC-UCB-radius0.1', 'DC-UCB', '#A2142F', 'DC-UCB'),
    ('DCLinUCB', 'DC-LinUCB', 'palevioletred', 'DC-LinUCB'),
]
# file_path_ex3 = '../SimulationResults/Ex3-15/same-theta-dense/'
# draw_Reward(fileFolderPath=file_path_ex3, alg_list=alg_list, count=5000, drawType=drawType,
#             issave=True, file_name="Ex3")


alg_list = [
    ('DILinUCB', 'DILinUCB', 'green', 'DILinUCB'),
]
file_path_ex3 = '../SimulationResults/Test/same-theta-dense/'
# draw_Reward(fileFolderPath=file_path_ex3, alg_list=alg_list, count=5000, drawType=drawType,
#             issave=True, file_name="Ex3")