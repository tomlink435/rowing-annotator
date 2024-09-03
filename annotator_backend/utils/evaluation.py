"""标注质量标准"""
import math


def get_score():
    return 1


"""
    标注方式: 定位分类
    todo: 合并多人标注结果，标注同一目标区域左上角坐标和长宽平均值，删除歧义目标
"""


def merge_locate_result(results):
    length = len(results)
    if length == 1:
        return results
    # 合并结果
    merge_results = []
    # 暴力循环
    for i in range(0, length):
        for result_1 in eval(results[i]["result"]):
            # 满足条件的结果放入temp_result数组中，若数量大于标注次数的1/2,则认为标注有效，结算最终结果
            temp_result = [result_1]
            print("初始temp_result", temp_result)
            # 横纵坐标阈值
            threshold_Y = result_1["coordinate"]["height"] * 0.3 if result_1["coordinate"][
                                                                        "height"] * 0.3 < 50 else 50
            threshold_X = result_1["coordinate"]["width"] * 0.3 if result_1["coordinate"]["width"] * 0.3 < 50 else 50
            for j in range(0, length):
                if i == j:
                    continue
                for result_2 in eval(results[j]["result"]):
                    if is_locate_same_object(result_1, result_2, threshold_X, threshold_Y):
                        temp_result.append(result_2)
                        print("符合条件", result_2)
                # 满足条件的标注结果 >= 标注次数的 1/2,则任务标注有效
            if len(temp_result) >= math.ceil(length / 2):
                avg_x = int(sum(item["coordinate"]['x'] for item in temp_result) / len(temp_result))
                avg_y = int(sum(item["coordinate"]['y'] for item in temp_result) / len(temp_result))
                avg_width = int(sum(item["coordinate"]['width'] for item in temp_result) / len(temp_result))
                avg_height = int(sum(item["coordinate"]['height'] for item in temp_result) / len(temp_result))
                avg_result = {"coordinate": {"x": avg_x, "y": avg_y, "width": avg_width, "height": avg_height},
                              "tag_id": temp_result[0]["tag_id"]}
                for item in temp_result:
                    print("temp_result_list:", item)
                print("avg_result:", avg_result)
                is_existed = False
                for merge_result in merge_results:
                    if is_locate_same_object(avg_result, merge_result, threshold_X, threshold_Y):
                        is_existed = True
                if not is_existed:
                    merge_results.append(avg_result)
            for item in merge_results:
                print(item)
            print("==========================================")
    print(len(merge_results))
    print(merge_results)
    return merge_results


"""
    判断是否标注了同一个目标
"""


def is_locate_same_object(locate_result1, locate_result2, threshold_X, threshold_Y):
    if abs(locate_result1["coordinate"]["x"] - locate_result2["coordinate"]["x"]) < threshold_X and abs(
            locate_result1["coordinate"]["y"] - locate_result2["coordinate"]["y"]) < threshold_Y and abs(
        locate_result1["coordinate"]["height"] - locate_result2["coordinate"]["height"]) < threshold_Y and abs(
        locate_result1["coordinate"]["width"] - locate_result2["coordinate"]["width"]) < threshold_X and \
            locate_result1["tag_id"][0] == locate_result2["tag_id"][0]:
        return True
    else:
        return False
