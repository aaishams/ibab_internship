x_values <- seq(-2 * pi, 5 * pi, length.out = 1000)
real_part <- exp(x_values) * cos(x_values)
imaginary_part <- exp(x_values) * sin(x_values)

plot(x_values, real_part, type = "l", col = "blue", ylim = c(-1000, 1000),
     xlab = "x", ylab = "Value", main = "Real and Imaginary parts of the function")
lines(x_values, imaginary_part, col = "red")
legend("topleft", legend = c("Real Part", "Imaginary Part"), col = c("blue", "red"), lty = 1)