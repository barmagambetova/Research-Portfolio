fb= read.csv("Facebook.csv")
View(fb)



#HYPOTHESIS NUMBER 1

library(ggplot2)
library(dplyr)

#boxplot
boxplot(log(TotalInteractions+1)~Type, data=fb,
        xlab="Type of the post",
        ylab="Log of Total Interactions",
        main="Statistics of Facebook Data",
        col=c("violet", "skyblue", "pink", "lightgreen"))


#data for photo
subset_fb <- subset(fb, Type == "Photo")
View(subset_fb)
mean(subset_fb$TotalInteractions)            #218.8052
median(subset_fb$TotalInteractions)          #124
range(subset_fb$TotalInteractions)           #6334
min(subset_fb$TotalInteractions)             #0
max(subset_fb$TotalInteractions)             #6334
sd(subset_fb$TotalInteractions)              #407
summary(subset_fb$TotalInteractions)

#data for status
subset_fb1 <- subset(fb, Type == "Status")
View(subset_fb1)
mean(subset_fb1$TotalInteractions)          #217.0444
median(subset_fb1$TotalInteractions)        #186
range(subset_fb1$TotalInteractions)         #992
min(subset_fb1$TotalInteractions)           #17
max(subset_fb1$TotalInteractions)           #1009
sd(subset_fb1$TotalInteractions)            #178
summary(subset_fb1$TotalInteractions)

#data for link
subset_fb2 <- subset(fb, Type == "Link")
View(subset_fb2)
mean(subset_fb2$TotalInteractions)          #89.04545
median(subset_fb2$TotalInteractions)        #52.5
range(subset_fb2$TotalInteractions)         #414
min(subset_fb2$TotalInteractions)           #6
max(subset_fb2$TotalInteractions)           #420
sd(subset_fb2$TotalInteractions)            #95
summary(subset_fb2$TotalInteractions)

#data for video
subset_fb3 <- subset(fb, Type == "Video")
View(subset_fb3)
mean(subset_fb3$TotalInteractions)          #295.8571
median(subset_fb3$TotalInteractions)        #271
range(subset_fb3$TotalInteractions)         #469
min(subset_fb3$TotalInteractions)           #81
max(subset_fb3$TotalInteractions)           #550
sd(subset_fb3$TotalInteractions)            #183
summary(subset_fb3$TotalInteractions)


#calculating the median total interactions for each post type
median <- fb %>%
  group_by(Type) %>%
  summarise(MedianTotalInteractions = median(TotalInteractions, na.rm = TRUE))

#barplot
ggplot(median, aes(x = Type, y = MedianTotalInteractions, fill = Type)) +
  geom_bar(stat = "identity") +
  labs(title = "Statistics of Facebook Data",
       x = "Type of the post",
       y = "Median of Total Interactions")





#HYPOTHESIS NUMBER 2 


#data for Paid
subset_fb_paid <- subset(fb, Paid == "1")
View(subset_fb_paid)
mean(subset_fb_paid$TotalInteractions)            
median(subset_fb_paid$TotalInteractions)     
range(subset_fb_paid$TotalInteractions)
min(subset_fb_paid$TotalInteractions)
max(subset_fb_paid$TotalInteractions)             
sd(subset_fb_paid$TotalInteractions)

#data for UnPaid
subset_fb_unpaid <- subset(fb, Paid == "0")
View(subset_fb_unpaid)
mean(subset_fb_unpaid$TotalInteractions)            
median(subset_fb_unpaid$TotalInteractions)     
range(subset_fb_unpaid$TotalInteractions)
min(subset_fb_unpaid$TotalInteractions)
max(subset_fb_unpaid$TotalInteractions)             
sd(subset_fb_unpaid$TotalInteractions)


# Creating a box plot


boxplot(log(TotalInteractions +1)~Paid, data=fb,
        xlab="Paid",
        ylab="TotalInteractions",
        main="Paid/Unpaid Post and Total Interaction BoxPlot",
        col=c("blue","green"))


#HYPOTHESIS NUMBER 3

cor(fb$LifetimePostTotalReach,fb$TotalInteractions)


plot(log(fb$LifetimePostTotalReach),log(fb$TotalInteractions), 
     xlab="People who saw a page post)",
     ylab="Total interactions)",
     main="Number of people who saw post and total interactions",
     pch=9, col="violetred")
