"""Salary checker tool, using differential privacy methods."""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from doubt import Boot
import numpy as np
from data import load_data


def main():
    """Main function."""

    # Load data
    data = load_data()

    # Create model
    model = Boot(LinearRegression())

    # Drop unused variables
    columns = ["timestamp", "gender", "danish_national", "bonus"]
    data = data.drop(columns=columns, axis=1)

    # Convert all category variables to their numerical values
    for feat, dtype in data.dtypes.items():
        if dtype == "category":
            data[feat] = data[feat].cat.codes

    # Set up the feature matrix and target vector
    X = data.drop(columns="salary")
    y = data["salary"]

    # Split up the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

    # Fit the scaler and scale the data
    # y_train_expanded = np.expand_dims(y_train, axis=1)
    # scaler = StandardScaler().fit(y_train_expanded)
    # y_train_scaled = scaler.transform(y_train_expanded)

    # Fit the model
    model.fit(X_train, y_train)

    # Print the model score
    preds, intervals = model.predict(X_test, uncertainty=0.05)
    # preds = scaler.inverse_transform(np.expand_dims(preds_scaled, axis=1))[0]
    mse_score = np.abs(preds - y_test).mean()
    containment_score = np.mean(
        (y_test > intervals[:, 0]) & (y_test < intervals[:, 1])
    )
    print(f"Model MAE score: {int(mse_score):,}")
    print(f"Model containment score: {100 * containment_score:.2f}%")

    sample = X[:1]
    prediction, intervals = model.predict(sample, uncertainty=0.05)
    #prediction = scaler.inverse_transform(np.expand_dims(prediction_scaled, axis=1))
    print(f"Sample: {sample}")
    print(f"Prediction: ({int(intervals[0][0]):,}, {int(intervals[0][1]):,}) - {int(prediction[0]):,}")

    breakpoint()


if __name__ == "__main__":
    main()
