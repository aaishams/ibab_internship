# Assuming
L <- 1
An <- 1

# X and Y axes values
x <- seq(0, L, length.out = 1000) #length.out divides gives 10 intervals between 0 and L

# Modes
n_values <- 1:4
colors <- c("red", "green", "blue", "orange")

# Blank plot
plot(NULL, xlim = c(0, L), ylim = c(-1,1), xlab = "x", ylab = expression("u"[n]*"(x,t)"), main = "1D Vibrating String Modes Plot at t = 0")

# Final plot
for (i in seq_along(n_values)){
  n <- n_values[i]
  color <- colors[i]
  un <- An * sin(n * pi * x / L)
  lines(x, un, col = color, lwd = 2)
}

# Label
legend("bottomleft", legend = paste("n =", n_values), col = colors, lwd = 2, lty = 1)
