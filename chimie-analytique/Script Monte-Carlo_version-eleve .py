"""

Ce script permet de calculer la quantité de matière et son incertitude associée en utilisant la méthode de Monte-Carlo. 

1) Rappeler le principe de fonctionnement de la méthode de Monte-Carlo et en quoi la fonction monte_carlo utilisée dans ce script permet de simuler cette technique

2) A quoi servent les np.mean et np.std ? 

3) Tester le code en changeant le nombre de tirage. Le nombre de tirage semble-t-il important ? Combien de tirages minimum vous semblent satisfaisant ? 

4) ligne 67 : le dernier chiffre correspond à l'intervalle de confiance ( 75 pour 75%). Modifier le code pour appliquer un 
intervalle de confiance de 95%. Comment évolue l'incertitude calculée ? Comment évolue l'histogramme de densité de probabilité ? 
Conclure

5) Proposer des modifications pour appliquer la méthode de Monte-Carlo au calcul d'une concentration fille lors d'une dilution 

#aide potentielle : Dans le cas d'une dilution la formule est de la forme Cf = Ci * Vi / Vf. On a donc désormais 3 paramètres à prendre en compte. Pour pouvoir 
obtenir la grandeur d'intérêt et son incertitude associée, il faut donc changer la formule et ajouter une variable et son incertitude dans la fonction monte_carlo'

"""

import scipy.optimize as optimize
import numpy as np
import matplotlib.pyplot as plt

def monte_carlo(f, x, y, sigma_x, sigma_y, N=1000000):

    """
#Fonction permettant d'estimer l'incertitude sur f(x, y)
    :f: Fonction à évaluer, de la forme f(x, y)
    :y: Valeur centrale de y
    :sigma_y: Écart-type
    :N: Nombre de simulations Monte Carlo
    """
    

    x_samples = np.random.normal(x, sigma_x, N)
    y_samples = np.random.normal(y, sigma_y, N)

    f_samples = f(x_samples, y_samples)

    return np.mean(f_samples), np.std(f_samples), f_samples

def func_start(x,data,moy,conf):
    """
    x abscisses
    """
    return ((moy-x < data) & (data < moy+x)).sum()/data.size*100-conf

"""


Application de la méthode de Monte-Carlo a une quantité de matière: 


"""

def n(c, v):
    return c * v

x = 0.1
y = 0.001
sigma_x = 0.01
sigma_y = 0.0005

mean_f, std_f, f_samples = monte_carlo(n, x, y, sigma_x, sigma_y)
res = optimize.brentq(func_start,0, np.max( [mean_f-np.min(f_samples),np.max(f_samples)-mean_f]),args=(f_samples,mean_f,75))
print(f"La concentration est de {mean_f:.5f} avec une incertitude de {res:.5f} mol/L")


plt.hist(f_samples, bins=500, density=True, alpha=0.6, color='b')
plt.axvline(mean_f, color='r', linestyle='dashed', linewidth=2, label=f"Quantité de matière moyenne: {mean_f:.5f} mol")
plt.xlabel("Valeur de n(c, v)")
plt.ylabel("Densité de probabilité")
plt.title("Histogramme des valeurs simulées de n(c, v)")
plt.legend()
plt.show()
plt.grid()