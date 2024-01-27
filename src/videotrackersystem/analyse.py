from videotrackersystem import video
from videotrackersystem.core import logger
import cv2
from videotrackersystem.core import letterbox, get_current_dir
import onnxruntime as ort
import numpy as np
from collections import defaultdict
import os
import argparse
import sys
import pickle


CLASSES = {
    0: "人",
    1: "自行车",
    2: "汽车",
    3: "摩托车",
    4: "飞机",
    5: "公交车",
    6: "火车",
    7: "卡车",
    8: "船",
    9: "交通灯",
    10: "消防栓",
    11: "停车标志",
    12: "停车计时器",
    13: "长凳",
    14: "鸟",
    15: "猫",
    16: "狗",
    17: "马",
    18: "羊",
    19: "牛",
    20: "大象",
    21: "熊",
    22: "斑马",
    23: "长颈鹿",
    24: "背包",
    25: "雨伞",
    26: "手提包",
    27: "领带",
    28: "行李箱",
    29: "飞盘",
    30: "滑雪板",
    31: "单板滑雪",
    32: "运动球",
    33: "风筝",
    34: "棒球棒",
    35: "棒球手套",
    36: "滑板",
    37: "冲浪板",
    38: "网球拍",
    39: "瓶子",
    40: "酒杯",
    41: "杯子",
    42: "叉子",
    43: "刀",
    44: "勺子",
    45: "碗",
    46: "香蕉",
    47: "苹果",
    48: "三明治",
    49: "橙子",
    50: "西兰花",
    51: "胡萝卜",
    52: "热狗",
    53: "披萨",
    54: "甜甜圈",
    55: "蛋糕",
    56: "椅子",
    57: "沙发",
    58: "盆栽",
    59: "床",
    60: "餐桌",
    61: "马桶",
    62: "电视",
    63: "笔记本电脑",
    64: "鼠标",
    65: "遥控器",
    66: "键盘",
    67: "手机",
    68: "微波炉",
    69: "烤箱",
    70: "烤面包机",
    71: "水槽",
    72: "冰箱",
    73: "书",
    74: "时钟",
    75: "花瓶",
    76: "剪刀",
    77: "泰迪熊",
    78: "吹风机",
    79: "牙刷",
}

onnx_model = os.path.join(get_current_dir(), "blackcat-v1.onnx")
iou_thres = 0.5
confidence_thres = 0.5
# sys.stdout.write(f"onnx path: {onnx_model}\n")


def get_video_info(path):
    video_info = video.VideoInfo.from_video_path(path)
    return video_info


def postprocess(output):
        """
        Performs post-processing on the model's output to extract bounding boxes, scores, and class IDs.

        Args:
            output (numpy.ndarray): The output of the model.

        Returns:
            dict: The number of every different class in one frame.
        """
        # Transpose and squeeze the output to match the expected shape
        outputs = np.transpose(np.squeeze(output[0]))
        # Get the number of rows in the outputs array
        rows = outputs.shape[0]
        # Lists to store the bounding boxes, scores, and class IDs of the detections
        boxes = []
        scores = []
        class_ids = []
        
        # Iterate over each row in the outputs array
        for i in range(rows):
            # Extract the class scores from the current row
            classes_scores = outputs[i][4:]

            # Find the maximum score among the class scores
            max_score = np.amax(classes_scores)

            # If the maximum score is above the confidence threshold
            if max_score >= confidence_thres:
                # Get the class ID with the highest score
                class_id = np.argmax(classes_scores)

                # Extract the bounding box coordinates from the current row
                x, y, w, h = outputs[i][0], outputs[i][1], outputs[i][2], outputs[i][3]

                # Calculate the scaled coordinates of the bounding box
                left = int(x - w / 2)
                top = int(y - h / 2)
                width = int(w)
                height = int(h)
                # Add the class ID, score, and box coordinates to the respective lists
                class_ids.append(class_id)
                scores.append(max_score)
                boxes.append([left, top, width, height])

        # Apply non-maximum suppression to filter out overlapping bounding boxes
        indices = cv2.dnn.NMSBoxes(boxes, scores, confidence_thres, iou_thres)

        # Iterate over the selected indices after non-maximum suppression
        result = defaultdict(int)
        for i in indices:
            # Get the box, score, and class ID corresponding to the index
            box = boxes[i]
            score = scores[i]
            class_id = class_ids[i]
            class_name = CLASSES[class_id]
            result[class_name] += 1
        
        return dict(result)



def frame_generator(path, stripe=5):
    # Create an inference session using the ONNX model and specify execution providers
    session = ort.InferenceSession(onnx_model, providers=["CPUExecutionProvider"])

    # Get the model inputs
    model_inputs = session.get_inputs()
    # Store the shape of the input for later use
    input_shape = model_inputs[0].shape
    input_width = input_shape[2]
    input_height = input_shape[3]
    sys.stdout.write(f"model input: width: {input_width}, height: {input_height}\n")

    cap = cv2.VideoCapture(path)
    count = 0
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        count += 1
        if count % stripe != 0:
            continue
        # preprocess
        img_data, _, _ = letterbox(frame)
        image_data = np.array(img_data) / 255.0
        # Transpose the image to have the channel dimension as the first dimension
        image_data = np.transpose(image_data, (2, 0, 1))  # Channel first
        # Expand the dimensions of the image data to match the expected input shape
        image_data = np.expand_dims(image_data, axis=0).astype(np.float32)
        # Run inference using the preprocessed image data
        outputs = session.run(None, {model_inputs[0].name: image_data})
        # Perform post-processing on the outputs to obtain output image.
        frame_ret = postprocess(outputs) 
        # logger.info(frame_ret)
        yield count, frame_ret



if __name__ == "__main__":
    # Create an argument parser to handle command-line arguments
    parser = argparse.ArgumentParser()
    # parser.add_argument("--path", type=str, help="Input your video path.")
    parser.add_argument("--paths", metavar='N', type=str, nargs='+',
                    help='List of path strings')
    parser.add_argument("--stripe", type=int, default=5, help="Stripe.")
    args = parser.parse_args()
    ret = {}

    for path in args.paths:
        sys.stdout.write(f"开始分析:{path}\n{'*'*20}")
        vinfo = get_video_info(path)
        sys.stdout.write(f"width: {vinfo.width}, \nheight: {vinfo.height}, \nfps: {vinfo.fps}, \ntotalFrames:{vinfo.total_frames}")
        ret[path] = []
        for frame_idx, frame_ret in frame_generator(path, vinfo.fps):
            if frame_idx % (vinfo.fps * 10) == 0:
                sys.stdout.write(f"完成: {frame_idx/vinfo.total_frames:.0%}\n")
            if frame_ret:
                sys.stdout.write(f"{frame_ret}")
                ret[path].append([f"{frame_idx}/{vinfo.total_frames}", frame_ret])

        sys.stdout.write(f"完成: 100%\n{'*'*16}")
        with open(os.path.join(get_current_dir(), ".tmp-task.txt"), "wb") as f:
            f.write(pickle.dumps(ret))
