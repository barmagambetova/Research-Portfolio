telework <- read.csv("Telework Final (1).csv")

#LOADING LIBRARIES
library(ggplot2)
library(dplyr)
library(car)

View(telework)

#DATASET MANIPULATIONS

telework$Age <- 2024 - telework$Birth_Year



telework$Remote_Work_Percentage <- replace(telework$Remote_Work_Percentage, telework$Remote_Work_Percentage == "100% - I spent all of my time remote working", 100)
telework$Remote_Work_Percentage <- replace(telework$Remote_Work_Percentage, telework$Remote_Work_Percentage == "100%", 100)

telework$Remote_Work_Percentage <- replace(telework$Remote_Work_Percentage, telework$Remote_Work_Percentage == "50% - I spent about half of my time remote working", 50)
telework$Remote_Work_Percentage <- replace(telework$Remote_Work_Percentage, telework$Remote_Work_Percentage == "50%", 50)

telework$Remote_Work_Percentage <- replace(telework$Remote_Work_Percentage, telework$Remote_Work_Percentage == "1%", 1)

telework$Remote_Work_Percentage <- replace(telework$Remote_Work_Percentage, telework$Remote_Work_Percentage == "10%", 10)

telework$Remote_Work_Percentage <- replace(telework$Remote_Work_Percentage, telework$Remote_Work_Percentage == "1%", 1)

telework$Remote_Work_Percentage <- replace(telework$Remote_Work_Percentage, telework$Remote_Work_Percentage == "20%", 20)

telework$Remote_Work_Percentage <- replace(telework$Remote_Work_Percentage, telework$Remote_Work_Percentage == "30%", 30)

telework$Remote_Work_Percentage <- replace(telework$Remote_Work_Percentage, telework$Remote_Work_Percentage == "40%", 40)

telework$Remote_Work_Percentage <- replace(telework$Remote_Work_Percentage, telework$Remote_Work_Percentage == "Less than 10% of my time", 5)
telework$Remote_Work_Percentage <- replace(telework$Remote_Work_Percentage, telework$Remote_Work_Percentage == "5%", 5)

telework$Remote_Work_Percentage <- replace(telework$Remote_Work_Percentage, telework$Remote_Work_Percentage == "Rarely or never", 1)

telework$Remote_Work_Percentage <- replace(telework$Remote_Work_Percentage, telework$Remote_Work_Percentage == "60%", 60)

telework$Remote_Work_Percentage <- replace(telework$Remote_Work_Percentage, telework$Remote_Work_Percentage == "70%", 70)

telework$Remote_Work_Percentage <- replace(telework$Remote_Work_Percentage, telework$Remote_Work_Percentage == "80%", 80)

telework$Remote_Work_Percentage <- replace(telework$Remote_Work_Percentage, telework$Remote_Work_Percentage == "90%", 90)


telework$Industry_Group <- case_when(
  telework$Industry %in% c("Accommodation and Food", "Administrative and Support", "Arts and Recreation", 
                           "Retail Trade", "Rental, Hiring and Real Estate") ~ "Service-Oriented",
  telework$Industry %in% c("Education and Training", "Financial and Insurance", 
                           "Information Media and Telecommunications", "Professional, Scientific and Technical") ~ "Knowledge-Based",
  telework$Industry %in% c("Health Care and Social Assistance", "Public Administration and Safety", 
                           "Electricity, Gas, Water and Waste") ~ "Public and Community Services",
  telework$Industry %in% c("Manufacturing", "Construction", "Mining") ~ "Industrial and Manufacturing",
  telework$Industry == "Agriculture, Forestry and Fishing" ~ "Agriculture and Natural Resources",
  telework$Industry %in% c("Transport, Postal and Warehousing", "Wholesale Trade") ~ "Logistics and Trade",
  TRUE ~ "Other"
)


telework$clerk <- grepl("Clerical", telework$Occupation)
telework$Occupation <- replace(telework$Occupation, telework$clerk == TRUE, "Clerical and administrative workers")

telework$tech <- grepl("Technicians", telework$Occupation)
telework$Occupation <- replace(telework$Occupation, telework$tech == TRUE, "Technicians and trades workers")

