colors = c("green", "blue", "pink", "yellow")
interactions <- c("16. n (N[10]) -> 86. π* (C[25]-O[27])", 
                  "16. n (N[10]) -> 81. σ* (C[22]-H[23])", 
                  "18. n (O[27]) -> 79. σ* (C[19]-H[21])")
conformers <- c("CN_P1", "CN_P2", "CN_N1", "CN_N2")

# Matrix of interaction energies
interaction_energies <- matrix(c(6.58, 0.11, 0, 6.72, 0.33, 0.1, 0, 0, 0, 0, 0.17, 0.27),
                 nrow = 4, ncol = 3, byrow = TRUE)

# Bar plot
barplot(interaction_energies, main = "Significant Interactions (|ΔE| > 0.1 kcal/mol)", names.arg = interactions,
        xlab = "Interactions", ylab = "Interaction Energies (kcal/mol)",
        col = colors, beside = TRUE)

# Legend for conformers
legend("topright", legend = conformers, fill = colors)