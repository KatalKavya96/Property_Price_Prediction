
PAGE_TITLE = "Property Price Prediction Dashboard"
LAYOUT = "wide"
MODEL_PATH = "model/house_price_lr_pipeline.joblib"
UNIT_LABEL = "USD"

PRESETS = {
    "Custom":  dict(OverallQual=5, GrLivArea=1500, GarageCars=2, TotalBsmtSF=800, YearBuilt=2000, FullBath=2, Fireplaces=1, LotArea=8000),
    "Starter": dict(OverallQual=4, GrLivArea=1100, GarageCars=1, TotalBsmtSF=650, YearBuilt=1978, FullBath=1, Fireplaces=0, LotArea=7000),
    "Family":  dict(OverallQual=6, GrLivArea=1850, GarageCars=2, TotalBsmtSF=950, YearBuilt=2004, FullBath=2, Fireplaces=1, LotArea=9000),
    "Premium": dict(OverallQual=8, GrLivArea=2850, GarageCars=3, TotalBsmtSF=1400, YearBuilt=2016, FullBath=3, Fireplaces=2, LotArea=12000),
}

FEATURE_COLS = [
    "OverallQual", "GrLivArea", "GarageCars", "TotalBsmtSF", 
    "YearBuilt", "FullBath", "Fireplaces", "LotArea"
]
