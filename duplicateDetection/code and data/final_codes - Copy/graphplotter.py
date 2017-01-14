from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
def plotgraph(x,y,zs):    
    # x = []
    # y = []
    # index = 0
    # for shingleSize in range(2, 7):
        # for threshold in range(0,10):
            # x.insert(index, shingleSize)
            # y.insert(index, threshold)
            # index+=1
            
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xs = x
    ys = y
    # zs = [top(x, y) for x,y in zip(xs,ys)]

    ax.scatter(xs, ys, zs)

    ax.set_xlabel('Shingle size')
    ax.set_ylabel('Threshold')
    ax.set_zlabel('No of duplicates')

    plt.show()
    
def main():
    x=[1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4]
    y=[40, 42, 44, 46, 48, 50, 40, 42, 44, 46, 48, 50, 40, 42, 44, 46, 48, 50, 40, 42, 44, 46, 48, 50]
    z=[0.543352601156,0.61038961039,0.730158730159,0.771929824561,0.834951456311,0.868686868687,0.561403508772, 0.630872483221, 0.752, 0.831683168317, 0.857142857143, 0.857142857143, 0.571428571429, 0.693548387097, 0.824742268041, 0.886363636364, 0.857142857143, 0.857142857143, 0.558139534884, 0.625, 0.740740740741, 0.781609195402, 0.781609195402, 0.809523809524]
    #z=[125,106,78,66,55,51,123,101,77,53,43,43,120,76,49,40,36,36,124,96,60,39,39,36]
    plotgraph(x,y,z)
if __name__=="__main__": main()
