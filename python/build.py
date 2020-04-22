import onnxruntime as rt
import numpy

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression

from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

# load and split the iris data
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y)

print("Test Data")
print(X_test)
print()

print("Test Labels")
print(y_test)
print()

# build a model
clr = LogisticRegression(max_iter=5000)
clr.fit(X_train, y_train)

# make some predictions and report them
y_pred = clr.predict(X_test.astype(numpy.float32))
print("Predictions")
print(y_pred)
print()

# evaluate
print("Evaluation")
print(classification_report(y_test, y_pred))
print()

# convert to model to ONNX
initial_type = [('float_input', FloatTensorType([None, 4]))]
onx = convert_sklearn(clr, initial_types=initial_type)
with open("logreg_iris.onnx", "wb") as f:
  f.write(onx.SerializeToString())

# run and test the ONNX model
sess = rt.InferenceSession("logreg_iris.onnx")
input_name = sess.get_inputs()[0].name
label_name = sess.get_outputs()[0].name
pred_onx = sess.run([label_name], {input_name: X_test.astype(numpy.float32)})[0]

print("ONNX Predictions")
print(pred_onx)
print()
