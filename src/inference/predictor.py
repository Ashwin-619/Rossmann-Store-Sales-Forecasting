from pathlib import Path
from typing import Any, Dict, Union
import pickle
import pandas as pd
import numpy as np


class TwoStageModelPipeline:

  def __init__(
      self,
      customer_model_path: Union[str, Path],
      sales_model_path: Union[str, Path],
      customer_col_name: str = "Customers",
  ):
    """Loads native xgb.Booster instances and handles sequential inference."""
    self.xgb_customer_model = self._load_booster(customer_model_path)
    self.xgb_sales_model = self._load_booster(sales_model_path)
    self.customer_col_name = customer_col_name

  def _load_booster(self, path: Union[str, Path]):
    """Safely loads native Booster whether saved via joblib or booster.save_model()."""
    path_str = str(path)
    model = pickle.load(open(path_str, "rb"))
    return model 
    
  def _align_features_and_dtypes(self, df: pd.DataFrame, model: Any) -> pd.DataFrame:
      df_aligned = df.copy()

      # Extract model booster and feature list
      expected_features = model.feature_names_in_

      # 2. REORDER columns strictly to match the model's exact training sequence
      with open(r"models\categorical_schemas.pkl", "rb") as file:
          categorical_schemas = pickle.load(file)

      for col, dtype in categorical_schemas.items():
          df_aligned[col] = df_aligned[col].astype(dtype)

      df_aligned = df_aligned[list(expected_features)]

      return pd.DataFrame(df_aligned)

  def predict(self, feature_df: pd.DataFrame) -> Dict[str, Any]:

      try:
        # Stage 1: Align columns & predict Customers
        df_stage1 = self._align_features_and_dtypes(feature_df, self.xgb_customer_model)
        #df_stage1 = xgb.DMatrix(df_stage1, enable_categorical=True)
        customer_pred = np.expm1(float(self.xgb_customer_model.predict(df_stage1)[0]))

        # Stage 2: Append predicted Customers & align columns for Sales model
        df_stage2_input = feature_df.copy()
        df_stage2_input[self.customer_col_name] = customer_pred

        df_stage2 = self._align_features_and_dtypes(df_stage2_input, self.xgb_sales_model)
        #dstage2 = xgb.DMatrix(df_stage2, enable_categorical=True)
        sales_pred = np.expm1(float(self.xgb_sales_model.predict(df_stage2)[0]))
        

        return {
            "predicted_customers": int(np.round(customer_pred, 0)),
            "predicted_sales": int(np.round(sales_pred, 0))
        }

        

      except Exception as e:
        raise RuntimeError(f"Error during prediction: {e}")