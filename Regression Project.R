hotel <- read.csv("Hotel.csv")
View(hotel)

library(ggplot2)
library(car)


summary(hotel$ADR)
sd(hotel$ADR)

ggplot(data = hotel) +
  geom_histogram(mapping = aes(x = ADR))+
  theme_minimal()

#prettier graph
ggplot(data = hotel) +
  geom_histogram(mapping = aes(x = ADR), 
                 bins = 50, 
                 fill = "#69b3a2", 
                 color = "white", 
                 alpha = 0.8) +
  theme_minimal(base_size = 14) +
  labs(
    title = "Distribution of Average Daily Rate (ADR)",
    x = "Average Daily Rate (ADR)",
    y = "Count"
  ) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    axis.text = element_text(color = "#4a4a4a"),
    panel.grid.major = element_line(color = "#e0e0e0"),
    panel.grid.minor = element_blank()
  )


summary(hotel$DistanceSkiLift_KM)
sd(hotel$DistanceSkiLift_KM)
ggplot(data = hotel) +
  geom_histogram(mapping = aes(x = DistanceSkiLift_KM))+
  theme_minimal()

ggplot(data = hotel) +
  geom_histogram(
    mapping = aes(x = DistanceSkiLift_KM),
    bins = 40,
    fill = "#FFB347",
    color = "white",
    alpha = 0.8
  ) +
  theme_minimal(base_size = 14) +
  labs(
    title = "Distribution of Distance to Ski Lift",
    x = "Distance to Ski Lift (KM)",
    y = "Count"
  ) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    axis.text = element_text(color = "#4a4a4a"),
    panel.grid.major = element_line(color = "#e0e0e0"),
    panel.grid.minor = element_blank()
  )


summary(hotel$BookingComRating)
sd(hotel$BookingComRating)
ggplot(data = hotel) +
  geom_histogram(mapping = aes(x = BookingComRating))+
  theme_minimal()
ggplot(data = hotel) +
  geom_histogram(
    mapping = aes(x = BookingComRating),
    bins = 30,
    fill = "#6A5ACD",  # Soft purple
    color = "white",
    alpha = 0.8
  ) +
  theme_minimal(base_size = 14) +
  labs(
    title = "Distribution of Booking.com Ratings",
    x = "Booking.com Rating",
    y = "Count"
  ) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    axis.text = element_text(color = "#4a4a4a"),
    panel.grid.major.x = element_blank(),
    panel.grid.minor.x = element_blank(),
    panel.border = element_blank()
  )


summary(hotel$RoomSize)
sd(hotel$RoomSize)
ggplot(data = hotel) +
  geom_histogram(mapping = aes(x = RoomSize))+
  theme_minimal()

ggplot(data = hotel) +
  geom_histogram(
    aes(x = RoomSize),
    bins = 30,              
    fill = "#4DAF4A",       
    color = "white", 
    alpha = 0.8          
  ) +
  theme_minimal(base_size = 14) +
  labs(
    title = "Distribution of Room Sizes",
    x = "Room Size (sq meters)",
    y = "Count"
  ) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold", size = 16),
    axis.text = element_text(color = "#4a4a4a"),
    axis.title = element_text(face = "bold"),
    panel.grid.major.y = element_line(color = "#e0e0e0"),
    panel.grid.major.x = element_blank()
  )

table(hotel$Location)
ggplot(hotel, aes(x = Location, y = Percentage, fill = Location)) +
  geom_bar(stat = "identity", width = 0.6) +
  geom_text(aes(label = paste0(Percentage, "% (", Count, ")")), 
            vjust = -0.5, size = 4) +
  scale_fill_brewer(palette = "Set2") +
  theme_minimal(base_size = 14) +
  labs(
    title = "Distribution of Locations",
    x = "Location",
    y = "Percentage"
  ) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    legend.position = "none"
  )

pie(table(hotel$Location))
location_counts <- table(hotel$Location)
location_percentages <- round(100 * prop.table(location_counts), 1)
labels <- paste0(names(location_counts), " (", location_percentages, "%)")


pie(
  table(hotel$Location),
  labels = labels,
  col = c("#FFB347", "#6A5ACD", "#FF6347", "#4DAF4A", "#FF69B4"),
  main = "Distribution of Hotel Locations",
  border = "white",
  cex = 1.5
)



table(hotel$WellnessActivities)
pie(
  table(hotel$WellnessActivities),
  labels = c("With them (90.2%)", "Without (9.8%)"),
  col = c("#6A5ACD", "#FF69B4"),
  main = "Distribution of Wellness Activities",
  border = "white",
  cex = 1.2
)


modelB <- lm(ADR ~ DistanceSkiLift_KM, data = hotel)
summary(modelB)


