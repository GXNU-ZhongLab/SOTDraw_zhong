import matplotlib.pyplot as plt
import numpy as np
import os

from .draw_utils import COLOR, LINE_STYLE

save_root='./output/quxiantu/' 
if not os.path.exists(save_root):
    os.makedirs(save_root)  # 创建多层目录
    print(f"Directory {save_root} was created.")
else:
    print(f"Directory {save_root} already exists.")

def draw_success_precision(success_ret, name, videos, attr, precision_ret=None,
        norm_precision_ret=None, bold_name=None, axis=[0, 1]):
    # success plot
    fig, ax = plt.subplots()
    # ax.grid(b=True)
    ax.set_aspect(1)
    plt.xlabel('Overlap threshold', fontsize=16)
    plt.ylabel('Success rate', fontsize=16)
    if attr == 'ALL':
        plt.title(r'Success plots of OPE on %s' % (name))
    else:
        plt.title(r'Success plots of OPE - %s' % (attr))
    plt.axis([0, 1]+axis)
    success = {}
    thresholds = np.arange(0, 1.05, 0.05)
    for tracker_name in success_ret.keys():
        value = [v for k, v in success_ret[tracker_name].items() if k in videos]
        success[tracker_name] = np.mean(value)
    #print(success)
    for idx, (tracker_name, auc) in  \
            enumerate(sorted(success.items(), key=lambda x:x[1], reverse=True)):
        if tracker_name == bold_name:
            label = r"[%.3f] %s" % (auc, tracker_name)
        else:
            label = "[%.3f] " % (auc) + tracker_name
        value = [v for k, v in success_ret[tracker_name].items() if k in videos]
        plt.plot(thresholds, np.mean(value, axis=0),
                color=COLOR[idx], linestyle=LINE_STYLE[idx],label=label, linewidth=2)
    ax.legend(loc='lower left', labelspacing=0.2, fontsize=13)
    ax.autoscale(enable=True, axis='both', tight=True)
    xmin, xmax, ymin, ymax = plt.axis()
    ax.autoscale(enable=False)
    ymax += 0.03
    ymin = 0
    plt.axis([xmin, xmax, ymin, ymax])
    plt.xticks(np.arange(xmin, xmax+0.01, 0.1))
    plt.yticks(np.arange(ymin, ymax, 0.1))
    ax.set_aspect((xmax - xmin)/(ymax-ymin))
    #plt.show()
    try:
        output_path = os.path.join(save_root, attr + '-suc.pdf')
        plt.rcParams['text.usetex'] = False
        plt.savefig(output_path)
    except Exception as e:
        print(e)


    if precision_ret:
        # norm precision plot
        fig, ax = plt.subplots()
        # ax.grid(b=True)
        ax.set_aspect(50)
        plt.xlabel('Location error threshold', fontsize=16)
        plt.ylabel('Precision', fontsize=16)
        if attr == 'ALL':
            plt.title(r'Precision plots of OPE on %s' % (name))
        else:
            plt.title(r'Precision plots of OPE - %s' % (attr))
        plt.axis([0, 50]+axis)
        precision = {}
        thresholds = np.arange(0, 51, 1)
        for tracker_name in precision_ret.keys():
            value = [v for k, v in precision_ret[tracker_name].items() if k in videos]
            precision[tracker_name] = np.mean(value, axis=0)[20]
        for idx, (tracker_name, pre) in \
                enumerate(sorted(precision.items(), key=lambda x:x[1], reverse=True)):
            if tracker_name == bold_name:
                label = r"[%.3f] %s" % (pre, tracker_name)
            else:
                label = "[%.3f] " % (pre) + tracker_name
            value = [v for k, v in precision_ret[tracker_name].items() if k in videos]
            plt.plot(thresholds, np.mean(value, axis=0),
                    color=COLOR[idx], linestyle=LINE_STYLE[idx],label=label, linewidth=2)
        ax.legend(loc='lower right', labelspacing=0.2, fontsize=13)
        ax.autoscale(enable=True, axis='both', tight=True)
        xmin, xmax, ymin, ymax = plt.axis()
        ax.autoscale(enable=False)
        ymax += 0.03
        ymin = 0
        plt.axis([xmin, xmax, ymin, ymax])
        plt.xticks(np.arange(xmin, xmax+0.01, 5))
        plt.yticks(np.arange(ymin, ymax, 0.1))
        ax.set_aspect((xmax - xmin)/(ymax-ymin))
        #plt.show()        
        output_path = os.path.join(save_root, attr + '-p.pdf')
        plt.rcParams['text.usetex'] = False
        plt.savefig(output_path)



    # norm precision plot
    if norm_precision_ret:
        fig, ax = plt.subplots()
        # ax.grid(b=True)
        plt.xlabel('Location error threshold', fontsize=16)
        plt.ylabel('Precision', fontsize=16)
        if attr == 'ALL':
            plt.title(r'Normalized Precision plots of OPE on %s' % (name))
        else:
            plt.title(r'Normalized Precision plots of OPE - %s' % (attr))
        norm_precision = {}
        thresholds = np.arange(0, 51, 1) / 100
        for tracker_name in precision_ret.keys():
            value = [v for k, v in norm_precision_ret[tracker_name].items() if k in videos]
            norm_precision[tracker_name] = np.mean(value, axis=0)[20]
        for idx, (tracker_name, pre) in \
                enumerate(sorted(norm_precision.items(), key=lambda x:x[1], reverse=True)):
            if tracker_name == bold_name:
                label = r"[%.3f] %s" % (pre, tracker_name)
            else:
                label = "[%.3f] " % (pre) + tracker_name
            value = [v for k, v in norm_precision_ret[tracker_name].items() if k in videos]
            plt.plot(thresholds, np.mean(value, axis=0),
                    color=COLOR[idx], linestyle=LINE_STYLE[idx],label=label, linewidth=2)
        ax.legend(loc='lower right', labelspacing=0.2, fontsize=13)
        ax.autoscale(enable=True, axis='both', tight=True)
        xmin, xmax, ymin, ymax = plt.axis()
        ax.autoscale(enable=False)
        ymax += 0.03
        ymin = 0
        plt.axis([xmin, xmax, ymin, ymax])
        plt.xticks(np.arange(xmin, xmax+0.01, 0.05))
        plt.yticks(np.arange(ymin, ymax, 0.1))
        ax.set_aspect((xmax - xmin)/(ymax-ymin))
        #plt.show()        
        output_path = os.path.join(save_root, attr + '-pnorm.pdf')
        plt.rcParams['text.usetex'] = False
        plt.savefig(output_path)
        plt.close('all')
    return success

