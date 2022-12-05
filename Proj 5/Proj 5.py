###########################################################
#  Computer Project #5
#  
#  Program that uses a mix of files, functions, and calulations \n
#  to gather information on planets, stars, habitable planets, \n
#  distance of the planets/stars
#
#  The first part of the progam is where the functions are made
#
#  The first funtion opens a file, the second is a float function, \n
#  the third retrieves the density, the fourth is for the temperature, \n
#  and the fifth is for the distance
#
#  In the main function, variables are made and most of the code is run \n
#  through a for loop.
#
#  Each if statement in ther for loop runs through a given file to \n
#  obtain the necessary information needed for the calculation
#
# The print statements at the end display the data 
#  
###########################################################



import math

#Constants
PI = math.pi   
EARTH_MASS =  5.972E+24    # kg
EARTH_RADIUS = 6.371E+6    # meters
SOLAR_RADIUS = 6.975E+8    # radius of star in meters
AU = 1.496E+11             # distance earth to sun in meters
PARSEC_LY = 3.262

# Opens a file based ont he name given
def open_file():
    file_data = input("Input data to open: ") + ".csv"

    x = 0
    while x == 0:
        try:
            file_pointer = open(file_data)
            break
        except:
            print("\nError: file not found.  Please try again.")
            file_data = input("Enter a file name: ") + ".csv"

    return file_pointer

# Makes a float if possible. If it can't it will return -1
def make_float(s):
    try:
        s = float(s)
        return s

    except:
        return -1
  
# Calculates the density through mass and volume  
def get_density(mass, radius):


    if mass < 0 or radius < 0: 
        return -1 

    volume =  (4 * PI * (radius * EARTH_RADIUS)**3)/3
    density = (mass * EARTH_MASS)/volume

    return density

# Planet temperature is calcuated here
def temp_in_range(axis, star_temp, star_radius, albedo, low_bound, upp_bound):
    if axis == -1 or star_temp == -1 or star_radius == -1:
        return False

    planet_temp = star_temp * ((star_radius * SOLAR_RADIUS)/(2* (axis * AU)))**0.5 *(1 - albedo)**0.25

    if planet_temp > low_bound and planet_temp < upp_bound:
        return True

    else:
        return False

            


# Retrieves the distance from earth and makes it into a float. 
# If it can't an error message will occur an a reprompt
def get_dist_range():
    while(True):
        distance = input("\nEnter maximum distance from Earth (light years): ")
        try:
            distance = float(distance)
            if distance < 0:
                print("\nError: Distance needs to be greater than 0.")
                continue
            else:
                break
        
        except ValueError:
            print("\nError: Distance needs to be a float.")

    return distance

# Main function of the program
def main():
         
    print('''Welcome to program that finds nearby exoplanets '''\
          '''in circumstellar habitable zone.''')

    file_pointer = open_file()
    max_distance = get_dist_range()/PARSEC_LY
    
# variables needed for calculations
    low_bound = 200
    upp_bound = 350
    albedo = 0.5
    max_num_planets = -560
    max_num_stars = -866
    mass_planets = 0
    mass_count = 0
    habitable = 0
    p_radius = 0
    rocky = 0
    gas = 0
    min_rocky_dist = 5345
    min_gas_dist = 2345
    min_rocky_name = ""
    min_gas_name = ""



# For loop to iterate through each file
# each if statement has a different calculation
    for each_line in file_pointer:
        if make_float(each_line[114:]) != -1:
            if float(each_line[114:]):
                distance = make_float(each_line[114:])

        # Star radius
        if make_float(each_line[106:113]) != -1:
            if float(each_line[106:113]):
                s_radius = make_float(each_line[106:113])
        
        else:
            s_radius = -1

        # Each if statement reads through the file for the variable
        if make_float(each_line[66:77]) != -1:
            if float(each_line[66:77]):
                ax = make_float(each_line[66:77])
        
        else:
            ax = -1

        # Reads through star temperature 
        if make_float(each_line[97:105]) != -1:
            if float(each_line[97:105]):
                s_temp = make_float(each_line[97:105])
        else:
            s_temp = -1
    
        # Number of stars 
        if make_float(each_line[50:57]) != -1:
            if make_float(each_line[114:]) != -1:
                if float(each_line[114:]) <= max_distance:
                    if (float(each_line[50:57]) > max_num_stars):
                        max_num_stars = int(each_line[50:57])

        # Number of planets
        if make_float(each_line[58:65]) != -1:
            if make_float(each_line[114:]) != -1:
                if float(each_line[114:]) <= max_distance:
                    if float(each_line[58:65]) > max_num_planets:
                        max_num_planets = int(each_line[58:65])

        # Mass count
        if make_float(each_line[86:96]) != -1:
            if make_float(each_line[114:]) != -1:
                if float(each_line[114:]) <= max_distance:
                    mass_planets += float(each_line[86:96])
                    temp_mass = float(each_line[86:96])
                    mass_count += 1
        else:
            temp_mass = -1

        # Planet radius
        if make_float(each_line[78:85]) != -1:
            if float(each_line[78:85]):
                p_radius = make_float(each_line[78:85])
        
        else:
            p_radius = -1

        # Finds habitable planets for living
        if temp_in_range(ax, s_temp, s_radius, albedo, low_bound, upp_bound):
            if make_float(each_line[114:]) != -1:
                if float(each_line[114:]) <= max_distance:
                    habitable += 1

                    # Determines if a planet is rocky. If not rocky, it is a gas
                    if(temp_mass > 0 and temp_mass <= 10) or p_radius > 0 and p_radius <= 1.5 or get_density(temp_mass,p_radius) > 2000:
                        # Counts amount of rocky planets
                        rocky += 1
                        if (float(each_line[114:].strip()) < min_rocky_dist):
                            min_rocky_dist = float(each_line[114:].strip())
                            min_rocky_name = each_line[:25].strip()
                    else:
                        #Counts amount of gas planets
                        gas += 1
                        if (float(each_line[114:].strip()) < min_gas_dist):
                            min_gas_dist = float(each_line[114:].strip())
                            min_gas_name = each_line[:25].strip()
        


        

    # Prints out the data from the main function    
    print(f"\nNumber of stars in systems with the most stars: {max_num_stars:d}.")
    print(f"Number of planets in systems with the most planets: {max_num_planets:d}.")

    print(f"Average mass of the planets: {mass_planets /mass_count:.2f} Earth masses.")

    print(f"Number of planets in circumstellar habitable zone: {habitable:d}.")

    if(rocky == 0):
        print("No rocky planet in circumstellar habitable zone.")
    else:
        print(f"Closest rocky planet in the circumstellar habitable zone {min_rocky_name} is {min_rocky_dist * PARSEC_LY:.2f} light years away.")

    if(gas == 0):
        print("No gaseous planet in circumstellar habitable zone.")
    else:
        print(f"Closest gaseous planet in the circumstellar habitable zone {min_gas_name} is {min_gas_dist * PARSEC_LY:.2f} light years away.")


  


if __name__ == "__main__":
    main()