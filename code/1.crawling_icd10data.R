##crawling web
## https://www.icd10data.com


##https://www.icd10data.com/ICD10CM/Codes/A00-B99/A00-A09/A00-

library(rvest)
library(stringr)
library(data.table)
library(dplyr)
library(httr)

text_prepro <- function(tmp_string, tmp_word){
  tmp_string <- str_replace_all(tmp_string, '</li', tmp_word)
  tmp_string <- str_replace_all(tmp_string, '</a', tmp_word)
  tmp_string <- str_replace_all(tmp_string, '\"', tmp_word)
  tmp_string <- str_replace_all(tmp_string, "\r", tmp_word)
  tmp_string <- str_replace_all(tmp_string, "\n", tmp_word)
  tmp_string <- str_replace_all(tmp_string, "<ul>", tmp_word)
  tmp_string <- str_replace_all(tmp_string, "</ul>", tmp_word)
  tmp_string <- str_replace_all(tmp_string, "<li>", tmp_word)
  tmp_string <- str_replace_all(tmp_string, "</li>", tmp_word)
  tmp_string <- str_replace_all(tmp_string, '>', tmp_word)
  tmp_string <- str_replace_all(tmp_string, '<em', tmp_word)
  tmp_string <- str_replace_all(tmp_string, '</em', tmp_word)
  tmp_string <- str_replace_all(tmp_string, '<b', tmp_word)
  tmp_string <- str_replace_all(tmp_string, '</b', tmp_word)
  tmp_string <- gsub("\\s+", " ", str_trim(tmp_string))
  return(tmp_string)
}

##

main <- "https://www.icd10data.com"


tmp <- "https://www.icd10data.com/ICD10CM/Codes/"
tmp2 <- read_html(tmp)
tmp3 <- html_nodes(tmp2, "body") %>% html_nodes("ul li .identifier")
h1_1 <- tmp3 %>% html_attr("href") #URL
h1_1 <- h1_1[1:22]
h1_2 <- tmp3 %>% html_text() #DIS_CLASS
h1_2 <- h1_2[1:22]
h1_3 <- html_nodes(tmp2, "body") %>% html_nodes("ul li") %>% html_text()  #DIS_NAME
h1_3 <- h1_3[69:90]

for(i in 1:length(h1_3)){
  #DIS_NAME
  tmp_h3 <- text_prepro(h1_3[i], "")
  tmp_h3 <- substr(tmp_h3, 9, nchar(tmp_h3))
  h1_3[i] <- tmp_h3
}

main2 <- paste0(main, h1_1)

icd <- data.frame(DIS_CLASS = h1_2, URL = main2, DIS_NAME = h1_3, stringsAsFactors = FALSE)
icd$CLI_INFO <- ""
icd$APP_SYN <- ""

icd2 <- data.frame(DIS_CLASS = "", URL = "", DIS_NAME = "", stringsAsFactors = FALSE)
icd2$CLI_INFO <- ""
icd2$APP_SYN <- ""

icd3 <- data.frame(DIS_CLASS = "", URL = "", DIS_NAME = "", stringsAsFactors = FALSE)
icd3$CLI_INFO <- ""
icd3$APP_SYN <- ""

icd4 <- data.frame(DIS_CLASS = "", URL = "", DIS_NAME = "", stringsAsFactors = FALSE)
icd4$CLI_INFO <- ""
icd4$APP_SYN <- ""

