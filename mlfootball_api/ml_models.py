from sklearn.neighbors import NearestNeighbors


class NearestNeighborsGoals:

    def __init__(self, n=100):
        self.nbrs = NearestNeighbors(n_neighbors=n, algorithm='ball_tree')

    
    def find(self, stats, data):
        self.nbrs.fit(data)
        _, indices = self.nbrs.kneighbors(stats.reshape(1, -1))
        return indices