ggplot(data = hotel, mapping = aes(x = DistanceSkiLift_KM, y = ADR)) + 
  geom_point(mapping = aes(color = Location)) +
  geom_smooth() +
  theme_minimal() +
  labs(title = "Relationship Between Room Rate and Distance from Ski Lift",
       x = "Distance from Ski Lift (km)",
       y = "Average Daily Room Rate (chf)")



model = lm(ADR ~ DistanceSkiLift_KM  + BookingComRating + RoomSize + WellnessActivities + Location, data = hotel)
summary(model)


ggplot(data = hotel, mapping = aes(x = DistanceSkiLift_KM, y = ADR)) + 
  geom_point(mapping = aes(color = Location)) +
  geom_smooth() +
  theme_minimal() +
  labs(title = "Relationship Between Room Rate and Distance from Ski Lift",
       x = "Distance from Ski Lift (km)",
       y = "Average Daily Room Rate (chf)")


model2 = lm(ADR ~ DistanceSkiLift_KM:CityCenter + BookingComRating + RoomSize + WellnessActivities + Location, data = hotel)
summary(model2)

#need to run an interaction term
ggplot(hotel, aes(x = DistanceSkiLift_KM, y = ADR, color = CityCenter)) +
  geom_point() +
  geom_smooth(method = "lm", aes(group = CityCenter), se = FALSE) +
  theme_minimal()

model <- lm(ADR ~ DistanceSkiLift_KM * CityCenter, data = hotel)
summary(model)


################################################
# Regression diagnostics
################################################
hotel$DistanceSkiLift_KM[hotel$DistanceSkiLift_KM == 0] <- 0.001

modelHotel1 = lm(ADR ~ DistanceSkiLift_KM + RoomSize + BookingComRating + WellnessActivities + Location, data=hotel)
summary(modelHotel1)

modelHotel2 = lm(ADR ~ DistanceSkiLift_KM:CityCenter + RoomSize + BookingComRating + WellnessActivities + Location, data=hotel)
summary(modelHotel2)

modelHotelNew = lm(log(ADR) ~ DistanceSkiLift_KM + RoomSize + BookingComRating + WellnessActivities + Location, data=hotel)

modelHotelNew2 = lm(log(ADR) ~ DistanceSkiLift_KM:CityCenter + RoomSize + BookingComRating + WellnessActivities + Location, data=hotel)

# Plot for residuals against fitted
plot(fitted(modelHotel1), residuals(modelHotel1), 
     ylab="Residuals", xlab="Fitted Values", 
     main="Residual Plot: \n Residuals vs. Fitted")
abline(h=0, col="red", lty=2)

plot(fitted(modelHotel2), residuals(modelHotel2), 
     ylab="Residuals", xlab="Fitted Values", 
     main="Residual Plot: \n Residuals vs. Fitted")
abline(h=0, col="red", lty=2)

plot(fitted(modelHotelNew), residuals(modelHotelNew), 
     ylab="Residuals", xlab="Fitted Values", 
     main="Residual Plot: \n Residuals vs. Fitted")
abline(h=0, col="red", lty=2)

plot(fitted(modelHotelNew2), residuals(modelHotelNew2), 
     ylab="Residuals", xlab="Fitted Values", 
     main="Residual Plot: \n Residuals vs. Fitted")
abline(h=0, col="red", lty=2)


# Normal QQ plot
qqnorm(residuals(modelHotel1))
qqline(residuals(modelHotel1), col="red", lty=2)

qqnorm(residuals(modelHotel2))
qqline(residuals(modelHotel2), col="red", lty=2)

qqnorm(residuals(modelHotelNew))
qqline(residuals(modelHotelNew), col="red", lty=2)


vif(modelHotel1)
vif(modelHotel2)
vif(modelHotelNew)

ggplot(hotel, aes(x = DistanceSkiLift_KM, y = ADR, color = RoomSize)) +
  geom_point() +
  geom_smooth(method = "lm", aes(group = RoomSize), se = FALSE) +
  theme_minimal()

ggplot(hotel, aes(x = DistanceSkiLift_KM, y = ADR, color = BookingComRating)) +
  geom_point() +
  geom_smooth(method = "lm", aes(group = BookingComRating), se = FALSE) +
  theme_minimal()

ggplot(hotel, aes(x = DistanceSkiLift_KM, y = ADR, color = WellnessActivities)) +
  geom_point() +
  geom_smooth(method = "lm", aes(group = WellnessActivities), se = FALSE) +
  theme_minimal()

ggplot(hotel, aes(x = log(DistanceSkiLift_KM), y = ADR, color = Location)) +
  geom_point() +
  geom_smooth(method = "lm", aes(group = Location), se = FALSE) +
  theme_minimal()

summary(modelHotelNew)
modelHotelNew2 = lm(log(ADR) ~ DistanceSkiLift_KM + DistanceSkiLift_KM:CityCenter + RoomSize + BookingComRating + WellnessActivities + Location, data=hotel)

summary(modelHotelNew2)