for(i in 1:nrow(icd)){
  print(paste0(icd[i,]$DIS_CLASS, " start!! -- i"))
  tmp_i <- icd[i,]$URL
  tmp_i2 <- read_html(tmp_i)
  
  #check whether Codes in the page, then we can add rows in 'icd2'
  tmp_i3 <- html_nodes(tmp_i2, ".i51")
  #URL
  h2_1 <- html_nodes(tmp_i3, ".identifier") %>% html_attr("href")
  h2_main <- paste0(main, h2_1)
  #DIS_CLASS
  h2_2 <- html_nodes(tmp_i3, "li") %>% html_nodes("a") %>% html_text()
  h2_2 <- text_prepro(h2_2, "")
  #DIS_NAME
  h2_3 <- html_nodes(tmp_i3, "li") %>% html_text()
  h2_3 <- str_replace_all(h2_3, h2_2, "")
  h2_3 <- text_prepro(h2_3, "")
  tmp_icd2 <- data.frame(DIS_CLASS = h2_2, URL = h2_main, DIS_NAME = h2_3, stringsAsFactors = FALSE)
  tmp_icd2$CLI_INFO <- ""
  tmp_icd2$APP_SYN <- ""
  
  for(j in 1:nrow(tmp_icd2)){
    print(paste0(tmp_icd2[j,]$DIS_CLASS, " start!! -- j"))
    
    tmp_j <- tmp_icd2[j,]$URL
    tmp_j2 <- read_html(tmp_j)
    
    #check whether Codes in the page, then we can add rows in 'icd3'
    tmp_j3 <- html_nodes(tmp_j2, ".i51")
    #URL
    h3_1 <- html_nodes(tmp_j3, ".identifier") %>% html_attr("href")
    h3_main <- paste0(main, h3_1)
    #DIS_CLASS
    h3_2 <- html_nodes(tmp_j3, "li") %>% html_nodes("a") %>% html_text()
    h3_2 <- text_prepro(h3_2, "")
    #DIS_NAME
    h3_3 <- html_nodes(tmp_j3, "li") %>% html_text()
    h3_3 <- str_replace_all(h3_3, h3_2, "")
    h3_3 <- text_prepro(h3_3, "")
    tmp_icd3 <- data.frame(DIS_CLASS = h3_2, URL = h3_main, DIS_NAME = h3_3, stringsAsFactors = FALSE)
    tmp_icd3$CLI_INFO <- ""
    tmp_icd3$APP_SYN <- ""
    tmp_j2 <- as.character(tmp_j2)
    
    where_loc <- unlist(str_locate_all(string = tmp_j2, pattern = '<span>Clinical Information</span>'))
    cli_info <- c()
    if(length(where_loc) > 0){
      cli_info <- str_split(tmp_j2, '<span>Clinical Information</span>')[[1]][2]
      cli_info <- str_split(cli_info, '<div class="proper-ad-leaderboard">')[[1]][1]
      cli_info <- text_prepro(cli_info, " ")
      tmp_icd2[j,]$CLI_INFO <- cli_info
    }
    
    where_loc <- unlist(str_locate_all(string = tmp_j2, pattern = '<span>Approximate Synonyms</span>'))
    app_syn <- c()
    if(length(where_loc) > 0){
      app_syn <- str_split(tmp_j2, '<span>Approximate Synonyms</span>')[[1]][2]
      app_syn <- str_split(app_syn, '</ul>')[[1]][1]
      app_syn <- text_prepro(app_syn, " ")
      tmp_icd2[j,]$APP_SYN <- app_syn
    }
    
    #if(nrow(tmp_icd3) == 0) 
    for(k in 1:nrow(tmp_icd3)){
      print(paste0(tmp_icd3[k,]$DIS_CLASS, " start!! -- k"))
      
      tmp_k <- tmp_icd3[k,]$URL
      tmp_k2 <- read_html(tmp_k)
      tmp_k2 <- html_nodes(tmp_k2, "body")
      
      #check whether Codes in the page, then we can add rows in 'icd4'
      tmp_k3 <- html_nodes(tmp_k2, ".codeHierarchy")
      tmp_k3 <- tmp_k3[length(tmp_k3)]
      #URL
      h4_1 <- html_nodes(tmp_k3, ".identifierSpacing") %>% html_attr("href")
      if(length(h4_1) == 0){ h4_1 <- html_nodes(tmp_k3, ".identifier") %>% html_attr("href") }
      h4_main <- paste0(main, h4_1)
      #DIS_CLASS
      h4_2 <- html_nodes(tmp_k3, "li") %>% html_nodes("a") %>% html_text()
      h4_2 <- text_prepro(h4_2, "")
      #DIS_NAME
      h4_3 <- html_nodes(tmp_k3, "span") %>% html_text()
      if(length(h4_3) == 0){ h4_3 <- html_nodes(tmp_k3, "li") %>% html_text() }
      h4_3 <- str_replace_all(h4_3, h4_2, "")
      h4_3 <- text_prepro(h4_3, "")
      tmp_icd4 <- data.frame(DIS_CLASS = h4_2, URL = h4_main, DIS_NAME = h4_3, stringsAsFactors = FALSE)
      tmp_icd4$CLI_INFO <- ""
      tmp_icd4$APP_SYN <- ""
      tmp_k2 <- as.character(tmp_k2)
      
      where_loc <- unlist(str_locate_all(string = tmp_k2, pattern = '<span>Clinical Information</span>'))
      cli_info <- c()
      if(length(where_loc) > 0){
        cli_info <- str_split(tmp_k2, '<span>Clinical Information</span>')[[1]][2]
        cli_info <- str_split(cli_info, '<div class="proper-ad-leaderboard">')[[1]][1]
        cli_info <- text_prepro(cli_info, " ")
        tmp_icd3[k,]$CLI_INFO <- cli_info
      }
      
      where_loc <- unlist(str_locate_all(string = tmp_k2, pattern = '<span>Approximate Synonyms</span>'))
      app_syn <- c()
      if(length(where_loc) > 0){
        app_syn <- str_split(tmp_k2, '<span>Approximate Synonyms</span>')[[1]][2]
        app_syn <- str_split(app_syn, '</ul>')[[1]][1]
        app_syn <- text_prepro(app_syn, " ")
        tmp_icd3[k,]$APP_SYN <- app_syn
      }
      
      for(l in 1:nrow(tmp_icd4)){
        print(paste0(tmp_icd4[l,]$DIS_CLASS, " start!! -- l"))
        
        tmp_l <- tmp_icd4[l,]$URL
        tmp_l2 <- read_html(tmp_l)
        tmp_l2 <- html_nodes(tmp_l2, "body")
        
        where_loc <- unlist(str_locate_all(string = tmp_l2, pattern = '<span>Clinical Information</span>'))
        cli_info <- c()
        if(length(where_loc) > 0){
          cli_info <- str_split(tmp_l2, '<span>Clinical Information</span>')[[1]][2]
          cli_info <- str_split(cli_info, '<span>Code History</span>')[[1]][1]
          cli_info <- str_split(cli_info, '<span>ICD-10-CM')[[1]][1]
          cli_info <- text_prepro(cli_info, " ")
          tmp_icd4[l,]$CLI_INFO <- cli_info
        }
        
        where_loc <- unlist(str_locate_all(string = tmp_l2, pattern = '<span>Approximate Synonyms</span>'))
        app_syn <- c()
        if(length(where_loc) > 0){
          app_syn <- str_split(tmp_l2, '<span>Approximate Synonyms</span>')[[1]][2]
          app_syn <- str_split(app_syn, '</ul>')[[1]][1]
          app_syn <- text_prepro(app_syn, " ")
          tmp_icd4[l,]$APP_SYN <- app_syn
        }
      } # l end
      icd4 <- rbind(icd4, tmp_icd4)
      write.csv(icd4, "icd_info4_20210715.csv", row.names = FALSE)
    } # k end
    icd3 <- rbind(icd3, tmp_icd3)
    write.csv(icd3, "icd_info3_20210715.csv", row.names = FALSE)
  } # j end
  icd2 <- rbind(icd2, tmp_icd2)
  write.csv(icd2, "icd_info2_20210715.csv", row.names = FALSE)
} # i end

write.csv(icd, "icd_info_20210715.csv", row.names = FALSE)
write.csv(icd2, "icd_info2_20210715.csv", row.names = FALSE)
write.csv(icd3, "icd_info3_20210715.csv", row.names = FALSE)
write.csv(icd4, "icd_info4_20210715.csv", row.names = FALSE)

View(icd4)

##post-processing
icd4[grep("<", icd4$APP_SYN)[1],]

icd4$CLI_INFO2 <- icd4$CLI_INFO
for(i in grep("<", icd4$CLI_INFO)){
  tmp_cli <- icd4[i,]$CLI_INFO
  tmp_cli <- text_prepro(tmp_cli, "")
  tmp_cli <- unlist(str_split(tmp_cli,"<"))[1]
  icd4[i,]$CLI_INFO2 <- tmp_cli
}


icd4 <- select(icd4, DIS_CLASS, URL, DIS_NAME, CLI_INFO2, APP_SYN)
icd4 <- rename(icd4, CLI_INFO=CLI_INFO2)

write.csv(icd4, "../data/icd_info4.csv", row.names = FALSE)