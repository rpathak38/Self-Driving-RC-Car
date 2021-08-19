import math
import cv2
import numpy as np

fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
edge_output = cv2.VideoWriter("edges.avi", fourcc, 60, (640, 360))
lanes_output = cv2.VideoWriter("lanes.avi", fourcc, 60, (640, 360))


def region_of_interest(img, vertices=None):
    if vertices is None:
        height = img.shape[0]
        width = img.shape[1]
        vertices = [(0, height), (0, height - 100), (width / 2, height / 2), (width, height - 100), (width, height)]

    mask = np.zeros_like(img)
    match_mask_color = (255, 255, 255)
    mask = cv2.fillPoly(mask, np.array([vertices], np.int32), match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)

    return masked_image


def auto_lines(img, debug_mode=False):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    edges = region_of_interest(edges)
    lines = cv2.HoughLinesP(edges, rho=1, theta=math.pi / 180, threshold=100, minLineLength=50, maxLineGap=30)

    if debug_mode:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 8)

        edge_output.write(edges)
        lanes_output.write(img)
    return lines


def line_to_angle_sieve(lines):
    line_angles = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = math.atan((y2 - y1) / (x2 - x1))
        if angle < 0:
            angle += math.pi
        line_angles.append(angle)

    line_angles.sort()
    storage_sets = []
    curr_index = -1
    prev_angle = None
    for angle in line_angles:
        if curr_index == -1:
            storage_sets.append({angle})
            curr_index = curr_index + 1
            prev_angle = angle

        elif math.fabs(prev_angle - angle) <= math.pi / 36:
            storage_sets[curr_index].add(angle)
            prev_angle = angle

        else:
            storage_sets.append({angle})
            curr_index = curr_index + 1
            prev_angle = angle

    storage_sets = [sum(i) / len(i) for i in storage_sets]
    if len(storage_sets) != 2:
        print("WARNING: Detected more than 2 lanes. Check edge maps for confounding objects.")
    return storage_sets


def suggested_path(img, debug_mode=False):
    possible_lanes = auto_lines(img, debug_mode)
    lane_angles = line_to_angle_sieve(possible_lanes)
    lane_unit_vectors = [(math.cos(i), math.sin(i)) for i in lane_angles]
    path_vector = (sum([x[0] for x in lane_unit_vectors]), sum(x[1] for x in lane_unit_vectors))

    ret_angle = math.atan(path_vector[1] / path_vector[0])
    if ret_angle < 0:
        ret_angle += math.pi
    ret_angle = ret_angle * 180 / math.pi

    # print(path_vector)

    path_vector = int(path_vector[0] * 80), int(path_vector[1] * 80)
    height = int(img.shape[0])
    width = int(img.shape[1])
    cv2.arrowedLine(img, (path_vector[0] + width // 2, path_vector[1] + height // 2),
                    (int(width // 2), int(height // 2)),
                    (0, 0, 255), thickness=16, tipLength=0.2)
    return img, int(ret_angle)


if __name__ == "__main__":
    image = cv2.imread("laneImage.jpg")
    print(suggested_path(image, True)[1])
    cv2.imshow("image", image)
    cv2.waitKey()
    cv2.destroyAllWindows()
