library(tidyverse)
signor <- read_csv("Downloads/signor.csv")

length(table(signor$pathway_id))

signor2 <- signor %>% filter(typea == "protein" | typeb == "protein")

length(table(signor2$pathway_id))

signor3 <- signor2 %>% filter(tax_id == "9606")

length(table(signor3$pathway_id))

sum(is.na(signor3$entityb))

list_a <- signor3 %>% filter(typea == "protein") %>% select(pathway_id, entitya) %>% rename(symbol = entitya)
list_b <- signor3 %>% filter(typeb == "protein") %>% select(pathway_id, entityb) %>% rename(symbol = entityb)

list_comb <- rbind(list_a, list_b)

list_uniq <- unique(list_comb)

length(table(list_uniq$pathway_id))
