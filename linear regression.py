import pandas as pd
Iris_dataset = pd.read_csv("Iris.csv")
Iris_dataset

Iris_dataset.head()

import numpy as np
#here we are using the Batchlinearregression rather than standard linearregression because standard linear regression processes using entire dataset at once which makes so slow for large datasets.
#batchlinearregression divides lage datasets into batches and processes which impoves training efficiency faster.
class BatchLinearRegression:

    def __init__(self, batch_size=32, reg_param=0, max_epochs=100, patience=3):
        self.batch_size = batch_size
        self.reg_param = reg_param
        self.max_epochs = max_epochs
        self.patience = patience

        self.coefs = None  # We're going to store our weights here
        self.intercept = None  # And the bias term here
        self.best_coefs = None
        self.best_intercept = None


    def fit(self, data_inputs, data_outputs, batch_size=32, reg_param=0, max_epochs=100, patience=3): #fit method is used to train the model .
        num_rows, num_feats = data_inputs.shape
        self.coefs = np.zeros((num_feats, 1))
        self.intercept = 0


        val_split = int(num_rows * 0.1)
        train_inputs, val_inputs = data_inputs[val_split:], data_inputs[:val_split]
        train_outputs, val_outputs = data_outputs[val_split:], data_outputs[:val_split]


        best_val_loss = float('inf')
        no_progress_epochs = 0
        all_losses = []

        for epoch in range(max_epochs):

            for start_idx in range(0, len(train_inputs), batch_size):
                batch_in = train_inputs[start_idx:start_idx + batch_size]
                batch_out = train_outputs[start_idx:start_idx + batch_size]

                preds = self.predict(batch_in)
                errors = preds - batch_out      #here we calculate error

                grad_weights = (1 / batch_size) * np.dot(batch_in.T, errors) + (reg_param * self.coefs)
                grad_bias = (1 / batch_size) * np.sum(errors)

                self.coefs -= 0.01 * grad_weights   # here 0.01 is learning rate--> learning rate is the step size for the model.
                self.intercept -= 0.01 * grad_bias

            val_predictions = self.predict(val_inputs)
            val_loss = np.mean((val_outputs - val_predictions) ** 2)
            all_losses.append(val_loss)

            if val_loss < best_val_loss:
                best_val_loss = val_loss
                self.best_coefs = self.coefs.copy()
                self.best_intercept = self.intercept
                no_progress_epochs = 0
            else:
                no_progress_epochs += 1

            if no_progress_epochs >= patience:
                print(f"Early stopping at epoch {epoch}")
                break

        self.coefs = self.best_coefs
        self.intercept = self.best_intercept
        return all_losses

    def predict(self, data_inputs):    #predict method makes predictions using trained model .
        return np.dot(data_inputs, self.coefs) + self.intercept

    # here we Calculate mean squared error
    def score(self, data_inputs, data_outputs):    #score method looks the model performance .
        predictions = self.predict(data_inputs)
        mse = np.mean((data_outputs - predictions) ** 2)
        return mse

    def save_model(self, file_name):   #saves the model
        np.savez(file_name, coefs=self.coefs, intercept=self.intercept)

    def load_model(self, file_name):   #load method stores the progress of model and retreives the model progress where you stop .It ensures no need to start the training process again.
        loaded_params = np.load(file_name)
        self.coefs = loaded_params['coefs']
        self.intercept = loaded_params['intercept']
