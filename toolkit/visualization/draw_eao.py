import matplotlib.pyplot as plt
import numpy as np
import pickle

from matplotlib import rc
from ..visualization.draw_utils import COLOR, MARKER_STYLE

rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

def draw_eao(result):
    attrs = []
    res = {}
    for i, (attr, ret) in enumerate(result.items()):
        attrs.append(attr)
        for i, (tracker_name, val) in enumerate(ret.items()):
            if tracker_name not in res.keys():
                res.update({tracker_name:{}})
            res[tracker_name].update({attr:val})
    result = res
    fig = plt.figure(figsize=(13, 11)) #9.1, 8.4
    ax = fig.add_subplot(111, projection='polar')
    angles = np.linspace(0, 2*np.pi, 16, endpoint=True)

    attr2value = []
    for i, (tracker_name, ret) in enumerate(result.items()):
        value = list(ret.values())
        attr2value.append(value)
        value.append(value[0])
    attr2value = np.array(attr2value)
    max_value = np.max(attr2value, axis=0)
    min_value = np.min(attr2value, axis=0)
    for i, (tracker_name, ret) in enumerate(result.items()):
        value = list(ret.values())
        value.append(value[0])
        value = np.array(value)
        value *= (1 / max_value)
        plt.plot(angles, value, linestyle='-', color=COLOR[i], marker=MARKER_STYLE[i],
                label=tracker_name, linewidth=2)
                
    # attrs = ["Overall", "Camera motion",
    #          "Illumination change","Motion Change",
    #          "Size change","Occlusion",
    #          "Unassigned"]
    attr_value = []
    for attr, maxv, minv in zip(attrs, max_value, min_value):
        attr_value.append(attr + "\n({:.3f},{:.3f})".format(minv, maxv))
    ax.set_thetagrids(angles=angles[:-1] * 180/np.pi, labels=attr_value, fontsize=20)
    ax.tick_params(axis='x', pad=18)#属性标签远离圆心
    ax.spines['polar'].set_visible(False)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, - 0.15), frameon=True, ncol=5, fontsize=19, handletextpad=0.01,)#图例 
    ax.set_yticks([0.6,0.7,0.8,0.9,1.0])
    ax.set_yticklabels([''] * len(ax.get_yticklabels()))
    plt.grid(True, c='gray', linestyle='--', linewidth=0.8)

    ax.set_ylim(0.8, 1.03)
    plt.show()
    plt.savefig('./eao.pdf', dpi=810)

if __name__ == '__main__':
    result = pickle.load(open("../../result.pkl", 'rb'))
    draw_eao(result)