telework$prof <- grepl("Professionals", telework$Occupation)
telework$Occupation <- replace(telework$Occupation, telework$prof == TRUE, "Professionals")

telework$manage <- grepl("Managers", telework$Occupation)
telework$Occupation <- replace(telework$Occupation, telework$manage == TRUE, "Managers")

telework$sales <- grepl("Sales workers", telework$Occupation)
telework$Occupation <- replace(telework$Occupation, telework$sales == TRUE, "Sales workers")

telework$labor <- grepl("Labourers", telework$Occupation)
telework$Occupation <- replace(telework$Occupation, telework$labor == TRUE, "Labourers")

telework$machine <- grepl("Machinery operators and drivers", telework$Occupation)
telework$Occupation <- replace(telework$Occupation, telework$machine == TRUE, "Machinery operators and drivers")

telework$community <- grepl("Community and personal service workers", telework$Occupation)
telework$Occupation <- replace(telework$Occupation, telework$community == TRUE, "Community and personal service workers")

telework <- telework[, 1:24]


telework$new <- grepl("10% less", telework$Remote_Work_Productivity)
telework$Remote_Work_Productivity <- replace(telework$Remote_Work_Productivity, telework$new == TRUE, -10)

telework$new1 <- grepl("20% less", telework$Remote_Work_Productivity)
telework$Remote_Work_Productivity <- replace(telework$Remote_Work_Productivity, telework$new1 == TRUE, -20)

telework$new2 <- grepl("30% less", telework$Remote_Work_Productivity)
telework$Remote_Work_Productivity <- replace(telework$Remote_Work_Productivity, telework$new2 == TRUE, -30)

telework$new3 <- grepl("40% less", telework$Remote_Work_Productivity)
telework$Remote_Work_Productivity <- replace(telework$Remote_Work_Productivity, telework$new3 == TRUE, -40)

telework$new4 <- grepl("50% less", telework$Remote_Work_Productivity)
telework$Remote_Work_Productivity <- replace(telework$Remote_Work_Productivity, telework$new4 == TRUE, -50)


telework$new5 <- grepl("10% more", telework$Remote_Work_Productivity)
telework$Remote_Work_Productivity <- replace(telework$Remote_Work_Productivity, telework$new5 == TRUE, +10)
telework$new6 <- grepl("20% more", telework$Remote_Work_Productivity)
telework$Remote_Work_Productivity <- replace(telework$Remote_Work_Productivity, telework$new6 == TRUE, +20)
telework$new7 <- grepl("30% more", telework$Remote_Work_Productivity)
telework$Remote_Work_Productivity <- replace(telework$Remote_Work_Productivity, telework$new7 == TRUE, +30)
telework$new8 <- grepl("40% more", telework$Remote_Work_Productivity)
telework$Remote_Work_Productivity <- replace(telework$Remote_Work_Productivity, telework$new8 == TRUE, +40)
telework$new9 <- grepl("50% more", telework$Remote_Work_Productivity)
telework$Remote_Work_Productivity <- replace(telework$Remote_Work_Productivity, telework$new9 == TRUE, +50)

telework <- telework[, 1:24]

telework$new100 <- grepl("sole", telework$Org_Size)
telework$Org_Size <- replace(telework$Org_Size, telework$new100 == TRUE, "Between 1 and 19")

telework$new101 <- grepl("Between 1 and 4", telework$Org_Size)
telework$Org_Size <- replace(telework$Org_Size, telework$new101 == TRUE, "Between 1 and 19")

telework$new102 <- grepl("Between 5 and 19", telework$Org_Size)
telework$Org_Size <- replace(telework$Org_Size, telework$new102 == TRUE, "Between 1 and 19")

telework$neww <- grepl("same", telework$Remote_Work_Productivity)
telework$Remote_Work_Productivity <- replace(telework$Remote_Work_Productivity, telework$neww == TRUE, 0)

telework <- telework[, 1:24]


telework$Remote_Work_Percentage <- as.numeric(as.character(telework$Remote_Work_Percentage))
telework$Remote_Work_Productivity <- as.numeric(telework$Remote_Work_Productivity)


