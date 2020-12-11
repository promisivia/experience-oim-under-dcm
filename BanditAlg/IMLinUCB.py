from random import random
import numpy as np
import networkx as nx
from BanditAlg.greedy import ArmBaseStruct


class LinUCBUserStruct:
	def __init__(self, featureDimension, lambda_, userID):
		self.userID = userID
		self.d = featureDimension
		self.A = lambda_ * np.identity(n=self.d)
		self.b = np.zeros(self.d)
		self.AInv = np.linalg.inv(self.A)
		self.UserTheta = np.zeros(self.d)
		self.pta_max = 1

	def updateParameters(self, articlePicked_FeatureVector, click):
		self.A += np.dot(articlePicked_FeatureVector, np.transpose(articlePicked_FeatureVector))
		self.b += articlePicked_FeatureVector * click
		temp1 = np.dot(self.AInv, articlePicked_FeatureVector)
		temp2 = np.dot(np.transpose(articlePicked_FeatureVector), self.AInv)
		self.AInv = self.AInv - (np.dot(temp1, temp2)) / (
				1.0 + np.dot(temp2, articlePicked_FeatureVector))

		self.UserTheta = np.dot(self.AInv, self.b)

	def getTheta(self):
		return self.UserTheta

	def getA(self):
		return self.A

	# 返回 U_t(e) 对每条边 upper bound 的估计
	def getProb(self, alpha, article_FeatureVector):
		mean = np.dot(np.transpose(article_FeatureVector), self.UserTheta)
		var = np.sqrt(np.dot(np.dot(np.transpose(article_FeatureVector), self.AInv), article_FeatureVector))
		pta = mean + alpha * var
		if pta > self.pta_max:
			pta = self.pta_max
		return pta


class IMLinUCBAlgorithm:
	def __init__(self, G, P, parameter, seed_size, oracle, dimension, alpha, lambda_, FeatureDic, FeatureScaling, feedback='edge'):
		self.G = G
		self.trueP = P
		self.parameter = parameter
		self.oracle = oracle
		self.seed_size = seed_size
		self.dimension = dimension
		self.alpha = alpha
		self.lambda_ = lambda_
		self.FeatureDic = FeatureDic
		self.FeatureScaling = FeatureScaling
		self.feedback = feedback
		self.currentP = nx.DiGraph()
		self.users = {}  # Nodes
		self.arms = {}
		for u in self.G.nodes():
			self.users[u] = LinUCBUserStruct(dimension, lambda_, u)
			for v in self.G[u]:
				self.arms[(u, v)] = ArmBaseStruct((u, v))
				self.currentP.add_edge(u, v, weight=random())
		self.list_loss = []

	def decide(self):
		S = self.oracle(self.G, self.seed_size, self.currentP)
		return S

	def updateParameters(self, S, live_nodes, live_edges, _iter):
		count = 0
		loss_p = 0
		for u in live_nodes:
			for (u, v) in self.G.edges(u):
				featureVector = self.FeatureScaling * self.FeatureDic[(u, v)]
				if (u, v) in live_edges:
					reward = live_edges[(u, v)]
				else:
					reward = 0
				self.arms[(u, v)].updateParameters(reward=reward)
				self.users[u].updateParameters(featureVector, reward)
				self.currentP[u][v]['weight'] = self.users[v].getProb(self.alpha, featureVector)

				estimateP = self.currentP[u][v]['weight']
				trueP = self.trueP[u][v]['weight']
				loss_p += np.abs(estimateP - trueP)
				count += 1
		self.list_loss.append([loss_p / count])

	def getCoTheta(self, userID):
		return self.users[userID].UserTheta

	def getP(self):
		return self.currentP

	def getLoss(self):
		return np.asarray(self.list_loss)
