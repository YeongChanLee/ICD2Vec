#icd2vec comorbidity
library(dplyr)
library(data.table)
library(lubridate)
library(scales)

all_icd <- fread("../../../model/bio-clinicalBERT_icd2vec_finetuning/icd_code_vec_bio-clinicalBERT_finetuning.csv", header = TRUE, data.table = FALSE)
colnames(all_icd)[3:length(all_icd)] <- paste0("V", 1:768)
all_icd <- all_icd[,-1]
all_icd <- rename(all_icd, DIS_NAME = DIS_CODE)

#n_ab <- fread("ukbb_comorbidities2_sci.csv", data.table = FALSE)
#n_ab$SIG <- ifelse((n_ab$RR_L < 1) & (1 < n_ab$RR_U), 0 , 1)
#n_ab <- filter(n_ab, N_X1X2 > 50 & N_X1 > 50 & N_X2 > 50)
#n_ab2 <- filter(n_ab, SIG == 1)
#fwrite(n_ab2, "ukbb_comorbidities_sig.csv")

n_ab <- fread("ukbb_comorbidities_sig.csv", data.table = FALSE)
n_ab$COS_SIM <- 1
for(i in 1:nrow(n_ab)){
  if(i %% 1000 == 0) print(paste0(i, "th start!!"))
  n_ab[i,]$COS_SIM <- 1 - as.vector(dist(filter(all_icd, DIS_NAME == n_ab[i,]$X1)[2:769], filter(all_icd, DIS_NAME == n_ab[i,]$X2)[2:769], method = "cosine"))
}
#fwrite(n_ab, "ukbb_comorbidities_sig.csv")

comor <- n_ab
comor$LOG_RR <- log(comor$RR)
comor$COS_SIM_TILE <- ntile(comor$COS_SIM, 50)
tmp <- comor %>% group_by(COS_SIM_TILE) %>% summarise(MEDIAN = median(LOG_RR), MEAN = mean(LOG_RR), N = n())
tmp <- as.data.frame(tmp)

#Figure 2A
ggplot(data = comor) + 
  geom_boxplot(aes(x=COS_SIM_TILE, y=RR, group=COS_SIM_TILE), outlier.colour="#ebebeb", outlier.size=0.5, colour = "#9b9b9b") +
  stat_summary(aes(x=COS_SIM_TILE, y=RR), fun=mean, geom="point", size=2, color=c(rep("#025b9d", 45), rep("#9d020e", 5))) +
  theme_classic(base_size = 35) +
  coord_cartesian(ylim=c(0,50)) +
  labs(x="50-tiles of cosine similarity",
       y=c("Relative risk"))
cor.test(comor$COS_SIM, log10(comor$RR))
#0.111 (0.106-0.117)
cor.test(filter(comor, COS_SIM_TILE > 45)$COS_SIM, log10(filter(comor, COS_SIM_TILE > 45)$RR))
#0.178 (0.161-0.195)

library(limma)
comor$TOP10 <- "Others"
comor[which(comor$COS_SIM_TILE >= 45),]$TOP10 <- "Top 10%"
comor$LOG_RR <- log10(comor$RR)
comor2 <- select(comor, TOP10, RR)
x <- t(comor2$RR)
rownames(x) <- "COMORBIDITY"
y <- ifelse(comor2$TOP10 == "Others",0, 1)
design <- cbind(Grp1=1,Grp2vs1=y)
fit <- lmFit(x,design)
fit <- eBayes(fit)
topTable(fit,coef=2)
#  logFC AveExpr    t  P.Value adj.P.Val   B
#1  5.84    6.42 15.9 1.28e-56  1.28e-56 118
#################################################

#Figure 2D
comor2 <- comor %>% 
  group_by(TOP10)%>%  
  summarise(RR.mean= mean(RR),
            s.d=sd(RR),
            n=length(RR))%>% 
  mutate(s.e=s.d/sqrt(n)) 
ggplot(data = comor2) +
  geom_bar(aes(x = TOP10, y = RR.mean, fill = TOP10), stat = "identity", alpha = 0.2, color=c("#025b9d", "#9d020e")) +
  geom_errorbar(aes(x =TOP10, ymin = RR.mean - s.e, ymax = RR.mean + s.e), width = 0.3, color = c("#025b9d", "#9d020e")) + 
  scale_fill_manual(values =c("#025b9d", "#9d020e")) +
  stat_summary(aes(x = TOP10, y = RR.mean),fun=mean, geom="point", color = c("#025b9d", "#9d020e")) + 
  theme_classic(base_size = 35) +
  theme(legend.title = element_blank(), legend.position = "none") +
  labs(x="", y="Relative risk")  +
  coord_cartesian(ylim=c(0, 15))

