rm(list = ls())

# automatically take the path to the project location * RStudio API required
path <- dirname(rstudioapi::getActiveDocumentContext()$path)

setwd(path)
rm(path)

require(xlsx)
df <- read.xlsx2("scraper_output.xlsx", sheetIndex = 1, stringsAsFactors = F)


# remove duplicated records by title
df1 <- df[!duplicated(df$title),]


# write.xlsx(df1, "articles_metadata.xlsx", row.names = F, col.names = T)


df <- read.xlsx("articles_reviewed.xlsx", sheetIndex = 1, stringsAsFactors = F)


# how many applied multiverse-type analysis
sum(as.integer(df$mvs_applied))



