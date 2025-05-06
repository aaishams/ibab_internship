# Assuming
L <- 1
Amn <- 1

# X and Y axes values
x <- seq(0, L, length.out = 50) #length.out divides gives 1000 intervals between 0 and L
y <- seq(0, L, length.out = 50)

# Create grid
X <- outer(x, rep(1, length(y)))
Y <- outer(rep(1, length(x)), y)

# Modes
m <- 2
n <- 2

# Final plot
umn <- Amn * sin(m * pi * X / L) * sin(n * pi * Y / L)
persp(x, y, umn, xlab = "x", ylab = "y", zlab = expression(u_mn(x, y, t)), main = "2D Vibrating Mesh Plot at t = 0", col = "red", theta = 30, phi = 30)

# Label
legend("bottomleft", legend = paste("m = ", m, "\nn = ", n))