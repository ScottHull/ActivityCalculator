#Activity Calculator
#Written by Scott D. Hull, The Ohio State University 2016
#IN DEVELOPMENT



import os, pandas, csv
from math import *
from decimal import Decimal


#can implement T-dependent constants later, assume 25degC for now
A = 0.5085
B = 0.3281


#need .csv formatted perioid table for future development in arbitrary calculations, class 'molmass' is a hack for current needs
class molmass:

    def getmolmass(self, element):
        if element == 'Na' or element == 'na':
            molmass = 22.9898
            return molmass
        elif element == 'K' or element == 'k':
            molmass = 39.0983
            return molmass
        elif element == 'Ca' or element == 'ca':
            molmass = 40.078
            return molmass
        elif element == 'Mg' or element == 'mg':
            molmass = 24.305
            return molmass
        elif element == 'Si' or element == 'si':
            molmass = 28.0855
            return molmass
        elif element == 'Cl' or element == 'cl':
            molmass = 35.453
            return molmass
        elif element == 'SO4' or element == 'so4':
            molmass = 96.0626
            return molmass
        elif element == 'HCO3' or element == 'hco3':
            molmass = 61.0168
            return molmass

class effectivediameter:
    
    def geteffdia(self, element):
        if element == 'Na' or element == 'na':
            effdia = 4.5
            return effdia
        elif element == 'K' or element == 'k':
            effdia = 3.0
            return effdia
        elif element == 'Ca' or element == 'ca':
            effdia = 6.0
            return effdia
        elif element == 'Mg' or element == 'mg':
            effdia = 8.0
            return effdia
        elif element == 'Si' or element == 'si':
            effdia = 2.22
            return effdia
        elif element == 'Cl' or element == 'cl':
            effdia = 3.0
            return effdia
        elif element == 'SO4' or element == 'so4':
            effdia = 4.5
            return effdia
        elif element == 'HCO3' or element == 'hco3':
            effdia = 4.5
            return effdia


class equations:

    def ionicstrength(self, moles, charge):
        ionicstrength = (1/2)*(moles*charge**2)
        return ionicstrength

    def debye_huckel(self, charge, ionicstrength):
        activitycoeff = 10**-(0.5085*(charge**2)*(ionicstrength**(1/2)))
        return activitycoeff

    def extended_debye_huckel(self, Aconstant, Bconstant, charge, ionicstrength, effectivediameter):
        activitycoeff = 10**-((Aconstant*(charge**2)*ionicstrength**(1/2))/(1+(effectivediameter*Bconstant*ionicstrength**(1/2))))
        return activitycoeff

    def davis(self, Aconstant, ionicstrength):
        activitycoeff = 10**-(((ionicstrength**(1/2))/((1+(ionicstrength**(1/2)))))-(0.2*ionicstrength))
        return activitycoeff

    def pitzer(self):
        #not yet implemented
        # return activitycoeff
        pass


def __init__():
    print("\n\n_____________________________________\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("Welcome to the activity coefficient calculator!")
    print("Written by Scott D. Hull, The Ohio State University 2016\n")
    print("Please enter a .csv in the working directory with elements in the first column, "
          "charge in the second, and concentration in the third (mole/L).")

    input1 = input(">>> ")

    print("\n")

    with open(input1, "r") as infile:

        reader = csv.reader(infile, delimiter=",")
        element_list = []
        chg_list = []
        mol_list = []
        ionicstrength_sum_list = []
        for row in reader:

            print("*********************************************************")

            element = row[0]
            chg = float(row[1])
            conc = float(row[2])

            molarmass = molmass.getmolmass(molmass, element=element)
            moles = conc/molarmass

            element_list.append(element)
            chg_list.append(chg)
            mol_list.append(chg)

            #first, calculate the ionic strength of individual components
            ionicstrength = equations.ionicstrength(equations, moles=moles, charge=chg)
            ionicstrength_sum_list.append(ionicstrength)
            ionicstrength = equations.ionicstrength(equations, moles=moles, charge=chg)

            print("The ionic strength of " + element + " is: " + '%.4E' % Decimal(ionicstrength))

            # I < 5*10^-3 = debye-huckel
            # 5*10^-3 =< I =< 0.1 = extended debye-huckel
            # 0.1 =< I =< 0.5 = davis
            # I >= 0.5 = pitzer

            if ionicstrength < 0.005:
                #debye-huckel
                print("The element " + element + " requires the Debye-Huckel formula!")
                activity = equations.debye_huckel(equations, charge=chg, ionicstrength=ionicstrength)
                print("The activity of " + element + " is: " + str(round(activity, 6)))

            elif ionicstrength <= 0.1 and ionicstrength >= 0.005:
                #extended debye-huckel
                print("The element " + element + " requires the Extended Debye-Huckel formula!")
                effdia = effectivediameter.geteffdia(effectivediameter, element=element)
                activity = equations.extended_debye_huckel(equations, Aconstant=A, Bconstant=B, charge=chg, ionicstrength=ionicstrength, effectivediameter=effdia)
                print("The activity of " + element + " is: " + str(round(activity, 6)))

            elif ionicstrength > 0.005 and ionicstrength <= 0.5:
                #davis
                print("The element " + element + " requires the Davis formula!")
                activity = equations.davis(equations,Aconstant=A, ionicstrength=ionicstrength)
                print("The activity of " + element + " is: " + str(round(activity, 6)))
            elif ionicstrength > 0.5:
                print("The element " + element + " requires the Pitzer formula!")
                print("Not yet implemented!")
                pass
            else:
                print("\nCould not calculate activity.\n")

        ionicstrength_sum = sum(ionicstrength_sum_list)
        print("\nThe total ionic strength of the reservoir is: " + '%.4E' % Decimal(ionicstrength_sum))

    print("\n\nThank you for using the activity calculator!  Goodbye!\n\n\n\n")
    print("_______________________________\n")



__init__()