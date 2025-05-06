# Assuming
L <- 1

# X-axis and Y-axis values
x_values <- seq(0, L, length.out = 1000)
u_values <- (0.924) * (sin(pi * x_values / L) + sin(2 * pi * x_values / L))

# Final plot
plot(x_values, u_values, type = "l", lwd = 2, xlim = c(0, L), ylim = c(-2, 2), 
     xlab = "x", ylab = "u", main = "Travelling Wave no phase difference")

# Label
legend("bottomleft", legend = "t = 15/16𝜈")