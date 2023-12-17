from flask import Flask,request,render_template,jsonify
import os
import pandas as pd


app = Flask(__name__)


csv_filePath=os.path.join('predictionsCSV',"prediction.csv")

@app.route('/', methods=['GET'])
def index():
    app.logger.info("call the main route")
    response = jsonify({
        "message": "use predict route to get predictions",
    })
    response.status_code = 200
    return response


@app.route('/predict', methods=['POST'])
def predict():
    # Get data from POST request
    data = request.get_json()

    # Load existing predictions from CSV
    if os.path.exists(csv_filePath):
        df = pd.read_csv(csv_filePath)
    else:
        df = pd.DataFrame(columns=["Age", "Mileage", "Engine_Capacity", "Model", "Fuel_Type", "Transmission"])

    # Append new prediction to dataframe
    new_data = pd.DataFrame([{**data}], columns=df.columns)
    df = pd.concat([df, new_data], ignore_index=True)
    
    # Save dataframe to CSV
    df.to_csv(csv_filePath, index=False)

    return {"prediction": "prediction"}

                    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port,debug=True)    

