from visualizationTools.drawBaseFunction import *

drawType = "Average"  # "Cumulative" "Average" "Default"

alg_list = [
    ('UCB', 'UCB', 'orange', 'UCB'),
    ('CMAB-average', 'CMAB_average', '#0072BD', 'CMAB-UCB-average'),
    ('CMAB-random', 'CMAB_random', '#7E2F8E', 'CMAB-UCB-random'),
    ('DILinUCB-DC', 'DILinUCB-DC', 'green', 'DILinUCB'),
    ('DC-UCB-radius0.1', 'DC-UCB', '#A2142F', 'DC-UCB'),
    # ('DCLinUCB', 'DC-LinUCB', 'palevioletred', 'DC-LinUCB'),
    ('IMFB', 'IMFB', 'black', 'IMFB'),
    ('CUCB', 'CUCB', '#EDB120', 'CUCB(IC)'),
]

dataset_list = ['Small1', 'Small2']  # [ ]
scale_list = ['0.8_10000', '0.2_10000', '0.5_10000']
# ['0.8_10000', '0.2_10000', '0.5_10000', '0.1-0.5_10000', '0.3-0.7_10000', ]
for dataset in dataset_list:
    for scale in scale_list:
        file_path_ex1 = '../SimulationResults/Ex1/' + dataset + '_' + scale + '/'
        # if dataset == 'Small2':
        #     print(dataset, scale)
        #     draw_Reward(fileFolderPath=file_path_ex1, alg_list=alg_list, count=10000, drawType=drawType,
        #                 issave=True, file_name="Ex1_" + dataset + scale, subTitile='(d) 20 nodes, 51 edges')
        # else:
        #     print(dataset, scale)
        #     draw_Reward(fileFolderPath=file_path_ex1, alg_list=alg_list, count=10000, drawType=drawType,
        #                 issave=True, file_name="Ex1_" + dataset + scale, subTitile='(c) 10 nodes, 13 edges')

alg_list = [
    ('CUCB', 'CUCB', '#EDB120', 'CUCB(IC)'),
    ('CMAB-average', 'CMAB_average', '#0072BD', 'CMAB-UCB-average'),
    ('CMAB-random', 'CMAB_random', '#7E2F8E', 'CMAB-UCB-random'),
    ('DILinUCB-IC', 'DILinUCB-IC', 'green', 'DILinUCB'),
    ('DC-UCB-radius0.1', 'DC-UCB', '#A2142F', 'DC-UCB'),
    # ('IMFB', 'IMFB', 'black', 'IMFB'),
]
dataset = 'Flickr_'
prob = 0.8
file_path_ex2 = '../SimulationResults/Ex2/' + dataset + 'p=' + str(prob) + '/'
# draw_Reward(fileFolderPath=file_path_ex2, alg_list=alg_list, count=2000, drawType=drawType, issave=True, file_name="Ex2_"+dataset+"p=" + str(prob), subTitile="(a) p=" + str(prob),)

file_path_ex4 = '../SimulationResults/Ex4/Flixster/'
alg_list = [
    ('CUCB', 'CUCB', '#EDB120', 'CUCB(IC)'),
    ('CMAB-average', 'CMAB_average', '#0072BD', 'CMAB-UCB-average'),
    ('CMAB-random', 'CMAB_random', '#7E2F8E', 'CMAB-UCB-random'),
    # ('DILinUCB-IC', 'DILinUCB-IC', 'green', 'DILinUCB'),
    ('DC-UCB-radius0.1', 'DC-UCB', '#A2142F', 'DC-UCB'),
]
draw_Reward(fileFolderPath=file_path_ex4, alg_list=alg_list, count=10000, drawType=drawType, issave=True,
            file_name="Ex4_Flixster_withoutDILin")

alg_list = [
    ('CMAB-average', 'CMAB_average', '#0072BD', 'CMAB-UCB-average'),
    ('CMAB-random', 'CMAB_random', '#7E2F8E', 'CMAB-UCB-random'),
    ('DILinUCB-DC', 'DILinUCB-DC', 'green', 'DILinUCB'),
    ('DC-UCB-radius0.1', 'DC-UCB', '#A2142F', 'DC-UCB'),
    ('DCLinUCB', 'DC-LinUCB', 'palevioletred', 'DC-LinUCB'),
]
dataset = 'NetHEPT'
type = '0.3-0.7'
file_path_ex3 = '../SimulationResults/Ex3/' + dataset + '-' + type + '/'
# draw_Reward(fileFolderPath=file_path_ex3, alg_list=alg_list, count=10000, drawType=drawType, issave=True,
#             file_name="Ex3" + dataset + '-' + type)

######################################################
# Flickr same
# algo: DC-UCB-radius0.1 average is 187.0 algo: DCLinUCB average is 188.0
# Flickr random 212.0 213.0
# NetHEPT 96.375 96.0
# NetHEPT random 118.0 117.0
#####################################################
alg_list = [
    ('DILinUCB', 'DILinUCB', 'green', 'DILinUCB'),
]
file_path_ex3 = '../SimulationResults/Test/same-theta-dense/'
# draw_Reward(fileFolderPath=file_path_ex3, alg_list=alg_list, count=5000, drawType=drawType,
#             issave=True, file_name="Ex3")
