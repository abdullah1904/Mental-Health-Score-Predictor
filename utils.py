import joblib

def load_model(model_path):
    """
    Load a machine learning model from the specified path.

    Args:
        model_path (str): The path to the model file.

    Returns:
        The loaded machine learning model.
    """
    import os
    
    try:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}")
        
        model = joblib.load(model_path)
        return model
    except Exception as e:
        print(f"Error loading model from {model_path}: {e}")
        raise