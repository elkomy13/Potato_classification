# Potato Disease Classification

A machine learning application for classifying potato plant diseases using TensorFlow, FastAPI, React Native, React JS, and Google Cloud for deployment.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Python Environment Setup](#python-environment-setup)
- [Training the Model](#training-the-model)
- [Model Conversion](#model-conversion)
- [Running the API](#running-the-api)
- [Running the Frontend](#running-the-frontend)
- [Mobile App Setup](#mobile-app-setup)
- [Cloud Deployment](#cloud-deployment)

## Prerequisites

- Python 3.11 ([Installation Guide](https://wiki.python.org/moin/BeginnersGuide))
- Node.js ([Installation Guide](https://nodejs.org/en/download/package-manager/))
- NPM ([Installation Guide](https://www.npmjs.com/get-npm))
- Docker Desktop
- TensorFlow Serving ([Setup Instructions](https://www.tensorflow.org/tfx/serving/setup))
- Google Cloud SDK (for deployment) ([Setup Instructions](https://cloud.google.com/sdk/docs/quickstarts))

## Python Environment Setup

1. Create and activate a conda environment:

```bash
conda create --name potato_disease python=3.8
conda activate potato_disease
```

2. Install required Python packages:

```bash
pip install -r training/requirements.txt
pip install -r api/requirements.txt
```

## Training the Model

1. Download the PlantVillage dataset from [Kaggle](https://www.kaggle.com/arjuntejaswi/plant-village)
2. Extract and keep only potato-related folders
3. Launch Jupyter Notebook:

```bash
jupyter notebook
```

4. Open `training/potato-disease-training.ipynb`
5. Update the dataset path in cell #2
6. Execute all cells sequentially
7. Save the generated model with version number in the `models` folder

## Model Conversion

### Converting H5 to SavedModel Format

Use the following script to convert your trained H5 model to TensorFlow SavedModel format:

```python
import tensorflow as tf

# Load your H5 model
model = tf.keras.models.load_model(
    r"path/to/your/model/best.h5",
    compile=False
)

# Export to SavedModel format (for TensorFlow Serving)
model.export(r"path/to/save/potato_model/1")
```

### Creating TensorFlow Lite Model

1. Launch Jupyter Notebook:

```bash
jupyter notebook
```

2. Open `training/tf-lite-converter.ipynb`
3. Update the dataset path in cell #2
4. Execute all cells sequentially
5. The TF Lite model will be saved in the `tf-lite-models` folder

## Running the API

### Option 1: Using FastAPI Only

1. Navigate to the API directory:

```bash
cd api
```

2. Start the FastAPI server:

```bash
uvicorn main:app --reload --host 0.0.0.0
```

3. The API will be available at `http://0.0.0.0:8000`

### Option 2: Using FastAPI with TensorFlow Serving

1. Navigate to the API directory:

```bash
cd api
```

2. Configure the models:

```bash
cp models.config.example models.config
```

Update the paths in `models.config` to point to your model locations.

3. Pull the TensorFlow Serving Docker image (first time only):

```bash
docker pull tensorflow/serving
```

4. Start TensorFlow Serving container:

**Windows PowerShell:**
```powershell
docker run --rm -p 8501:8501 `
  -v /path/to/your/project/model:/model `
  tensorflow/serving `
  --model_config_file=/model/models.config
```

**Linux/Mac:**
```bash
docker run --rm -p 8501:8501 \
  -v /path/to/your/project/model:/model \
  tensorflow/serving \
  --model_config_file=/model/models.config
```

5. Start the FastAPI server:

```bash
uvicorn main-tf-serving:app --reload --host 0.0.0.0
```

Or run directly from your IDE using `main-tf-serving.py`

6. The API will be available at `http://0.0.0.0:8000`
7. TensorFlow Serving will be available at `http://localhost:8501`

### Testing the API

Use Postman or any HTTP client to send requests to the API endpoint with the configured port number.

## Running the Frontend

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install --from-lock-json
npm audit fix
```

3. Configure environment variables:

```bash
cp .env.example .env
```

Update `REACT_APP_API_URL` in `.env` with your API URL if needed.

4. Start the development server:

```bash
npm run start
```

The application will be available at `http://localhost:3000`

## Mobile App Setup

### Initial Setup

1. Follow the [React Native environment setup guide](https://reactnative.dev/docs/environment-setup)
2. Select the `React Native CLI Quickstart` tab and follow platform-specific instructions

### Installation

1. Navigate to the mobile app directory:

```bash
cd mobile-app
```

2. Install dependencies:

```bash
yarn install
```

3. For macOS users only (iOS development):

```bash
cd ios && pod install && cd ../
```

4. Configure environment variables:

```bash
cp .env.example .env
```

Update the `URL` in `.env` with your API URL if needed.

### Running the App

**Android:**
```bash
npm run android
```

**iOS:**
```bash
npm run ios
```

### Building for Production

To create a signed APK for Android, follow the [official React Native guide](https://reactnative.dev/docs/signed-apk-android).

## Cloud Deployment

### Prerequisites

1. Create a [GCP account](https://console.cloud.google.com/freetrial/signup/tos)
2. Create a new [GCP Project](https://cloud.google.com/appengine/docs/standard/nodejs/building-app/creating-project) and note the project ID
3. Create a [GCP Storage bucket](https://console.cloud.google.com/storage/browser/)
4. Authenticate with Google Cloud SDK:

```bash
gcloud auth login
```

### Deploying TensorFlow Lite Model

1. Upload `potatoes.h5` model to your GCP bucket at path: `models/potatos.h5`

2. Navigate to the GCP directory and deploy:

```bash
cd gcp
gcloud functions deploy predict_lite \
  --runtime python38 \
  --trigger-http \
  --memory 512 \
  --project PROJECT_ID
```

Replace `PROJECT_ID` with your actual GCP project ID.

3. Test the deployment using Postman with the trigger URL provided in the [GCP Console](https://cloud.google.com/functions/docs/calling/http)

### Deploying Full TensorFlow Model (.h5)

1. Upload the `.h5` model to your GCP bucket at path: `models/potato-model.h5`

2. Navigate to the GCP directory and deploy:

```bash
cd gcp
gcloud functions deploy predict \
  --runtime python38 \
  --trigger-http \
  --memory 512 \
  --project PROJECT_ID
```

Replace `PROJECT_ID` with your actual GCP project ID.

3. Test the deployment using Postman with the trigger URL provided in the GCP Console

## Additional Resources

- [TensorFlow Serving with Cloud Functions](https://cloud.google.com/blog/products/ai-machine-learning/how-to-serve-deep-learning-models-using-tensorflow-2-0-with-cloud-functions)
- [PlantVillage Dataset](https://www.kaggle.com/arjuntejaswi/plant-village)
