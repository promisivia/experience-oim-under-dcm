from visualizationTools.drawBaseFunction import *
from visualizationTools.average import average

drawType = "Average"  # "Cumulative" "Average" "Default"

# alg_list = [
#     ('UCB', 'UCB', 'orange', 'UCB'),
#     ('CMAB-average', 'CMAB_average', '#0072BD', 'CMAB-UCB-average'),
#     ('CMAB-random', 'CMAB_random', '#7E2F8E', 'CMAB-UCB-random'),
#     ('DILinUCB-DC', 'DILinUCB-DC', 'green', 'DILinUCB'),
#     ('DC-UCB-radius0.1', 'DC-UCB', '#A2142F', 'DC-UCB(ours)'),
# ]
#
# dataset_list = ['Small-choosen']
# scale_list = ['0.1-0.5', '0.5-0.9', '0.3-0.7']
# for dataset in dataset_list:
#     for scale in scale_list:
#         file_path_ex1 = '../SimulationResults/Ex1/' + dataset + '/' + scale + '/'
#         print(dataset, scale)
#         draw_Reward(fileFolderPath=file_path_ex1, alg_list=alg_list, count=10000, drawType=drawType,
#                     issave=True, file_name="Ex1_" + dataset + '_' + scale, subTitile="Ex1_" + dataset + '_' + scale)

# with scale
# dataset = 'Small-choosen'
# scale = '0.1-0.5'
# file_path_ex1 = '../SimulationResults/Ex1/' + dataset + '/' + scale + '/'
# draw_Reward(fileFolderPath=file_path_ex1, alg_list=alg_list, count=10000, drawType=drawType,
#             issave=True, file_name="Syn_01_05", subTitile='(b) p ∈ [0.1, 0.5]', y_start=7, y_end=10)

# scale = '0.3-0.7'
# file_path_ex1 = '../SimulationResults/Ex1/' + dataset + '/' + scale + '/'
# draw_Reward(fileFolderPath=file_path_ex1, alg_list=alg_list, count=10000, drawType=drawType,
#             issave=True, file_name="Syn_03_07", subTitile='(c) p ∈ [0.3, 0.7]', y_start=14, y_end=17.5)
#
# scale = '0.5-0.9'
# file_path_ex1 = '../SimulationResults/Ex1/' + dataset + '/' + scale + '/'
# draw_Reward(fileFolderPath=file_path_ex1, alg_list=alg_list, count=10000, drawType=drawType,
#             issave=True, file_name="Syn_05_09", subTitile='(d) p ∈ [0.5, 0.9]', y_start=18, y_end=19.5)

alg_list = [
    ('DC-UCB-radius0.1', 'DC-UCB', '#A2142F', 'DC-UCB'),
    # ('CMAB-random', 'CMAB_random', '#7E2F8E', 'CMAB-UCB-random'),
    # ('CMAB-average', 'CMAB_average', '#0072BD', 'CMAB-UCB-average'),
    # ('DILinUCB-IC', 'DILinUCB-IC', 'green', 'DILinUCB'),
    # ('CUCB', 'CUCB', '#EDB120', 'CUCB(IC)'),
    # ('IMFB', 'IMFB', 'black', 'IMFB'),
    # ('IMLinUCB', 'IMLinUCB', 'black', 'IMFB'),
]
dataset_list = ['NetHEPT_', 'Flickr_']
scale_list = [ 0.8]
# dataset_list = ['NetHEPT_']
# scale_list = [0.2]
for dataset in dataset_list:
    for prob in scale_list:
        print(dataset, prob)
        file_path_ex2 = '../SimulationResults/Ex2/' + dataset + 'p=' + str(prob) + '/'
        # average(fileFolderPath=file_path_ex2, alg_list=alg_list, count=800, drawType=drawType, issave=True,
        #         file_name="Ex2_" + dataset + "p=" + str(prob), subTitile="(a) p=" + str(prob), )

alg_list = [
    # ('CMAB-random', 'CMAB_random', '#7E2F8E', 'CMAB-UCB-random'),
    # ('CMAB-average', 'CMAB_average', '#0072BD', 'CMAB-UCB-average'),
    # ('DILinUCB-DC', 'DILinUCB-DC', 'green', 'DILinUCB'),
    ('DC-UCB-radius0.1', 'DC-UCB', '#A2142F', 'DC-UCB'),
]

list = ['NetHEPT-0.1-0.5', 'NetHEPT-0.3-0.7', 'NetHEPT-0.5-0.9', 'Flickr-0.1-0.5', 'Flickr-0.3-0.7', 'Flickr-0.5-0.9']
# list = ['Flickr-0.3-0.7', 'NetHEPT-0.3-0.7']
for type in list:
    print(type)
    file_path_ex3 = '../SimulationResults/Ex3/' + type + '/'
    average(fileFolderPath=file_path_ex3, alg_list=alg_list, count=800, drawType=drawType, issave=True,
            file_name="Ex3" + type)
