n <- 100
L <- 1
x_values <- seq(0, L, length.out = 1000)
psi_values <- c(sqrt(2 / L) * sin(n * pi * x_values / L))
psi_square_values <- c((2 / L) * (sin(n * pi * x_values / L)) ^ 2)

plot(x_values, psi_values, type = "l", ylim = c(0, 2), 
     xlab = "x", ylab = "Function", main = "Plot for n = 100")
lines(x_values, psi_square_values, col = "blue")

legend(NULL, legend = legend("topright", 
                             legend = c(expression(psi(x)), 
                                        expression("|" * psi(x) * "|"^2)), 
                             col = c("black", "blue"), lty = 1))
