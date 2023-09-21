from flask import request

hight = 70

flag_can_cm = 0
flag_pet_cm = 0
flag_gen_cm = 0


def fulllate_calculate(result_Data):
    global flag_gen_cm
    number = result_Data.get("number")
    # can_cm = result_Data.get("can")
    # pet_cm = result_Data.get("pet")
    input_gen_cm = result_Data.get("gen")
    
    # if(flag_pet_cm + 5 < pet_cm ):
    #     result_pet_cm = int(pet_cm / hight * 100)   
    if((flag_gen_cm + 5) < input_gen_cm ):
        flag_gen_cm = input_gen_cm
        gen_cm = int(input_gen_cm / hight * 100)
    else:
        gen_cm = int(flag_gen_cm / hight * 100)
    
    # if(flag_can_cm + 5 < can_cm ):
    #     result_can_cm = int(can_cm / hight * 100)
    
    #오차범위 5cm
    
    
    
    return { 
            "number " : number,
            # "Result_Can_Fulllate " : result_can_cm,
            # "Result_Pet_Fulllate " : result_pet_cm,
            "Result_Gen_Fulllate " : gen_cm 
            }