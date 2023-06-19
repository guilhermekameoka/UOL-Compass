import xgboost as xgb
import pandas as pd

# maintains a xgboost model and predict class labels
class XgboostPredictor:
  def __init__(self):
    self.load_model()

  # loads model trained by aws SageMaker
  def load_model(self):
    self.xgboost_model = xgb.Booster()
    self.xgboost_model.load_model('./model/xgboost-model')

  # return a missing or a invalid float arg, categorical args are optional
  def get_invalid_arg(self, args):

    # checks if float args:
    for arg_name in [
        'no_of_adults', 'no_of_children', 'no_of_weekend_nights', 
        'no_of_week_nights', 'required_car_parking_space', 'lead_time', 'arrival_year', 
        'arrival_month', 'arrival_date', 'repeated_guest', 'no_of_previous_cancellations',
        'no_of_previous_bookings_not_canceled', 'no_of_special_requests'
      ]:
      arg_value = args.get(arg_name)
      # exists
      if not arg_value:
        return f'Missing field {arg_name}'
      # can be casted to float
      try:
        float(arg_value)
      except:
        return f'Field {arg_name} must be a float, "{arg_value}" value given'
      
    return None

  # returns a class label based on args
  def predict(self, args):

    # checks if args are valid, return error if not
    error_message = self.get_invalid_arg(args)
    if error_message != None:
      return None, error_message

    # parse args
    parsed_args = self.parse_args(args)

    # does prevision and converts to the label class in range[1,3]
    prevision = self.xgboost_model.predict(parsed_args)
    prevision_class = 1 if prevision <= 1.0/3.0 else (2 if (prevision <= 2.0/3.0) else 3)

    return prevision_class, None

  # parse args to xgboost format
  def parse_args(self, args):

    # creates transpose dataframe args
    df_args = pd.DataFrame([
      float(args["no_of_adults"]),
      float(args["no_of_children"]),
      float(args["no_of_weekend_nights"]),
      float(args["no_of_week_nights"]),
      float(args["required_car_parking_space"]),
      float(args["lead_time"]),
      float(args["arrival_year"]),
      float(args["arrival_month"]),
      float(args["arrival_date"]),
      float(args["repeated_guest"]),
      float(args["no_of_previous_cancellations"]),
      float(args["no_of_previous_bookings_not_canceled"]),
      float(args["no_of_special_requests"]),
      1.0 if args.get("type_of_meal_plan") == "Meal Plan 1" else 0.0,
      1.0 if args.get("type_of_meal_plan") == "Meal Plan 2" else 0.0,
      1.0 if args.get("type_of_meal_plan") == "Meal Plan 3" else 0.0,
      1.0 if args.get("type_of_meal_plan") == "Not Selected" else 0.0,
      1.0 if args.get("room_type_reserved") == "Room_Type 2" else 0.0,
      1.0 if args.get("room_type_reserved") == "Room_Type 3" else 0.0,
      1.0 if args.get("room_type_reserved") == "Room_Type 4" else 0.0,
      1.0 if args.get("room_type_reserved") == "Room_Type 5" else 0.0,
      1.0 if args.get("room_type_reserved") == "Room_Type 6" else 0.0,
      1.0 if args.get("room_type_reserved") == "Room_Type 7" else 0.0,
      1.0 if args.get("market_segment_type") == "Aviation" else 0.0,
      1.0 if args.get("market_segment_type") == "Complementary" else 0.0,
      1.0 if args.get("market_segment_type") == "Corporate" else 0.0,
      1.0 if args.get("market_segment_type") == "Online" else 0.0
    ]).T

    # converts it to xgb.DMatrix and returns, required as input to do prevision
    return xgb.DMatrix(df_args.values)