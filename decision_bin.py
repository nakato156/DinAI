from sklearn import tree

#           distancia, velocidad 
features = [[8, 12], [8, 12],[0, 12], [-12, 12],[8, 12], [4, 12],[6, 12],[54, 12], [42, 12], [9, 12]]
labels = [1,1,0,0,1,1,1,0,0,1]

classifier = tree.DecisionTreeClassifier()
classifier.fit(features,labels)

class Clasif():
    def play(dist):
        pred = classifier.predict([[dist,12]])
        return pred
