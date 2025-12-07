from module_03_ci_culture_beginning.materials.testing_age.social_age import get_social_status

def check_if_can_get_child_status():
   age = 8
   expected_res = 'ребенок'
   function_res = get_social_status(age)
   if expected_res == function_res:
       print('It works')
   else:
       print("It doesn't works")


if __name__ == '__main__':
    check_if_can_get_child_status()
