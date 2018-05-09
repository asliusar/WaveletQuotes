import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures


def predictNextValue(indicator, degree=2):
    indexes = np.arange(len(indicator))
    model = Pipeline([('poly', PolynomialFeatures(degree)),
                      ('linear', LinearRegression(fit_intercept=False))])

    model = model.fit(indexes[:, np.newaxis], indicator)
    return model.predict(len(indicator))
