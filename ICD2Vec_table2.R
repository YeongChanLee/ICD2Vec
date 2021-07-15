#table 2
library(dplyr)
library(data.table)
library(proxy)

all_icd <- as.data.frame(fread("../ICD2Vec_raw_data/ICD_Code_Vectors.csv", header = TRUE))
colnames(all_icd)[3:302] <- paste0("V", 1:300)
all_icd <- all_icd[,-1]
all_icd <- rename(all_icd, DIS_NAME = DIS_CODE)
all_icd <- filter(all_icd, !(DIS_NAME %in% c("N068", "N078", "N018", "N048"))) # these diseases are needed to be modified.

r_icd <- filter(all_icd, grepl("R", DIS_NAME))
r_icd$NAME_COUNT <- nchar(r_icd$DIS_NAME)
r_icd <- filter(r_icd, NAME_COUNT <= 3)

other_icd <- filter(all_icd, !(grepl("R", DIS_NAME)))

set.seed(1234)
tmp_comb2 <- c()
r_comb <- c()
i <- 0
while(i < 1000){
  if(i %% 100 == 0) print(paste0(i, "th start!!"))
  
  tmp_comb <- sort(sample(r_icd$DIS_NAME, sample(c(1, 2, 3), 1)))
  if(length(which(tmp_comb2 == paste0(tmp_comb, collapse = ""))) > 0){
    next
  }
  tmp_comb2 <- c(tmp_comb2, paste0(tmp_comb, collapse = ""))
  
  tmp_icd <- filter(all_icd, DIS_NAME %in% tmp_comb)
  tmp_avg <- transpose(as.data.frame(apply(tmp_icd[,2:301], 2, mean)))
  
  other_icd2 <- other_icd
  other_icd2$COS_SIM <- as.vector(simil(other_icd2[2:301], tmp_avg[1:300], method = "cosine"))
  max_dis_name <- filter(other_icd2, COS_SIM == max(COS_SIM))$DIS_NAME
  max_dis_name <- max_dis_name[1]
  
  tmp_df <- data.frame(R1="", R2="", R3="", stringsAsFactors = FALSE)
  tmp_df[,1:length(tmp_comb)] <- tmp_comb
  tmp_df$BEST_ICD <- paste0(max_dis_name, collapse = ",")
  tmp_df$COS_SIM <- filter(other_icd2, DIS_NAME %in% max_dis_name)$COS_SIM
  
  r_comb <- rbind(r_comb, tmp_df)
  i <- i + 1
}

r_comb$NTILE <- ntile(r_comb$COS_SIM, 100)
r_comb <- arrange(r_comb, COS_SIM)

#write.csv(r_comb, "r_comb.csv", row.names = FALSE)
#r_comb <- fread("r_comb.csv", data.table = FALSE)

filter(r_comb, NTILE == 100) # for table 2 

#if you want a full table,
View(r_comb)