#GROUPING REMOTE WORK INTO 3 CATEGORIES
telework$Remote_Work_Group <- cut(telework$Remote_Work_Percentage,
                                  breaks = c(-Inf, 6, 51, 101), 
                                  labels = c("No Remote Work", "Moderate Remote Work", "Predominantly Remote Work"), 
                                  right = TRUE) 


ggplot(telework, aes(x = Remote_Work_Group)) +
  geom_bar(fill = "steelblue") +
  labs(title = "Distribution of Remote Work Groups",
       x = "Remote Work Group",
       y = "Count") +
  theme_minimal()

ggplot(telework, aes(x = Remote_Work_Group, y = Remote_Work_Productivity)) +
  geom_boxplot(fill = c("tomato", "gold", "skyblue")) +
  labs(title = "Productivity by Remote Work Group",
       x = "Remote Work Group",
       y = "Productivity") +
  theme_minimal()


#no need to run an interaction term for genders
ggplot(telework, aes(x = Remote_Work_Percentage, y = Remote_Work_Productivity, color = Gender)) +
  geom_point() +
  geom_smooth(method = "lm", aes(group = Gender), se = FALSE) +
  theme_minimal()

#no need to run an interaction term for org sizes
ggplot(telework, aes(x = Remote_Work_Percentage, y = Remote_Work_Productivity, color = Org_Size)) +
  geom_point() +
  geom_smooth(method = "lm", aes(group = Org_Size), se = FALSE) +
  theme_minimal()



#initial vizualisation of the effect
ggplot(data = telework, mapping = aes(x = Remote_Work_Percentage, y = Remote_Work_Productivity)) + 
  geom_point() +
  geom_smooth()

#RUNNING THE REGRESSION MODEL
model <- lm(Remote_Work_Productivity ~ Remote_Work_Group, data = telework)
summary(model)

model2 <- lm(Remote_Work_Productivity ~ Remote_Work_Group + Gender + Children + Org_Size + Location_Type + Industry_Group + Occupation + Job_Tenure + Age, data = telework)
summary(model2)


t.test(telework$Remote_Commute_Hours, telework$Office_Commute_Hours, paired = TRUE)
t.test(telework$Remote_Work_Hours, telework$Office_Hours, paired = TRUE)
t.test(telework$Remote_DomResp_Hours, telework$Office_DomResp_Hours, paired = TRUE)
t.test(telework$Remote_Sleep_Hours, telework$Office_Sleep_Hours, paired = TRUE)
t.test(telework$Remote_Family_Time_Hours, telework$Office_Family_Time_Hours, paired = TRUE)

mean(telework$Remote_Commute_Hours, na.rm=TRUE)
mean(telework$Office_Commute_Hours, na.rm=TRUE)
mean(telework$Remote_Work_Hours, na.rm=TRUE)
mean(telework$Office_Hours, na.rm=TRUE)
mean(telework$Remote_DomResp_Hours, na.rm=TRUE)
mean(telework$Office_DomResp_Hours, na.rm=TRUE)
mean(telework$Remote_Sleep_Hours, na.rm=TRUE)
mean(telework$Office_Sleep_Hours, na.rm=TRUE)
mean(telework$Remote_Family_Time_Hours, na.rm=TRUE)
mean(telework$Office_Family_Time_Hours, na.rm=TRUE)

# Create a data frame with the data
data <- data.frame(
  Activity = c("Commuting", "Working", "Sleeping", "Domestic Responsibilities", "Family Time"),
  Remote = c(1.2, 8.1, 7.5, 3.0, 4.3),
  Office = c(2.3, 7.85, 7.4, 2.8, 3.9)
)





summary(telework)
sd(telework$Remote_Work_Productivity, na.rm = TRUE)


table(telework$Gender)
table(telework$Org_Size)
table(telework$Location_Type)
table(telework$Children)
table(telework$Birth_Year)
table(telework$Job_Tenure)


summary(telework$Age)
sd(telework$Age)


table(telework$Occupation)
table(telework$Industry_Group)


