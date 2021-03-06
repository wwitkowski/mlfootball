import pandas as pd
import numpy as np
import tensorflow as tf
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.neighbors import NearestNeighbors
from scipy.stats import poisson, skellam
from tensorflow.python.lib.io.file_io import stat

class NearestNeighborsGoals:
    def __init__(self, n=100, radius=2):
        self.n = n
        self.radius = radius
        self.nbrs = NearestNeighbors(n_neighbors=self.n, radius=self.radius, algorithm='ball_tree')

    
    def find(self, stats, data):
        self.nbrs.fit(data)
        radius_indices = self.nbrs.radius_neighbors(stats.reshape(1, -1), return_distance=False)
        if len(radius_indices[0]) < self.n:
            indices = self.nbrs.kneighbors(stats.reshape(1, -1), return_distance=False)
            return indices[0]
        else:
            return radius_indices[0]


class FootballPoissonModel():
	def __init__(self):
		pass


	def fit(self, df):
		data = pd.concat([df[['team1', 'team2', 'score1']].assign(home=1).rename(
						 columns={'team1': 'team', 'team2': 'opponent', 'score1': 'goals'}),
						 df[['team2', 'team1', 'score2']].assign(home=0).rename(
						 columns={'team2': 'team', 'team1': 'opponent', 'score2': 'goals'})])
		self.model = smf.glm(formula="goals ~ home + team + opponent", data=data, 
							 family=sm.families.Poisson()).fit()


	@property
	def summary(self):
		return self.model.summary()


	def predict_goals(self, data):
		home_goals_pred = self.model.predict(data.assign(home=1).rename(
						columns={'team1': 'team', 'team2': 'opponent'}))
		away_goals_pred = self.model.predict(data.assign(home=0).rename(
						columns={'team2': 'team', 'team1': 'opponent'}))

		return home_goals_pred, away_goals_pred


	@staticmethod
	def predict_chances(home_goals, away_goals, max_goals=10):
		team_pred = [[poisson.pmf(i, team_avg) for i in range(0, max_goals + 1)] for team_avg in [home_goals, away_goals]]
		match_pred = [[np.outer(np.array([i[j] for i in team_pred[0]]), np.array([i[j] for i in team_pred[1]]))] for j in range(0, np.shape(team_pred)[2])]
		res = [[np.sum(np.tril(match_pred[i][0], -1)), np.sum(np.diag(match_pred[i][0])), np.sum(np.triu(match_pred[i][0], 1))] for i in range(0, len(match_pred))]
		return zip(*res)

	@staticmethod
	def predict_overs(home_goals, away_goals, max_goals=10):
		team_pred = [[poisson.pmf(i, team_avg) for i in range(0, max_goals + 1)] for team_avg in [home_goals, away_goals]]
		match_pred = [[np.outer(np.array([i[j] for i in team_pred[0]]), np.array([i[j] for i in team_pred[1]]))] for j in range(0, np.shape(team_pred)[2])]
		res = [[np.sum(np.triu(np.fliplr(match_pred[i]), -7)), np.sum(np.tril(np.fliplr(match_pred[i]), -8))] for i in range(0, len(match_pred))]
		return zip(*res)

	@staticmethod
	def predict_btts(home_goals, away_goals, max_goals=10):
		team_pred = [[poisson.pmf(i, team_avg) for i in range(0, max_goals + 1)] for team_avg in [home_goals, away_goals]]
		match_pred = [[np.outer(np.array([i[j] for i in team_pred[0]]), np.array([i[j] for i in team_pred[1]]))] for j in range(0, np.shape(team_pred)[2])]
		#res = [[np.sum(match_pred[i]), -7)), np.sum(np.tril(np.fliplr(match_pred[i]), -8))] for i in range(0, len(match_pred))]

		return 1

		

class NeuralNetworkModel():
	def __init__(self, n_features=None, path=None, activations=('relu', 'relu'), nodes=(50, 50), batch_size=256, dropout=None, optimizer='adam', loss='mse', metrics=['mse'], bias=None):
		self.path = path
		self.batch_size = batch_size

		if self.path is not None:
			self.model = tf.keras.models.load_model(self.path)
		else:
			self._build(n_features=n_features, activations=activations, nodes=nodes, dropout=dropout, optimizer=optimizer, loss=loss, metrics=metrics, bias=bias)


	def _build(self, n_features, activations=('relu', 'relu'), nodes=(50, 50), dropout=None, optimizer='adam', loss='mse', metrics=['mse'], bias=None):
		optimizer = optimizer
		#loss = tf.keras.losses.MeanAbsoluteError()
		loss = loss
		metrics = metrics
		if bias is not None:
				bias = tf.keras.initializers.Constant(bias)

		self.model = tf.keras.Sequential()
		# First layer
		self.model.add(tf.keras.layers.Dense(nodes[0], activation=activations[0], input_shape=(n_features,)))
		# Hidden layers
		for i in range(1, len(activations)):
			self.model.add(tf.keras.layers.Dense(nodes[i], activation=activations[i]))
		if dropout:
			self.model.add(tf.keras.layers.Dropout(dropout))
		# Output layer
		self.model.add(tf.keras.layers.Dense(1, activation='exponential', bias_initializer=bias))
		self.model.compile(
			optimizer=optimizer,
			loss=loss,
			metrics=metrics)


	def fit(self, X_train, y_train, X_val, y_val, verbose=1, epochs=200):
		early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=50, restore_best_weights=True, verbose=0)

		self.history = self.model.fit(X_train, y_train,
									  batch_size=self.batch_size,
									  verbose=verbose,
									  epochs=epochs,
									  callbacks=[early_stopping],
									  validation_data=(X_val, y_val))

		return self.history


	def predict(self, X):
		y_pred = self.model.predict(X)

		return y_pred


	def save_model(self, path):
		self.model.save(f'{path}.hdf5')


	@property
	def summary(self):
		return self.model.summary()

