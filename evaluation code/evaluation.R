rm(list=ls())
library(tidyverse)
library(rpart)
library(rattle)
library(rpart.plot)
library(RColorBrewer)

setwd('../data/')
fpd_df <- read.csv('fpd_eval_forR.csv') %>% as_tibble()


onepull <- function(tb, pull_num, form){
  tb_pull <- tb %>% filter(pull == pull_num, cnt > 10)
  fpd_tree <- rpart(form, data=tb_pull, method="anova")
  fancyRpartPlot(fpd_tree)
  lm_mod <- lm(form, data=tb_pull)
  summary(lm_mod)
}

onepull(fpd_df, 1, "mp60 ~ expected + fpd_score")



cart_df <- read.csv("cart_eval_forR.csv") %>% as_tibble()
summary(cart_df[-c(1, 3)])
hist(cart_df$cart_score)

onepull(cart_df, 11, "mp60 ~ cart_score + approval_amount")


joined_df <- inner_join(cart_df[c(1,3,6)], fpd_df)

onepull(joined_df, 4, "mp60 ~ expected + fpd_score + cart_score")

