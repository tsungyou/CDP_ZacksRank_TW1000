import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# euclidean
points = {
  "blue": [[1, 2], [2, 2], [4, 2], [6, 2], [3, 3]],
  "red": [[4, 4], [2, 5], [3, 4], [1, 1], [4, 5]],          
}
fit_point = [3, 3]
class KNearestNeighbors:
    
    def __init__(self, points, k = 3):
        self.k = k
        self.points = points
    
    def distance(self, point, test_data, type="euclidean"):
        if type == "euclidean":
            result = np.sqrt(np.sum((np.array(point) - np.array(test_data))**2))
            # print(result)

        else:
            pass
        return result    
    def fit(self, test_data):
        res = {}
        # print(self.points)
        # print(len(self.points))
        for category in self.points:
            # print("=========")
            # print(category)            

            for _ in self.points[category]:
                distance = self.distance(_, test_data, type="euclidean")
                res[distance] = category
        return res
    def sort_get_result(self, res):
        df = pd.DataFrame(res.values(), index=res.keys())
        sort_df = df.sort_index()
        classification = sort_df.iloc[:self.k, 0]
        max_category = np.max(classification)
        # print(classification)
        print(max_category)
        return max_category
clf = KNearestNeighbors(points)
a = clf.fit(fit_point)
test_data_cate = clf.sort_get_result(a)

ax = plt.subplot()

for point in points['red']:
    ax.scatter(point[0], point[1], color = "red")
    
for point in points['blue']:
    ax.scatter(point[0], point[1], color = "blue")

ax.plot(fit_point[0], fit_point[1], color = "yellow", marker="*")
plt.show()