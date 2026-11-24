from src.models.orders import Size
def get_coef(x):
   if x == Size.small:
      return 1
   if x == Size.medium:
      return 1.5
   if x == Size.large:
      return 1.75
   return 2
