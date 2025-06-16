library(mice)
library(dplyr)

output_dir <- "imputed/"

# SF-36 questionnaire columns with 31.2% missing data
file_list_31 <- list.files(
  path       = "targets/",
  pattern    = "31.csv$",
  full.names = TRUE
)

for (file in file_list_31) {
  df <- read.csv(file)
  print(file)
  df$X <- NULL

  # begin imputation for 31 datasets each with 10 iterations
  imp <- mice(df, m = 31, maxit = 10, method = "pmm", seed = 1)

  # combine all imputed datasets into a single one
  long <- complete(imp, action = "long", include = FALSE)

  out_file <- file.path(
    output_dir,
    paste0(tools::file_path_sans_ext(basename(file)), "_imputed.csv")
  )
  write.csv(long, out_file, row.names = FALSE)
}

# SF-36 questionnaire columns with 12.5% missing data
file_list_13 <- list.files(
  path       = "targets/",
  pattern    = "13.csv$",
  full.names = TRUE
)

for (file in file_list_13) {
  df <- read.csv(file)
  print(file)
  df$X <- NULL

  # begin imputation for 13 datasets each with 10 iterations
  imp <- mice(df, m = 13, maxit = 10, method = "pmm", seed = 1)

  # combine all imputed datasets into a single one
  long <- complete(imp, action = "long", include = FALSE)

  out_file <- file.path(
    output_dir,
    paste0(tools::file_path_sans_ext(basename(file)), "_imputed.csv")
  )
  write.csv(long, out_file, row.names = FALSE)
}