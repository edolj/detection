import cv2
import numpy as np
import glob
import os
from pathlib import Path
import json
from preprocessing.preprocess import Preprocess
from metrics.evaluation import Evaluation

class EvaluateAll:

    def __init__(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))

        with open('config.json') as config_file:
            config = json.load(config_file)

        self.images_path = config['images_path']
        self.annotations_path = config['annotations_path']
        self.prediction_path = config['prediction_path']

    def get_annotations(self, annot_name):
            with open(annot_name) as f:
                lines = f.readlines()
                annot = []
                for line in lines:
                    l_arr = line.split(" ")[1:5]
                    l_arr = [int(i) for i in l_arr]
                    annot.append(l_arr)
            return annot

    def run_evaluation(self):

        im_list = sorted(glob.glob(self.images_path + '/*.png', recursive=True))
        iou_arr = []
        preprocess = Preprocess()
        eval = Evaluation()
        
        # import detectors.your_super_detector.detector as super_detector
        import detectors.cascade_detector.detector as leftEar_detector
        cascade_detectorL = leftEar_detector.Detector()
        
        import detectors.cascade_detector2.detector as rightEar_detector
        cascade_detectorR = rightEar_detector.Detector2()

        for im_name in im_list:
            
            # Read an image
            img = cv2.imread(im_name)

            # Apply some preprocessing
            #img = preprocess.histogram_equlization_rgb(img) # This one makes VJ worse
            #img = preprocess.grayscale(img)
            #img = preprocess.sharpen(img)
            #img = preprocess.downscale(img)
            #img = preprocess.upscale(img)

            # Run the detector. It runs a list of all the detected bounding-boxes. 
            # Uncomment to use cascade detectors.
            """
            prediction_listL = cascade_detectorL.detect(img)
            prediction_listR = cascade_detectorR.detect(img)
            prediction_list = []
            for x in prediction_listL:
                prediction_list.append(x)
            for y in prediction_listR:
                prediction_list.append(y)
            prediction_list = np.array(prediction_list)
            """

            # Uncomment to get Yolo annotations
            prediction_name = os.path.join(self.prediction_path, Path(os.path.basename(im_name)).stem) + '.txt'
            prediction_list = self.get_annotations(prediction_name)
            #print(prediction_list)

            # Read annotations:
            annot_name = os.path.join(self.annotations_path, Path(os.path.basename(im_name)).stem) + '.txt'
            annot_list = self.get_annotations(annot_name)

            # Only for detection:
            p, gt = eval.prepare_for_detection(prediction_list, annot_list)
            
            iou = eval.iou_compute(p, gt)
            iou_arr.append(iou)

        miou = np.average(iou_arr)
        print("\n")
        print("Average IOU:", f"{miou:.2%}")
        print("\n")

if __name__ == '__main__':
    ev = EvaluateAll()
    ev.run_evaluation()
