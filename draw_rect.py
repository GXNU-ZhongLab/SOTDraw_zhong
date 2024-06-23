import cv2
import os
from bbox import get_axis_aligned_bbox
from toolkit.datasets import DatasetFactory
import math
import numpy as np
import argparse
import pandas as pd
import matplotlib.pyplot as plt
parser = argparse.ArgumentParser(description='Draw rectangular boxes for Single Object Tracking')
parser.add_argument('--video', default='', type=str, help='eval one special video') #序列的名字，可以为''（此时默认画出数据集的所有序列）
parser.add_argument('--dataset_dir', type=str, default='/home/data/', help='dataset root directory') #数据集的路径
parser.add_argument('--dataset', type=str,default='lasot', help='dataset name') #数据集的名字
parser.add_argument('--tracker_result_dir', type=str, default='./result/', help='tracker result root') #跟踪器的跟踪结果txt文件存放出，里面文件夹命名记得和tracker名字保持一致
parser.add_argument('--trackers',default=['USCLTrack','EVPTrack','SeqTrack','ROMTrack', 'OSTrack'], nargs='+')#跟踪器的名字,按照顺序画跟踪框
# parser.add_argument('--trackers',default=[], nargs='+') #，不放跟踪器时，只画Groudtruth
parser.add_argument('--format', default='png', type=str, help='png, pdf, jpg')
parser.add_argument('--save_dir', default='./output', type=str, help='Save path') #输出保存的路径
parser.add_argument('--gt_draw', dest='gt_draw', default=True, action="store_true")
parser.add_argument('--vis', dest='vis', action='store_true')
args = parser.parse_args()
# OTB100
# CarDark
color = ["yellow", "red", "lime", "blue", "black", "cyan", "pink", "purple", "orange", "turquoise", "slategray"] # 第一个颜色Groudtruth，后面接着是若干个跟踪器
if not os.path.exists(args.save_dir):
    os.makedirs(args.save_dir)
if 'GOT' in args.dataset:
    dataset_root = os.path.join(args.dataset_dir, args.dataset, "test")
else:
    dataset_root = os.path.join(args.dataset_dir, args.dataset)
dataset = DatasetFactory.create_dataset(name=args.dataset, dataset_root=dataset_root, load_img=False)

for v_idx, video in enumerate(dataset):
    if args.video != '':
        if video.name != args.video:
            continue
    if v_idx in [1] or v_idx < 16:
        continue
    pred_bboxes = []
    bboxes = []
    names = []

    for P in args.trackers:
        if "GOT" in args.dataset:
            try:
                bboxes.append(pd.read_csv(os.path.join(args.tracker_result_dir, P, str(video.name), str(video.name) + "_001.txt"), sep='\t|,| ',
                                          header=None, names=['xmin', 'ymin', 'width', 'height'], engine='python'))
                names.append(P.split('/')[-1])
            except:
                print("Please check path")
                print(" GOT result file :{}".format(os.path.join(args.tracker_result_dir, P, str(video.name), str(video.name) + "_001.txt")))
                exit()
        elif "VOT" in args.dataset:
            try:
                bboxes.append(pd.read_csv(os.path.join(args.tracker_result_dir, P, 'baseline', str(video.name), str(video.name) + "_001.txt"), sep='\t|,| ',
                                          header=None, names=['xmin', 'ymin', 'width', 'height'], engine='python'))
                names.append(P.split('/')[-1])
            except:
                print("Please check path")
                print(" GOT result file :{}".format(os.path.join(args.tracker_result_dir, P, 'baseline', str(video.name), str(video.name) + "_001.txt")))
                exit()
        else:
            try:
                bboxes.append(pd.read_csv(os.path.join(args.tracker_result_dir, P, str(video.name) + ".txt"), sep='\t|,| ',
                                              header=None, names=['xmin', 'ymin', 'width', 'height'],engine='python'))
                names.append(P.split('/')[-1])
            except:
                try:
                    name = str(video.name)
                    bboxes.append(
                            pd.read_csv(os.path.join(args.tracker_result_dir, P, str(video.name)[:-2] + "_" + str(video.name)[-1] + ".txt"),
                                        sep='\t|,| ', header=None, names=['xmin', 'ymin', 'width', 'height'], engine='python'))
                    names.append(P.split('/')[-1])
                except:
                    print("Please check path")
                    print("path1:{} or path2:{}".format(os.path.join(args.tracker_result_dir, P, str(video.name) + ".txt"),os.path.join(args.tracker_result_dir, P, str(video.name)[:-2] + "_" + str(video.name)[-1] + ".txt")))
                    exit()

    for idx, (img, gt_bbox) in enumerate(video):
        img = img[..., ::-1]
        plt.imshow(img)
        ax = plt.gca()
        if len(gt_bbox) == 4:
            gt_bbox = [gt_bbox[0], gt_bbox[1],gt_bbox[0], gt_bbox[1] + gt_bbox[3] - 1,
                       gt_bbox[0] + gt_bbox[2] - 1, gt_bbox[1] + gt_bbox[3] - 1, gt_bbox[0] + gt_bbox[2] - 1, gt_bbox[1]]

        if args.gt_draw:
            if "VOT" in args.dataset:
                ax.add_patch(plt.Polygon(np.array(gt_bbox).reshape(-1,2), color=color[0], fill=False, linewidth=3))
            else:
                cx, cy, w, h = get_axis_aligned_bbox(np.array(gt_bbox))
                x1, y1, x2, y2 = int(cx - w / 2 + 1), int(cy - h / 2 + 1), int(cx + w / 2 - 1), int(cy + h / 2 - 1)
                ax.add_patch(plt.Rectangle((x1, y1), x2 - x1 + 1, y2 - y1 + 1, color=color[0], fill=False, linewidth=3))
        for (n, bbox) in enumerate(bboxes):
            try:
                bbox = list(map(int, bbox.iloc[idx].values))
                if not any(map(math.isnan, bbox)):
                    try:
                        ax.add_patch(plt.Rectangle((bbox[0], bbox[1]), bbox[2], bbox[3], color=color[n+1], fill=False, linewidth=3))
                    except:
                        continue
            except:
                continue
        Rdir = os.path.join(args.save_dir, video.name)
        if os.path.exists(Rdir) is False:
            os.makedirs(Rdir)
        image_dir = os.path.join(Rdir, str(idx) + '.' + args.format)
        h, w, d = img.shape
        plt.text(20/500*w, 30/280*h, "#{:06d}".format(idx), fontdict={'color': 'yellow', 'size': math.ceil(15/math.sqrt(500*280)*math.sqrt(w*h))}) #标上第几帧
        plt.axis('off')
        plt.savefig(image_dir, format=args.format, bbox_inches = 'tight',pad_inches = 0)
        if args.vis:
            plt.ioff()
            plt.pause(0.001)
        plt.cla()

