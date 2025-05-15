conformers <- c("CN_N1", "CN_N2", "CN_P1", "CN_P2")
difference <- c(186, 346, 0, 57)

# Use numeric positions for plotting
x_pos <- 1:length(conformers)

# Create the plot
plot(x_pos, difference, type = 'o', xaxt = 'n', 
     main = "Hartree Energy Variation Across Conformers",
     xlab = "Conformers", ylab = "Difference in Wavenumber (cm-1)",
     ylim = c(0, 400))

# Add x-axis labels
axis(1, at = x_pos, labels = conformers)

# Label points
text(x = x_pos, y = difference, labels = difference,
     pos = 3, cex = 0.8, col = "red")