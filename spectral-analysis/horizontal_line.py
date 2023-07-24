# importing the module
import matplotlib.pyplot as plt
  
# plotting line within the given range
plt.axhline(y = .5, xmin = 0.25, xmax = 0.9)
  
# line colour is blue
plt.axhline(y = 3, color = 'b', linestyle = ':')
  
# line colour is white
plt.axhline(y = 1, color = 'w', linestyle = '--')
  
# line colour is red
plt.axhline(y = 2, color = 'r', linestyle = 'dashed')    
    
# adding axis labels    
plt.xlabel('x - axis')
plt.ylabel('y - axis')
  
# displaying the plot
plt.show()