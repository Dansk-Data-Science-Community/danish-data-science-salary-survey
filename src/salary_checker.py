"""Salary checker tool, using differential privacy methods."""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from diffprivlib.models import LinearRegression
from data import load_data


def main():
    """Main function."""

    # Load data
    data = load_data()

    # Create model
    model = LinearRegression()

    # Drop unused variables
    columns = ["timestamp", "gender", "danish_national", "bonus"]
    data = data.drop(columns=columns, axis=1)

    # Convert all category variables to their numerical values
    for feat, dtype in data.dtypes.items():
        if dtype == "category":
            data[feat] = data[feat].cat.codes

    # Set up the feature matrix
    X = data.drop(columns="salary")

    # Set up the target vector
    y = StandardScaler().fit_transform(data.salary)

    # Split up the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

    # Fit the model
    model.fit(X_train, y_train)

    # Print the model score
    score = model.score(X_test, y_test)
    print("Model score:", score)

    sample = X[:1]
    print("Sample:", sample)
    print("Prediction:", model.predict(sample))

    breakpoint()


if __name__ == "__main__":
    main()
