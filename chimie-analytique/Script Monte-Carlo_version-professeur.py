import scipy.optimize as optimize
import numpy as np
import matplotlib.pyplot as plt

#Objectif du script : Tracé la distribution sous forme d'histogramme des incertitudes par méthode de Monte-Carlo

#Modif 1 : Si plus ou moins de paramètres à prendre en compte rajouter un i_sample, un i et un sigma i.dans chaque fonction/partie

#Modif 2 : Si la relation n'est pas un produit, changer la formule dans le def/return de la grandeur d'intérêt 

def monte_carlo(f, x, y, z, sigma_x, sigma_y, sigma_z, N=1000000):
    
    """
#Fonction permettant d'estimer l'incertitude sur f(x, y)
    :f: Fonction à évaluer, de la forme f(x, y)
    :y: Valeur centrale de y
    :sigma_y: Incertitude sur y (écart-type)
    :N: Nombre de simulations Monte Carlo
    """
    
#Simuler un tirage random de chaque grandeur d'intérêt, puis d'une valeur de notre grandeur correspondante : 

    x_samples = np.random.normal(x, sigma_x, N)
    y_samples = np.random.normal(y, sigma_y, N)
    z_samples = np.random.normal(z, sigma_z, N)
    
    #Le normal implique une distribution gaussiene des valeurs (uniform pour rectangulaire et triangular pour triangulaire)
    
    f_samples = f(x_samples, y_samples, z_samples)
    
    # Renvoyer la valeur moyenne des tirages effectués avec l'écart type associé : 
    
    return np.mean(f_samples), np.std(f_samples), f_samples

#Fonction permettant de sommer (sum) le nombre de valeur dans l'intervalle donné puis fais un pourcentage.
#On soustrait un intervalle de confiance pour obtenir le nombre de valeur dans l'intervalle de confiance 

def func_start(x,data,moy,conf):
    """
    x abscisses
    """
    return ((moy-x < data) & (data < moy+x)).sum()/data.size*100-conf

# Formule permettant de calculer la grandeur d'intérêt (cas d'une dilution):
    
def Cf(c, v, vi):
    return c * v / vi

#Listes des différentes grandeurs avec l'incertitude associée (cas d'une dilution):

x = 0.1
y = 0.001
z = 0.1
sigma_x = 0.01
sigma_y = 0.00001
sigma_z = 0.01

mean_f, std_f, f_samples = monte_carlo(Cf, x, y, z, sigma_x, sigma_y, sigma_z)

#Attention std correspond à l'écart type et non à une valeur d'incertitude liée à un intervalle de confiance comme dans MC

"""

Pour avoir seulement les valeurs dans un intervalle de confiance fixé, on utilise la fonction brentq qui va déterminer 
quand une fonction est égale à 0 
On peut changer l'intervalle de confiance en changeant la dernière valeur 

"""
# (fonction, borne inférieure, borne supérieure, arguments)
res = optimize.brentq(func_start,0, np.max( [mean_f-np.min(f_samples),np.max(f_samples)-mean_f]),args=(f_samples,mean_f,95))

print(f"La concentration est de {mean_f:.5f} avec une incertitude de {res:.5f} mol/L")

# Tracé de l'histogramme des valeurs simulées

plt.hist(f_samples, bins=500, density=True, alpha=0.6, color='b')
plt.axvline(mean_f, color='r', linestyle='dashed', linewidth=2, label=f"Concentration moyenne : {mean_f:.4f} mol/L")
plt.xlabel("Valeur de Cf(C, V, vi)")
plt.ylabel("Densité de probabilité")
plt.title("Histogramme des valeurs simulées de Cf(C, V, vi)")
plt.legend()
plt.show()
plt.grid()
